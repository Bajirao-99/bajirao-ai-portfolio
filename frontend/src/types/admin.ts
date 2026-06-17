import type {
  ChatSource,
} from "./ai";

export interface AdminTokenResponse {
  access_token: string;
  token_type: "bearer";
  expires_in: number;
}

export interface AdminUser {
  id: number;
  username: string;
  email: string;
  is_active: boolean;
  is_superuser: boolean;
  last_login: string | null;
  created_at: string;
}

export interface AnalyticsSummary {
  total_unique_visitors: number;
  total_page_views: number;
  period_page_views: number;
  total_project_views: number;
  total_resume_downloads: number;
  total_contact_messages: number;
  new_contact_messages: number;
  total_interview_requests: number;
  pending_interview_requests: number;
  total_job_match_analyses: number;
  total_chat_interactions: number;
}

export interface TopPageStat {
  page_path: string;
  views: number;
}

export interface TopProjectStat {
  id: number;
  title: string;
  slug: string;
  view_count: number;
}

export interface ResumeDownloadStat {
  id: number;
  title: string;
  resume_type: string;
  download_count: number;
}

export interface DailyPageViewStat {
  view_date: string;
  views: number;
}

export interface AnalyticsDashboard {
  period_days: number;
  summary: AnalyticsSummary;
  top_pages: TopPageStat[];
  top_projects: TopProjectStat[];
  resume_downloads: ResumeDownloadStat[];
  daily_page_views: DailyPageViewStat[];
}

export interface ContactMessageAdmin {
  id: number;
  name: string;
  email: string;
  phone: string | null;
  subject: string;
  message: string;
  status: string;
  admin_notes: string | null;
  created_at: string;
  updated_at: string;
}

export interface InterviewRequestAdmin {
  id: number;
  name: string;
  email: string;
  phone: string | null;
  company: string;
  role: string;
  preferred_datetime: string | null;
  timezone: string | null;
  meeting_mode: string | null;
  message: string | null;
  status: string;
  admin_notes: string | null;
  created_at: string;
  updated_at: string;
}

export interface JobMatchHistory {
  id: number;
  job_title: string | null;
  company_name: string | null;
  overall_match_score: number;
  match_level: string;
  score_breakdown: Record<string, number>;
  matched_skills: string[];
  missing_skills: string[];
  recommended_resume_type: string;
  embedding_method: string;
  created_at: string;
}

export interface ChatInteractionHistory {
  id: number;
  visitor_key: string;
  question: string;
  answer: string;
  source_refs: ChatSource[];
  confidence_score: number;
  grounded: boolean;
  model_name: string;
  retrieval_method: string;
  created_at: string;
}