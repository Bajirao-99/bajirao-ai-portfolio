import hashlib
import re
from statistics import mean
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ai.semantic_engine import (
    calculate_semantic_similarity,
)
from app.ai.skill_catalog import (
    canonicalize_skill_name,
    extract_skills,
)
from app.models.experience import Experience
from app.models.github import GitHubRepository
from app.models.job_match import JobMatchAnalysis
from app.models.profile import Profile
from app.models.project import Project
from app.models.research import ResearchPublication
from app.models.resume import Resume
from app.models.skill import Skill


AI_KEYWORDS = {
    "artificial intelligence",
    "machine learning",
    "deep learning",
    "nlp",
    "natural language processing",
    "llm",
    "large language model",
    "rag",
    "generative ai",
    "data science",
    "computer vision",
    "tensorflow",
    "pytorch",
    "transformers",
}

ACADEMIC_KEYWORDS = {
    "assistant professor",
    "associate professor",
    "professor",
    "faculty",
    "lecturer",
    "teaching",
    "academic",
    "university",
    "college",
    "research",
    "publication",
    "curriculum",
    "mentoring students",
}

RESEARCH_KEYWORDS = {
    "research",
    "publication",
    "paper",
    "thesis",
    "experiment",
    "dataset",
    "model evaluation",
    "natural language processing",
    "machine learning",
    "deep learning",
}


def join_text(*values: Any) -> str:
    parts: list[str] = []

    for value in values:
        if value is None:
            continue

        if isinstance(value, list):
            parts.extend(
                str(item)
                for item in value
                if item is not None
            )
            continue

        parts.append(str(value))

    return " ".join(parts)


def shorten_text(
    text: str | None,
    limit: int = 300,
) -> str | None:
    if text is None:
        return None

    normalized_text = re.sub(
        r"\s+",
        " ",
        text,
    ).strip()

    if len(normalized_text) <= limit:
        return normalized_text

    return (
        normalized_text[: limit - 3]
        .rstrip()
        + "..."
    )


def similarity_to_percentage(
    score: float,
) -> float:
    return round(
        max(
            0.0,
            min(1.0, score),
        )
        * 100,
        2,
    )


def average_top_scores(
    scores: list[float],
    count: int,
) -> float:
    if not scores:
        return 0.0

    highest_scores = sorted(
        scores,
        reverse=True,
    )[:count]

    return round(
        mean(highest_scores),
        2,
    )


def extract_required_experience_years(
    job_description: str,
) -> float | None:
    normalized_text = job_description.lower()

    range_match = re.search(
        r"(\d+(?:\.\d+)?)\s*"
        r"(?:-|–|—|to)\s*"
        r"(\d+(?:\.\d+)?)\s*"
        r"(?:years?|yrs?)",
        normalized_text,
    )

    if range_match is not None:
        return float(
            range_match.group(1)
        )

    minimum_match = re.search(
        r"(?:minimum|min\.?|at least)\s*"
        r"(\d+(?:\.\d+)?)\+?\s*"
        r"(?:years?|yrs?)",
        normalized_text,
    )

    if minimum_match is not None:
        return float(
            minimum_match.group(1)
        )

    general_match = re.search(
        r"(\d+(?:\.\d+)?)\+?\s*"
        r"(?:years?|yrs?)"
        r"(?:\s+of\s+experience)?",
        normalized_text,
    )

    if general_match is not None:
        return float(
            general_match.group(1)
        )

    return None


def determine_match_level(
    score: float,
) -> str:
    if score >= 80:
        return "Excellent Match"

    if score >= 65:
        return "Strong Match"

    if score >= 50:
        return "Moderate Match"

    return "Limited Match"


def load_portfolio_data(
    database_session: Session,
) -> dict[str, Any]:
    profile = database_session.scalar(
        select(Profile)
        .where(Profile.is_active.is_(True))
        .order_by(Profile.id.asc())
    )

    skills = list(
        database_session.scalars(
            select(Skill)
            .where(Skill.is_visible.is_(True))
            .order_by(
                Skill.display_order.asc(),
                Skill.id.asc(),
            )
        ).all()
    )

    experiences = list(
        database_session.scalars(
            select(Experience)
            .where(
                Experience.is_visible.is_(True)
            )
            .order_by(
                Experience.display_order.asc(),
                Experience.id.asc(),
            )
        ).all()
    )

    projects = list(
        database_session.scalars(
            select(Project)
            .where(Project.is_visible.is_(True))
            .order_by(
                Project.display_order.asc(),
                Project.id.asc(),
            )
        ).all()
    )

    research_records = list(
        database_session.scalars(
            select(ResearchPublication)
            .where(
                ResearchPublication.is_visible.is_(
                    True
                )
            )
            .order_by(
                ResearchPublication
                .display_order.asc(),
                ResearchPublication.id.asc(),
            )
        ).all()
    )

    resumes = list(
        database_session.scalars(
            select(Resume)
            .where(Resume.is_visible.is_(True))
            .order_by(
                Resume.display_order.asc(),
                Resume.id.asc(),
            )
        ).all()
    )

    github_repositories = list(
        database_session.scalars(
            select(GitHubRepository)
            .where(
                GitHubRepository.is_visible.is_(
                    True
                )
            )
        ).all()
    )

    return {
        "profile": profile,
        "skills": skills,
        "experiences": experiences,
        "projects": projects,
        "research": research_records,
        "resumes": resumes,
        "github_repositories": (
            github_repositories
        ),
    }


def collect_candidate_skills(
    portfolio_data: dict[str, Any],
) -> tuple[set[str], list[str]]:
    raw_skills: list[str] = []

    for skill in portfolio_data["skills"]:
        raw_skills.append(skill.name)

    for project in portfolio_data["projects"]:
        raw_skills.extend(
            project.tech_stack or []
        )

    for research in portfolio_data["research"]:
        raw_skills.extend(
            research.models_used or []
        )

    for repository in (
        portfolio_data["github_repositories"]
    ):
        if repository.language:
            raw_skills.append(
                repository.language
            )

    canonical_skills = {
        canonicalize_skill_name(
            skill_name
        ).lower()
        for skill_name in raw_skills
        if skill_name.strip()
    }

    return canonical_skills, raw_skills


def build_evidence_items(
    portfolio_data: dict[str, Any],
) -> list[dict[str, Any]]:
    evidence_items: list[dict[str, Any]] = []

    profile = portfolio_data["profile"]

    if profile is not None:
        evidence_items.append(
            {
                "type": "profile",
                "record": profile,
                "text": join_text(
                    profile.headline,
                    profile.short_bio,
                    profile.about_me,
                ),
            }
        )

    for experience in portfolio_data[
        "experiences"
    ]:
        evidence_items.append(
            {
                "type": "experience",
                "record": experience,
                "text": join_text(
                    experience.job_title,
                    experience.organization,
                    experience.employment_type,
                    experience.description,
                ),
            }
        )

    for project in portfolio_data["projects"]:
        evidence_items.append(
            {
                "type": "project",
                "record": project,
                "text": join_text(
                    project.title,
                    project.category,
                    project.short_description,
                    project.description,
                    project.tech_stack,
                    project.challenges,
                    project.solutions,
                    project.results,
                ),
            }
        )

    for research in portfolio_data["research"]:
        evidence_items.append(
            {
                "type": "research",
                "record": research,
                "text": join_text(
                    research.title,
                    research.research_type,
                    research.short_summary,
                    research.abstract,
                    research.dataset_details,
                    research.methodology,
                    research.models_used,
                    list(
                        (research.metrics or {}).keys()
                    ),
                ),
            }
        )

    return evidence_items


def determine_resume_type(
    job_description: str,
    recognized_skills: list[str],
) -> tuple[str, str]:
    normalized_text = job_description.lower()

    ai_score = sum(
        1
        for keyword in AI_KEYWORDS
        if keyword in normalized_text
    )

    academic_score = sum(
        1
        for keyword in ACADEMIC_KEYWORDS
        if keyword in normalized_text
    )

    ai_skill_names = {
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "natural language processing",
        "large language models",
        "rag",
        "generative ai",
        "computer vision",
        "tensorflow",
        "pytorch",
        "lstm",
        "bilstm",
        "transformers",
        "embeddings",
        "vector databases",
    }

    ai_score += sum(
        1
        for skill_name in recognized_skills
        if skill_name.lower() in ai_skill_names
    )

    if (
        academic_score >= 2
        and academic_score > ai_score
    ):
        return (
            "academic",
            "The job description emphasizes "
            "teaching, research or academic work.",
        )

    if ai_score >= 2:
        return (
            "ai-ml",
            "The job description emphasizes AI, "
            "machine learning, NLP or data-related "
            "skills.",
        )

    return (
        "software-engineer",
        "The job description primarily emphasizes "
        "software development, programming and "
        "engineering skills.",
    )


def find_recommended_resume(
    resumes: list[Resume],
    recommended_type: str,
) -> Resume | None:
    for resume in resumes:
        if (
            resume.resume_type.lower()
            == recommended_type.lower()
        ):
            return resume

    return None


def build_strengths(
    skill_score: float,
    matched_skills: list[str],
    required_years: float | None,
    candidate_years: float,
    relevant_experiences: list[dict],
    relevant_projects: list[dict],
    relevant_research: list[dict],
) -> list[str]:
    strengths: list[str] = []

    if skill_score >= 70 and matched_skills:
        strengths.append(
            "Strong overlap with the technologies "
            "identified in the job description."
        )

    if matched_skills:
        strengths.append(
            "Matched skills include: "
            + ", ".join(matched_skills[:6])
            + "."
        )

    if (
        required_years is not None
        and candidate_years >= required_years
    ):
        strengths.append(
            "The stated experience level meets or "
            "exceeds the detected minimum requirement."
        )

    if (
        relevant_experiences
        and relevant_experiences[0][
            "relevance_score"
        ]
        >= 40
    ):
        strengths.append(
            "The portfolio contains directly relevant "
            "professional experience."
        )

    if (
        relevant_projects
        and relevant_projects[0][
            "relevance_score"
        ]
        >= 40
    ):
        strengths.append(
            "At least one project provides relevant "
            "technical evidence for this role."
        )

    if (
        relevant_research
        and relevant_research[0][
            "relevance_score"
        ]
        >= 40
    ):
        strengths.append(
            "Research work provides additional "
            "evidence for the role requirements."
        )

    return strengths[:5]


def build_improvement_areas(
    missing_skills: list[str],
    required_years: float | None,
    candidate_years: float,
    relevant_projects: list[dict],
) -> list[str]:
    improvement_areas: list[str] = []

    if missing_skills:
        improvement_areas.append(
            "Consider demonstrating or learning these "
            "identified skills: "
            + ", ".join(missing_skills[:6])
            + "."
        )

    if (
        required_years is not None
        and candidate_years < required_years
    ):
        improvement_areas.append(
            "The detected experience requirement is "
            f"{required_years:g} years, while the "
            "portfolio currently states "
            f"{candidate_years:g} years."
        )

    if (
        not relevant_projects
        or relevant_projects[0][
            "relevance_score"
        ]
        < 30
    ):
        improvement_areas.append(
            "Add a project that more directly "
            "demonstrates the main responsibilities "
            "of this role."
        )

    if not improvement_areas:
        improvement_areas.append(
            "Tailor the recommended resume with the "
            "exact terminology used in the job "
            "description."
        )

    return improvement_areas[:5]


def save_job_match_analysis(
    database_session: Session,
    job_title: str | None,
    company_name: str | None,
    job_description: str,
    overall_score: float,
    match_level: str,
    score_breakdown: dict[str, float],
    matched_skills: list[str],
    missing_skills: list[str],
    recommended_resume_type: str,
    embedding_method: str,
) -> JobMatchAnalysis:
    description_hash = hashlib.sha256(
        job_description.encode("utf-8")
    ).hexdigest()

    analysis = JobMatchAnalysis(
        job_title=job_title,
        company_name=company_name,
        job_description_hash=description_hash,
        overall_match_score=overall_score,
        match_level=match_level,
        score_breakdown=score_breakdown,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        recommended_resume_type=(
            recommended_resume_type
        ),
        embedding_method=embedding_method,
    )

    database_session.add(analysis)
    database_session.commit()
    database_session.refresh(analysis)

    return analysis


