from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class JobMatchRequest(BaseModel):
    job_description: str = Field(
        min_length=100,
        max_length=30000,
    )

    job_title: str | None = Field(
        default=None,
        max_length=250,
    )

    company_name: str | None = Field(
        default=None,
        max_length=250,
    )

    top_k: int = Field(
        default=3,
        ge=1,
        le=5,
    )


class ScoreBreakdown(BaseModel):
    skill_score: float
    semantic_score: float
    experience_score: float
    project_score: float
    research_score: float


class RelevantExperienceResponse(BaseModel):
    id: int
    organization: str
    job_title: str
    relevance_score: float
    description: str | None


class RelevantProjectResponse(BaseModel):
    id: int
    title: str
    slug: str
    relevance_score: float
    matched_technologies: list[str]


class RelevantResearchResponse(BaseModel):
    id: int
    title: str
    slug: str
    relevance_score: float
    models_used: list[str]


class RecommendedResumeResponse(BaseModel):
    id: int
    title: str
    resume_type: str
    download_url: str


class JobMatchResponse(BaseModel):
    analysis_id: int

    overall_match_score: float
    match_level: str

    score_breakdown: ScoreBreakdown

    recognized_job_skills: list[str]
    matched_skills: list[str]
    missing_skills: list[str]

    required_experience_years: float | None
    candidate_experience_years: float

    relevant_experiences: list[
        RelevantExperienceResponse
    ]

    relevant_projects: list[
        RelevantProjectResponse
    ]

    relevant_research: list[
        RelevantResearchResponse
    ]

    recommended_resume_type: str

    recommended_resume: (
        RecommendedResumeResponse | None
    )

    recommendation_reason: str

    strengths: list[str]
    improvement_areas: list[str]

    explanation: str
    embedding_method: str


class JobMatchHistoryResponse(BaseModel):
    id: int
    job_title: str | None
    company_name: str | None
    overall_match_score: float
    match_level: str
    score_breakdown: dict[str, float]
    matched_skills: list[str]
    missing_skills: list[str]
    recommended_resume_type: str
    embedding_method: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )