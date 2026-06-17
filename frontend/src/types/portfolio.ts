export interface Profile {
  id: number;
  full_name: string;
  headline: string;
  short_bio: string;
  about_me: string;
  email: string;
  phone: string | null;
  location: string | null;
  profile_image_url: string | null;
  linkedin_url: string | null;
  github_url: string | null;
  leetcode_url: string | null;
  codechef_url: string | null;
  years_experience: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Education {
  id: number;
  institution: string;
  degree: string;
  field_of_study: string;
  start_date: string;
  end_date: string | null;
  grade: string | null;
  description: string | null;
  location: string | null;
  display_order: number;
  is_visible: boolean;
  created_at: string;
  updated_at: string;
}

export interface Experience {
  id: number;
  organization: string;
  job_title: string;
  employment_type: string | null;
  location: string | null;
  start_date: string;
  end_date: string | null;
  is_current: boolean;
  description: string | null;
  display_order: number;
  is_visible: boolean;
  created_at: string;
  updated_at: string;
}

export interface Skill {
  id: number;
  name: string;
  category: string;
  proficiency: number;
  icon_name: string | null;
  is_featured: boolean;
  display_order: number;
  is_visible: boolean;
  created_at: string;
  updated_at: string;
}

export interface Achievement {
  id: number;
  title: string;
  issuer: string | null;
  achievement_date: string | null;
  result: string | null;
  description: string | null;
  proof_url: string | null;
  display_order: number;
  is_visible: boolean;
  created_at: string;
  updated_at: string;
}

export interface Certification {
  id: number;
  name: string;
  issuer: string;
  issue_date: string | null;
  expiration_date: string | null;
  credential_id: string | null;
  credential_url: string | null;
  description: string | null;
  display_order: number;
  is_visible: boolean;
  created_at: string;
  updated_at: string;
}

export interface ProjectImage {
  id: number;
  project_id: number;
  image_url: string;
  alt_text: string;
  caption: string | null;
  display_order: number;
  created_at: string;
}

export interface Project {
  id: number;
  title: string;
  slug: string;
  category: string;
  short_description: string;
  description: string;
  tech_stack: string[];
  github_url: string | null;
  live_demo_url: string | null;
  challenges: string | null;
  solutions: string | null;
  results: string | null;
  view_count: number;
  is_featured: boolean;
  display_order: number;
  is_visible: boolean;
  images: ProjectImage[];
  created_at: string;
  updated_at: string;
}

export type MetricValue = string | number;

export interface ResearchPublication {
  id: number;
  title: string;
  slug: string;
  research_type: string;
  short_summary: string;
  abstract: string;
  dataset_details: string | null;
  methodology: string | null;
  models_used: string[];
  metrics: Record<string, MetricValue>;
  publication_status: string;
  publication_date: string | null;
  venue: string | null;
  paper_url: string | null;
  thesis_url: string | null;
  code_url: string | null;
  is_featured: boolean;
  display_order: number;
  is_visible: boolean;
  created_at: string;
  updated_at: string;
}

export interface Resume {
  id: number;
  title: string;
  resume_type: string;
  description: string | null;
  original_filename: string;
  mime_type: string;
  file_size_bytes: number;
  download_count: number;
  download_url: string;
  display_order: number;
  is_visible: boolean;
  created_at: string;
  updated_at: string;
}

export interface TopLanguage {
  language: string;
  repositories: number;
}

export interface GitHubProfile {
  id: number;
  github_user_id: number;
  username: string;
  name: string | null;
  bio: string | null;
  avatar_url: string;
  profile_url: string;
  company: string | null;
  location: string | null;
  blog_url: string | null;
  followers: number;
  following: number;
  public_repos: number;
  total_stars: number;
  total_forks: number;
  top_languages: TopLanguage[];
  github_created_at: string | null;
  github_updated_at: string | null;
  last_synced_at: string;
}

export interface GitHubRepository {
  id: number;
  github_repo_id: number;
  name: string;
  full_name: string;
  description: string | null;
  repository_url: string;
  homepage_url: string | null;
  language: string | null;
  topics: string[];
  stars_count: number;
  forks_count: number;
  open_issues_count: number;
  is_fork: boolean;
  is_archived: boolean;
  is_featured: boolean;
  is_visible: boolean;
  display_order: number;
  github_created_at: string | null;
  github_updated_at: string | null;
  github_pushed_at: string | null;
  last_synced_at: string;
}

export interface GitHubPortfolio {
  profile: GitHubProfile;
  repositories: GitHubRepository[];
}

export interface CodingProfile {
  id: number;
  platform: string;
  username: string | null;
  display_name: string;
  profile_url: string | null;
  total_solved: number | null;
  rating: number | null;
  max_rating: number | null;
  ranking: string | null;
  achievement_summary: string | null;
  statistics: Record<string, unknown>;
  display_order: number;
  is_visible: boolean;
  created_at: string;
  updated_at: string;
}

export interface PortfolioData {
  profile: Profile;
  education: Education[];
  experiences: Experience[];
  skills: Skill[];
  achievements: Achievement[];
  certifications: Certification[];
  projects: Project[];
  research: ResearchPublication[];
  resumes: Resume[];
  github: GitHubPortfolio | null;
  codingProfiles: CodingProfile[];
}

export interface ContactSubmission {
  id: number;
  status: string;
  message: string;
  created_at: string;
}