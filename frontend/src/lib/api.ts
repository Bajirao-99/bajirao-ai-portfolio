import type {
  Achievement,
  Certification,
  CodingProfile,
  ContactSubmission,
  Education,
  Experience,
  GitHubPortfolio,
  PortfolioData,
  Profile,
  Project,
  ResearchPublication,
  Resume,
  Skill,
} from "../types/portfolio";

import type {
  InterviewRequestPayload,
  InterviewRequestResponse,
  JobMatchRequest,
  JobMatchResponse,
  PortfolioChatRequest,
  PortfolioChatResponse,
} from "../types/ai";

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

// export interface JobMatchRequest {
//   job_description: string;
//   job_title: string | null;
//   company_name: string | null;
//   top_k: number;
// }

// export interface JobMatchResponse {
//   analysis_id: number;
//   overall_match_score: number;
//   match_level: string;
//   score_breakdown: ScoreBreakdown;
//   recognized_job_skills: string[];
//   matched_skills: string[];
//   missing_skills: string[];
//   required_experience_years: number | null;
//   candidate_experience_years: number;
//   relevant_experiences: RelevantExperience[];
//   relevant_projects: RelevantProject[];
//   relevant_research: RelevantResearch[];
//   recommended_resume_type: string;
//   recommended_resume: RecommendedResume | null;
//   recommendation_reason: string;
//   strengths: string[];
//   improvement_areas: string[];
//   explanation: string;
//   embedding_method: string;
// }

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

// export interface PortfolioChatRequest {
//   visitor_key: string;
//   question: string;
//   history: ChatHistoryMessage[];
//   top_k?: number;
// }

// export interface PortfolioChatResponse {
//   interaction_id: number;
//   answer: string;
//   grounded: boolean;
//   confidence_score: number;
//   sources: ChatSource[];
//   model_name: string;
//   retrieval_method: string;
//   disclaimer: string;
// }

// export interface InterviewRequestPayload {
//   name: string;
//   email: string;
//   phone: string | null;
//   company: string;
//   role: string;
//   preferred_datetime: string | null;
//   timezone: string | null;
//   meeting_mode: string | null;
//   message: string | null;
// }

// export interface InterviewRequestResponse {
//   id: number;
//   status: string;
//   message: string;
//   created_at: string;
// }
export const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL ??
  "http://127.0.0.1:8000"
).replace(/\/$/, "");

export class ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

export async function apiRequest<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const headers = new Headers(options.headers);

  if (
    options.body &&
    !(options.body instanceof FormData) &&
    !headers.has("Content-Type")
  ) {
    headers.set("Content-Type", "application/json");
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers,
  });

  if (response.status === 204) {
    return undefined as T;
  }

  if (!response.ok) {
    const payload = await response
      .json()
      .catch(() => null);

    let message = `Request failed with status ${response.status}.`;

    if (
      payload &&
      typeof payload === "object" &&
      "detail" in payload
    ) {
      const detail = payload.detail;

      if (typeof detail === "string") {
        message = detail;
      }
    }

    throw new ApiError(message, response.status);
  }

  return response.json() as Promise<T>;
}

export function resolveApiUrl(
  value: string | null | undefined,
): string | null {
  if (!value) {
    return null;
  }

  if (
    value.startsWith("http://") ||
    value.startsWith("https://")
  ) {
    return value;
  }

  return `${API_BASE_URL}${
    value.startsWith("/") ? value : `/${value}`
  }`;
}

async function getGitHubPortfolio(
  signal?: AbortSignal,
): Promise<GitHubPortfolio | null> {
  try {
    return await apiRequest<GitHubPortfolio>(
      "/api/v1/integrations/github",
      { signal },
    );
  } catch (error) {
    if (
      error instanceof ApiError &&
      error.status === 404
    ) {
      return null;
    }

    throw error;
  }
}

async function getPortfolio(
  signal?: AbortSignal,
): Promise<PortfolioData> {
  const [
    profile,
    education,
    experiences,
    skills,
    achievements,
    certifications,
    projects,
    research,
    resumes,
    github,
    codingProfiles,
  ] = await Promise.all([
    apiRequest<Profile>(
      "/api/v1/profile",
      { signal },
    ),
    apiRequest<Education[]>(
      "/api/v1/education",
      { signal },
    ),
    apiRequest<Experience[]>(
      "/api/v1/experiences",
      { signal },
    ),
    apiRequest<Skill[]>(
      "/api/v1/skills",
      { signal },
    ),
    apiRequest<Achievement[]>(
      "/api/v1/achievements",
      { signal },
    ),
    apiRequest<Certification[]>(
      "/api/v1/certifications",
      { signal },
    ),
    apiRequest<Project[]>(
      "/api/v1/projects",
      { signal },
    ),
    apiRequest<ResearchPublication[]>(
      "/api/v1/research",
      { signal },
    ),
    apiRequest<Resume[]>(
      "/api/v1/resumes",
      { signal },
    ),
    getGitHubPortfolio(signal),
    apiRequest<CodingProfile[]>(
      "/api/v1/coding-profiles",
      { signal },
    ),
  ]);

  return {
    profile,
    education,
    experiences,
    skills,
    achievements,
    certifications,
    projects,
    research,
    resumes,
    github,
    codingProfiles,
  };
}

export const publicApi = {
  getPortfolio,

  getProject(
    slug: string,
    signal?: AbortSignal,
  ) {
    return apiRequest<Project>(
      `/api/v1/projects/slug/${encodeURIComponent(slug)}`,
      { signal },
    );
  },

  getResearch(
    slug: string,
    signal?: AbortSignal,
  ) {
    return apiRequest<ResearchPublication>(
      `/api/v1/research/slug/${encodeURIComponent(slug)}`,
      { signal },
    );
  },

  trackPageView(data: {
    visitor_key: string;
    page_path: string;
    referrer: string | null;
  }) {
    return apiRequest(
      "/api/v1/analytics/page-view",
      {
        method: "POST",
        body: JSON.stringify(data),
      },
    );
  },

  trackProjectView(slug: string) {
    return apiRequest(
      `/api/v1/analytics/projects/${encodeURIComponent(slug)}/view`,
      {
        method: "POST",
      },
    );
  },

  submitContact(data: {
    name: string;
    email: string;
    phone: string | null;
    subject: string;
    message: string;
  }) {
    return apiRequest<ContactSubmission>(
      "/api/v1/contact",
      {
        method: "POST",
        body: JSON.stringify(data),
      },
    );
  },

    matchJobDescription(
    data: JobMatchRequest,
  ) {
    return apiRequest<JobMatchResponse>(
      "/api/v1/ai/job-match",
      {
        method: "POST",
        body: JSON.stringify(data),
      },
    );
  },

  getChatSuggestions() {
    return apiRequest<string[]>(
      "/api/v1/ai/chat/suggestions",
    );
  },

  askPortfolioChatbot(
    data: PortfolioChatRequest,
  ) {
    return apiRequest<PortfolioChatResponse>(
      "/api/v1/ai/chat",
      {
        method: "POST",
        body: JSON.stringify(data),
      },
    );
  },

  submitInterviewRequest(
    data: InterviewRequestPayload,
  ) {
    return apiRequest<InterviewRequestResponse>(
      "/api/v1/interview-requests",
      {
        method: "POST",
        body: JSON.stringify(data),
      },
    );
  },
};