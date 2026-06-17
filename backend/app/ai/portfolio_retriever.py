import re
from collections import defaultdict
from dataclasses import dataclass
from statistics import mean

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ai.semantic_engine import (
    calculate_semantic_similarity,
)
from app.core.config import settings
from app.models.achievement import Achievement
from app.models.certification import Certification
from app.models.coding_profile import CodingProfile
from app.models.education import Education
from app.models.experience import Experience
from app.models.github import (
    GitHubProfile,
    GitHubRepository,
)
from app.models.profile import Profile
from app.models.project import Project
from app.models.research import ResearchPublication
from app.models.resume import Resume
from app.models.skill import Skill


STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "for",
    "from",
    "he",
    "his",
    "how",
    "in",
    "is",
    "it",
    "me",
    "of",
    "on",
    "the",
    "to",
    "what",
    "which",
    "who",
    "with",
}


@dataclass
class KnowledgeChunk:
    source_type: str
    source_id: int | None
    title: str
    text: str
    url: str | None


def join_text(*values: object) -> str:
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

        if isinstance(value, dict):
            parts.extend(
                f"{key}: {item}"
                for key, item in value.items()
            )
            continue

        parts.append(str(value))

    return " ".join(parts)


def build_portfolio_knowledge(
    database_session: Session,
) -> list[KnowledgeChunk]:
    chunks: list[KnowledgeChunk] = []

    profile = database_session.scalar(
        select(Profile)
        .where(Profile.is_active.is_(True))
        .order_by(Profile.id.asc())
    )

    if profile is not None:
        chunks.append(
            KnowledgeChunk(
                source_type="profile",
                source_id=profile.id,
                title="Professional Profile",
                text=join_text(
                    profile.full_name,
                    profile.headline,
                    profile.short_bio,
                    profile.about_me,
                    f"Years of experience: "
                    f"{profile.years_experience}",
                    profile.location,
                ),
                url="/",
            )
        )

    education_records = list(
        database_session.scalars(
            select(Education)
            .where(Education.is_visible.is_(True))
            .order_by(
                Education.display_order.asc(),
                Education.id.asc(),
            )
        ).all()
    )

    for record in education_records:
        chunks.append(
            KnowledgeChunk(
                source_type="education",
                source_id=record.id,
                title=(
                    f"{record.degree} — "
                    f"{record.institution}"
                ),
                text=join_text(
                    record.degree,
                    record.field_of_study,
                    record.institution,
                    record.grade,
                    record.description,
                    record.location,
                    f"Start date: {record.start_date}",
                    f"End date: {record.end_date}",
                ),
                url="/#education",
            )
        )

    experiences = list(
        database_session.scalars(
            select(Experience)
            .where(Experience.is_visible.is_(True))
            .order_by(
                Experience.display_order.asc(),
                Experience.id.asc(),
            )
        ).all()
    )

    for record in experiences:
        chunks.append(
            KnowledgeChunk(
                source_type="experience",
                source_id=record.id,
                title=(
                    f"{record.job_title} — "
                    f"{record.organization}"
                ),
                text=join_text(
                    record.job_title,
                    record.organization,
                    record.employment_type,
                    record.description,
                    record.location,
                    f"Start date: {record.start_date}",
                    f"End date: {record.end_date}",
                    f"Current position: "
                    f"{record.is_current}",
                ),
                url="/#experience",
            )
        )

    skills = list(
        database_session.scalars(
            select(Skill)
            .where(Skill.is_visible.is_(True))
            .order_by(
                Skill.category.asc(),
                Skill.display_order.asc(),
                Skill.id.asc(),
            )
        ).all()
    )

    skills_by_category: dict[
        str,
        list[Skill],
    ] = defaultdict(list)

    for skill in skills:
        skills_by_category[
            skill.category
        ].append(skill)

    for category, category_skills in (
        skills_by_category.items()
    ):
        skill_descriptions = [
            (
                f"{skill.name} "
                f"(proficiency {skill.proficiency}/100, "
                f"featured: {skill.is_featured})"
            )
            for skill in category_skills
        ]

        chunks.append(
            KnowledgeChunk(
                source_type="skills",
                source_id=None,
                title=f"Skills — {category}",
                text=join_text(
                    category,
                    skill_descriptions,
                ),
                url="/#skills",
            )
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

    for project in projects:
        chunks.append(
            KnowledgeChunk(
                source_type="project",
                source_id=project.id,
                title=project.title,
                text=join_text(
                    project.title,
                    project.category,
                    project.short_description,
                    project.description,
                    project.tech_stack,
                    project.challenges,
                    project.solutions,
                    project.results,
                ),
                url=f"/projects/{project.slug}",
            )
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

    for research in research_records:
        chunks.append(
            KnowledgeChunk(
                source_type="research",
                source_id=research.id,
                title=research.title,
                text=join_text(
                    research.title,
                    research.research_type,
                    research.short_summary,
                    research.abstract,
                    research.dataset_details,
                    research.methodology,
                    research.models_used,
                    research.metrics,
                    research.publication_status,
                    research.venue,
                ),
                url=f"/research/{research.slug}",
            )
        )

    achievements = list(
        database_session.scalars(
            select(Achievement)
            .where(
                Achievement.is_visible.is_(True)
            )
            .order_by(
                Achievement.display_order.asc(),
                Achievement.id.asc(),
            )
        ).all()
    )

    for achievement in achievements:
        chunks.append(
            KnowledgeChunk(
                source_type="achievement",
                source_id=achievement.id,
                title=achievement.title,
                text=join_text(
                    achievement.title,
                    achievement.issuer,
                    achievement.result,
                    achievement.description,
                    achievement.achievement_date,
                ),
                url="/#achievements",
            )
        )

    certifications = list(
        database_session.scalars(
            select(Certification)
            .where(
                Certification.is_visible.is_(True)
            )
            .order_by(
                Certification.display_order.asc(),
                Certification.id.asc(),
            )
        ).all()
    )

    for certification in certifications:
        chunks.append(
            KnowledgeChunk(
                source_type="certification",
                source_id=certification.id,
                title=certification.name,
                text=join_text(
                    certification.name,
                    certification.issuer,
                    certification.description,
                    certification.issue_date,
                    certification.expiration_date,
                    certification.credential_id,
                ),
                url="/#certifications",
            )
        )

    coding_profiles = list(
        database_session.scalars(
            select(CodingProfile)
            .where(
                CodingProfile.is_visible.is_(True)
            )
            .order_by(
                CodingProfile.display_order.asc(),
                CodingProfile.id.asc(),
            )
        ).all()
    )

    for coding_profile in coding_profiles:
        chunks.append(
            KnowledgeChunk(
                source_type="coding-profile",
                source_id=coding_profile.id,
                title=coding_profile.display_name,
                text=join_text(
                    coding_profile.platform,
                    coding_profile.username,
                    coding_profile.total_solved,
                    coding_profile.rating,
                    coding_profile.max_rating,
                    coding_profile.ranking,
                    coding_profile.achievement_summary,
                    coding_profile.statistics,
                ),
                url=coding_profile.profile_url,
            )
        )

    github_profile = database_session.scalar(
        select(GitHubProfile)
        .order_by(GitHubProfile.id.asc())
    )

    if github_profile is not None:
        chunks.append(
            KnowledgeChunk(
                source_type="github-profile",
                source_id=github_profile.id,
                title="GitHub Profile",
                text=join_text(
                    github_profile.username,
                    github_profile.name,
                    github_profile.bio,
                    f"Public repositories: "
                    f"{github_profile.public_repos}",
                    f"Total stars: "
                    f"{github_profile.total_stars}",
                    f"Total forks: "
                    f"{github_profile.total_forks}",
                    github_profile.top_languages,
                ),
                url=github_profile.profile_url,
            )
        )

    github_repositories = list(
        database_session.scalars(
            select(GitHubRepository)
            .where(
                GitHubRepository.is_visible.is_(True)
            )
            .order_by(
                GitHubRepository.is_featured.desc(),
                GitHubRepository.stars_count.desc(),
                GitHubRepository.id.asc(),
            )
            .limit(20)
        ).all()
    )

    for repository in github_repositories:
        chunks.append(
            KnowledgeChunk(
                source_type="github-repository",
                source_id=repository.id,
                title=repository.name,
                text=join_text(
                    repository.name,
                    repository.description,
                    repository.language,
                    repository.topics,
                    f"Stars: {repository.stars_count}",
                    f"Forks: {repository.forks_count}",
                ),
                url=repository.repository_url,
            )
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

    for resume in resumes:
        chunks.append(
            KnowledgeChunk(
                source_type="resume",
                source_id=resume.id,
                title=resume.title,
                text=join_text(
                    resume.title,
                    resume.resume_type,
                    resume.description,
                ),
                url=resume.download_url,
            )
        )

    return chunks


def tokenize(value: str) -> set[str]:
    tokens = re.findall(
        r"[a-z0-9+#.]+",
        value.lower(),
    )

    return {
        token
        for token in tokens
        if (
            token not in STOP_WORDS
            and len(token) > 1
        )
    }


def lexical_similarity(
    question: str,
    document: str,
) -> float:
    question_tokens = tokenize(question)
    document_tokens = tokenize(document)

    if not question_tokens:
        return 0.0

    overlap = question_tokens.intersection(
        document_tokens
    )

    return len(overlap) / len(
        question_tokens
    )


def retrieve_portfolio_context(
    database_session: Session,
    question: str,
    top_k: int | None = None,
) -> tuple[list[dict], str, float]:
    chunks = build_portfolio_knowledge(
        database_session
    )

    if not chunks:
        return [], "no-portfolio-data", 0.0

    semantic_scores, retrieval_method = (
        calculate_semantic_similarity(
            question,
            [
                chunk.text
                for chunk in chunks
            ],
        )
    )

    ranked_chunks: list[dict] = []

    for chunk, semantic_score in zip(
        chunks,
        semantic_scores,
        strict=False,
    ):
        lexical_score = lexical_similarity(
            question,
            chunk.text,
        )

        combined_score = (
            semantic_score * 0.85
            + lexical_score * 0.15
        )

        ranked_chunks.append(
            {
                "chunk": chunk,
                "score": combined_score,
            }
        )

    ranked_chunks.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    result_limit = (
        top_k
        or settings.chat_retrieval_top_k
    )

    selected_chunks = [
        item
        for item in ranked_chunks
        if (
            item["score"]
            >= settings.chat_min_relevance_score
        )
    ][:result_limit]

    if not selected_chunks:
        return [], retrieval_method, 0.0

    source_results = [
        {
            "source_type": (
                item["chunk"].source_type
            ),
            "source_id": (
                item["chunk"].source_id
            ),
            "title": item["chunk"].title,
            "url": item["chunk"].url,
            "relevance_score": round(
                item["score"] * 100,
                2,
            ),
            "content": item["chunk"].text,
        }
        for item in selected_chunks
    ]

    confidence_score = round(
        mean(
            item["score"]
            for item in selected_chunks[:3]
        )
        * 100,
        2,
    )

    return (
        source_results,
        retrieval_method,
        confidence_score,
    )