def analyze_job_match(
    database_session: Session,
    job_description: str,
    job_title: str | None,
    company_name: str | None,
    top_k: int,
) -> dict[str, Any]:
    portfolio_data = load_portfolio_data(
        database_session
    )

    profile = portfolio_data["profile"]

    if profile is None:
        raise ValueError(
            "The active professional profile "
            "has not been configured."
        )

    (
        candidate_skill_set,
        raw_candidate_skills,
    ) = collect_candidate_skills(
        portfolio_data
    )

    recognized_job_skills = extract_skills(
        job_description,
        additional_skills=raw_candidate_skills,
    )

    matched_skills = [
        skill_name
        for skill_name in recognized_job_skills
        if skill_name.lower()
        in candidate_skill_set
    ]

    missing_skills = [
        skill_name
        for skill_name in recognized_job_skills
        if skill_name.lower()
        not in candidate_skill_set
    ]

    evidence_items = build_evidence_items(
        portfolio_data
    )

    similarity_scores, embedding_method = (
        calculate_semantic_similarity(
            job_description,
            [
                item["text"]
                for item in evidence_items
            ],
        )
    )

    for item, raw_score in zip(
        evidence_items,
        similarity_scores,
        strict=False,
    ):
        item["relevance_score"] = (
            similarity_to_percentage(
                raw_score
            )
        )

    experience_items = [
        item
        for item in evidence_items
        if item["type"] == "experience"
    ]

    project_items = [
        item
        for item in evidence_items
        if item["type"] == "project"
    ]

    research_items = [
        item
        for item in evidence_items
        if item["type"] == "research"
    ]

    semantic_score = average_top_scores(
        [
            item["relevance_score"]
            for item in evidence_items
        ],
        5,
    )

    required_years = (
        extract_required_experience_years(
            job_description
        )
    )

    candidate_years = float(
        profile.years_experience
    )

    if (
        required_years is None
        or required_years == 0
        or candidate_years >= required_years
    ):
        years_score = 100.0
    else:
        years_score = round(
            min(
                100.0,
                (
                    candidate_years
                    / required_years
                )
                * 100,
            ),
            2,
        )

    experience_relevance = average_top_scores(
        [
            item["relevance_score"]
            for item in experience_items
        ],
        2,
    )

    experience_score = round(
        (
            experience_relevance * 0.75
            + years_score * 0.25
        ),
        2,
    )

    project_score = average_top_scores(
        [
            item["relevance_score"]
            for item in project_items
        ],
        2,
    )

    research_score = average_top_scores(
        [
            item["relevance_score"]
            for item in research_items
        ],
        2,
    )

    if recognized_job_skills:
        skill_score = round(
            (
                len(matched_skills)
                / len(recognized_job_skills)
            )
            * 100,
            2,
        )
    else:
        skill_score = semantic_score

    normalized_job_description = (
        job_description.lower()
    )

    research_focused = any(
        keyword in normalized_job_description
        for keyword in RESEARCH_KEYWORDS
    )

    if recognized_job_skills:
        if research_focused:
            overall_score = (
                skill_score * 0.35
                + semantic_score * 0.20
                + experience_score * 0.20
                + project_score * 0.15
                + research_score * 0.10
            )
        else:
            overall_score = (
                skill_score * 0.40
                + semantic_score * 0.20
                + experience_score * 0.20
                + project_score * 0.20
            )
    else:
        if research_focused:
            overall_score = (
                semantic_score * 0.35
                + experience_score * 0.25
                + project_score * 0.20
                + research_score * 0.20
            )
        else:
            overall_score = (
                semantic_score * 0.40
                + experience_score * 0.30
                + project_score * 0.30
            )

    overall_score = round(
        max(
            0.0,
            min(100.0, overall_score),
        ),
        2,
    )

    match_level = determine_match_level(
        overall_score
    )

    sorted_experiences = sorted(
        experience_items,
        key=lambda item: item[
            "relevance_score"
        ],
        reverse=True,
    )[:top_k]

    relevant_experiences = [
        {
            "id": item["record"].id,
            "organization": (
                item["record"].organization
            ),
            "job_title": (
                item["record"].job_title
            ),
            "relevance_score": (
                item["relevance_score"]
            ),
            "description": shorten_text(
                item["record"].description
            ),
        }
        for item in sorted_experiences
    ]

    sorted_projects = sorted(
        project_items,
        key=lambda item: item[
            "relevance_score"
        ],
        reverse=True,
    )[:top_k]

    relevant_projects: list[dict] = []

    for item in sorted_projects:
        project = item["record"]

        project_skills = {
            canonicalize_skill_name(
                technology
            ).lower()
            for technology
            in (project.tech_stack or [])
        }

        matched_technologies = [
            skill_name
            for skill_name
            in recognized_job_skills
            if skill_name.lower()
            in project_skills
        ]

        relevant_projects.append(
            {
                "id": project.id,
                "title": project.title,
                "slug": project.slug,
                "relevance_score": (
                    item["relevance_score"]
                ),
                "matched_technologies": (
                    matched_technologies
                ),
            }
        )

    sorted_research = sorted(
        research_items,
        key=lambda item: item[
            "relevance_score"
        ],
        reverse=True,
    )[:top_k]

    relevant_research = [
        {
            "id": item["record"].id,
            "title": item["record"].title,
            "slug": item["record"].slug,
            "relevance_score": (
                item["relevance_score"]
            ),
            "models_used": (
                item["record"].models_used
                or []
            ),
        }
        for item in sorted_research
    ]

    (
        recommended_resume_type,
        recommendation_reason,
    ) = determine_resume_type(
        job_description,
        recognized_job_skills,
    )

    recommended_resume = (
        find_recommended_resume(
            portfolio_data["resumes"],
            recommended_resume_type,
        )
    )

    strengths = build_strengths(
        skill_score=skill_score,
        matched_skills=matched_skills,
        required_years=required_years,
        candidate_years=candidate_years,
        relevant_experiences=(
            relevant_experiences
        ),
        relevant_projects=relevant_projects,
        relevant_research=relevant_research,
    )

    improvement_areas = (
        build_improvement_areas(
            missing_skills=missing_skills,
            required_years=required_years,
            candidate_years=candidate_years,
            relevant_projects=relevant_projects,
        )
    )

    score_breakdown = {
        "skill_score": skill_score,
        "semantic_score": semantic_score,
        "experience_score": experience_score,
        "project_score": project_score,
        "research_score": research_score,
    }

    analysis = save_job_match_analysis(
        database_session=database_session,
        job_title=job_title,
        company_name=company_name,
        job_description=job_description,
        overall_score=overall_score,
        match_level=match_level,
        score_breakdown=score_breakdown,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        recommended_resume_type=(
            recommended_resume_type
        ),
        embedding_method=embedding_method,
    )

    explanation = (
        "The score combines technology overlap, "
        "semantic similarity with portfolio content, "
        "professional experience, relevant projects "
        "and research evidence. It is an explainable "
        "ranking score, not a hiring guarantee."
    )

    recommended_resume_response = None

    if recommended_resume is not None:
        recommended_resume_response = {
            "id": recommended_resume.id,
            "title": recommended_resume.title,
            "resume_type": (
                recommended_resume.resume_type
            ),
            "download_url": (
                recommended_resume.download_url
            ),
        }

    return {
        "analysis_id": analysis.id,
        "overall_match_score": overall_score,
        "match_level": match_level,
        "score_breakdown": score_breakdown,
        "recognized_job_skills": (
            recognized_job_skills
        ),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "required_experience_years": (
            required_years
        ),
        "candidate_experience_years": (
            candidate_years
        ),
        "relevant_experiences": (
            relevant_experiences
        ),
        "relevant_projects": relevant_projects,
        "relevant_research": relevant_research,
        "recommended_resume_type": (
            recommended_resume_type
        ),
        "recommended_resume": (
            recommended_resume_response
        ),
        "recommendation_reason": (
            recommendation_reason
        ),
        "strengths": strengths,
        "improvement_areas": (
            improvement_areas
        ),
        "explanation": explanation,
        "embedding_method": embedding_method,
    }


def list_job_match_analyses(
    database_session: Session,
    limit: int,
    offset: int,
) -> list[JobMatchAnalysis]:
    statement = (
        select(JobMatchAnalysis)
        .order_by(
            JobMatchAnalysis.created_at.desc()
        )
        .limit(limit)
        .offset(offset)
    )

    return list(
        database_session.scalars(
            statement
        ).all()
    )


def get_job_match_analysis_by_id(
    database_session: Session,
    analysis_id: int,
) -> JobMatchAnalysis | None:
    return database_session.get(
        JobMatchAnalysis,
        analysis_id,
    )


def delete_job_match_analysis(
    database_session: Session,
    analysis: JobMatchAnalysis,
) -> None:
    database_session.delete(analysis)
    database_session.commit()