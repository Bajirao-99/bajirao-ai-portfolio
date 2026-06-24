export interface ScoreBreakdown {
  skill_score: number;
  semantic_score: number;
  experience_score: number;
  project_score: number;
  research_score: number;
}

export interface RelevantExperience {
  id: number;
  organization: string;
  job_title: string;
  relevance_score: number;
  description: string | null;
}

export interface RelevantProject {
  id: number;
  title: string;
  slug: string;
  relevance_score: number;
  matched_technologies: string[];
}

export interface RelevantResearch {
  id: number;
  title: string;
  slug: string;
  relevance_score: number;
  models_used: string[];
}

export interface RecommendedResume {
  id: number;
  title: string;
  resume_type: string;
  download_url: string;
}

export interface JobMatchRequest {
  job_description: string;
  job_title: string | null;
  company_name: string | null;
  top_k: number;
}

export interface JobMatchResponse {
  analysis_id: number;
  overall_match_score: number;
  match_level: string;
  score_breakdown: ScoreBreakdown;
  recognized_job_skills: string[];
  matched_skills: string[];
  missing_skills: string[];
  required_experience_years: number | null;
  candidate_experience_years: number;
  relevant_experiences: RelevantExperience[];
  relevant_projects: RelevantProject[];
  relevant_research: RelevantResearch[];
  recommended_resume_type: string;
  recommended_resume: RecommendedResume | null;
  recommendation_reason: string;
  strengths: string[];
  improvement_areas: string[];
  explanation: string;
  embedding_method: string;
}

export interface ChatHistoryMessage {
  role: "user" | "assistant";
  content: string;
}

export interface ChatSource {
  source_type: string;
  source_id: number | null;
  title: string;
  url: string | null;
  relevance_score: number;
}

export interface PortfolioChatRequest {
  visitor_key: string;
  question: string;
  history: ChatHistoryMessage[];
  top_k?: number;
}

export interface PortfolioChatResponse {
  interaction_id: number;
  answer: string;
  grounded: boolean;
  confidence_score: number;
  sources: ChatSource[];
  model_name: string;
  retrieval_method: string;
  answer_mode: "portfolio" | "general" | "mixed";
  disclaimer: string;
}

export interface InterviewRequestPayload {
  name: string;
  email: string;
  phone: string | null;
  company: string;
  role: string;
  preferred_datetime: string | null;
  timezone: string | null;
  meeting_mode: string | null;
  message: string | null;
}

export interface InterviewRequestResponse {
  id: number;
  status: string;
  message: string;
  created_at: string;
}