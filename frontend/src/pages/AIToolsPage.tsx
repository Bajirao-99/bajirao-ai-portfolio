import {
  ArrowRight,
  BriefcaseBusiness,
  CheckCircle2,
  Download,
  FileSearch,
  FlaskConical,
  Lightbulb,
  LoaderCircle,
  Search,
  Sparkles,
  Target,
  TriangleAlert,
  UserRoundSearch,
} from "lucide-react";
import {
  type FormEvent,
  useState,
} from "react";
import { Link } from "react-router";

import InterviewRequestForm from "../components/InterviewRequestForm";
import {
  publicApi,
  resolveApiUrl,
} from "../lib/api";
import type {
  JobMatchResponse,
} from "../types/ai";

const sampleJobDescription = `We are seeking a Python Backend Developer with at least 2 years of software development experience. The candidate should have strong knowledge of Python, FastAPI or Django, REST APIs, PostgreSQL, SQL, Git and Linux. The role involves designing scalable backend services, developing API endpoints, working with relational databases and collaborating with frontend developers. Experience with Docker, AWS, microservices, unit testing and CI/CD is preferred. Knowledge of data structures, algorithms, object-oriented programming and system design is expected. Exposure to machine learning or natural language processing will be considered an advantage.`;

function formatScore(
  value: number,
): string {
  return `${Math.round(value)}%`;
}

function ScoreBar({
  label,
  score,
}: {
  label: string;
  score: number;
}) {
  return (
    <div className="score-bar-item">
      <div>
        <span>{label}</span>
        <strong>
          {formatScore(score)}
        </strong>
      </div>

      <div className="score-bar-track">
        <span
          style={{
            width: `${Math.max(
              0,
              Math.min(100, score),
            )}%`,
          }}
        />
      </div>
    </div>
  );
}

export default function AIToolsPage() {
  const [jobTitle, setJobTitle] =
    useState("");

  const [companyName, setCompanyName] =
    useState("");

  const [
    jobDescription,
    setJobDescription,
  ] = useState("");

  const [topK, setTopK] =
    useState(3);

  const [result, setResult] =
    useState<JobMatchResponse | null>(
      null,
    );

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);

  async function handleJobMatch(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response =
        await publicApi.matchJobDescription({
          job_title:
            jobTitle.trim() || null,
          company_name:
            companyName.trim() || null,
          job_description:
            jobDescription.trim(),
          top_k: topK,
        });

      setResult(response);

      window.setTimeout(() => {
        document
          .getElementById(
            "job-match-result",
          )
          ?.scrollIntoView({
            behavior: "smooth",
            block: "start",
          });
      }, 100);
    } catch (matchError) {
      setError(
        matchError instanceof Error
          ? matchError.message
          : "Could not analyze the job description.",
      );
    } finally {
      setLoading(false);
    }
  }

  const resumeDownloadUrl =
    result?.recommended_resume
      ? resolveApiUrl(
          result.recommended_resume
            .download_url,
        )
      : null;

  return (
    <div className="ai-tools-page">
      <section className="ai-tools-hero">
        <div className="container">
          <span className="hero-badge">
            <Sparkles size={16} />
            AI-powered portfolio tools
          </span>

          <h1>
            Evaluate role fit using portfolio
            evidence
          </h1>

          <p>
            Paste a job description to calculate
            an explainable match score, identify
            skill gaps, rank relevant experience,
            find supporting projects and select
            the best resume version.
          </p>

          <div className="ai-tools-features">
            <span>
              <Target size={18} />
              Explainable match score
            </span>

            <span>
              <FileSearch size={18} />
              Skills and evidence
            </span>

            <span>
              <Download size={18} />
              Resume recommendation
            </span>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="container ai-tools-layout">
          <form
            className="ai-form job-match-form"
            onSubmit={handleJobMatch}
          >
            <div className="ai-form-heading">
              <span className="ai-form-icon">
                <UserRoundSearch
                  size={25}
                />
              </span>

              <div>
                <h2>
                  Job Description Matcher
                </h2>

                <p>
                  The score uses technology
                  overlap, semantic similarity,
                  experience, projects and
                  research.
                </p>
              </div>
            </div>

            <div className="ai-form-grid">
              <label>
                Job Title
                <input
                  maxLength={250}
                  value={jobTitle}
                  onChange={(event) => {
                    setJobTitle(
                      event.target.value,
                    );
                  }}
                  placeholder="Python Backend Developer"
                />
              </label>

              <label>
                Company Name
                <input
                  maxLength={250}
                  value={companyName}
                  onChange={(event) => {
                    setCompanyName(
                      event.target.value,
                    );
                  }}
                  placeholder="Company name"
                />
              </label>
            </div>

            <label>
              Job Description
              <textarea
                required
                minLength={100}
                maxLength={30000}
                rows={14}
                value={jobDescription}
                onChange={(event) => {
                  setJobDescription(
                    event.target.value,
                  );
                }}
                placeholder="Paste the complete job description here..."
              />
            </label>

            <div className="job-match-options">
              <label>
                Evidence Results
                <select
                  value={topK}
                  onChange={(event) => {
                    setTopK(
                      Number(
                        event.target.value,
                      ),
                    );
                  }}
                >
                  <option value={1}>
                    Top 1
                  </option>

                  <option value={2}>
                    Top 2
                  </option>

                  <option value={3}>
                    Top 3
                  </option>

                  <option value={4}>
                    Top 4
                  </option>

                  <option value={5}>
                    Top 5
                  </option>
                </select>
              </label>

              <button
                type="button"
                className="button button-secondary"
                onClick={() => {
                  setJobTitle(
                    "Python Backend Developer",
                  );

                  setCompanyName(
                    "Example Technologies",
                  );

                  setJobDescription(
                    sampleJobDescription,
                  );
                }}
              >
                Use Sample JD
              </button>
            </div>

            {error && (
              <div 
                className="ai-form-message ai-form-error"
                role="alert"
                >
                  <TriangleAlert size={18} />
                  {error}
              </div>
            )}

            <button
              type="submit"
              className="button button-primary button-full"
              disabled={loading}
            >
              {loading ? (
                <>
                  <LoaderCircle
                    className="spin"
                    size={18}
                  />
                  Analyzing Portfolio Match
                </>
              ) : (
                <>
                  <Search size={18} />
                  Analyze Job Description
                </>
              )}
            </button>
          </form>

          <aside className="ai-information-card">
            <Sparkles size={28} />

            <h3>
              How the analysis works
            </h3>

            <div className="ai-information-list">
              <div>
                <strong>1</strong>

                <p>
                  Extract technologies and
                  requirements from the job
                  description.
                </p>
              </div>

              <div>
                <strong>2</strong>

                <p>
                  Compare requirements with
                  skills, experience, projects
                  and research.
                </p>
              </div>

              <div>
                <strong>3</strong>

                <p>
                  Rank supporting portfolio
                  evidence using semantic
                  similarity.
                </p>
              </div>

              <div>
                <strong>4</strong>

                <p>
                  Recommend the most relevant
                  resume version.
                </p>
              </div>
            </div>

            <p className="ai-disclaimer">
              The score is an explainable
              portfolio-fit score. It is not a
              hiring guarantee.
            </p>
          </aside>
        </div>
      </section>

      {result && (
        <section
          className="section section-muted"
          id="job-match-result"
        >
          <div className="container">
            <div className="job-result-heading">
              <div>
                <span className="eyebrow">
                  Analysis Complete
                </span>

                <h2>
                  Portfolio Match Results
                </h2>

                <p>
                  {result.explanation}
                </p>
              </div>

              <div
                className="overall-score-ring"
                style={{
                  background: `conic-gradient(
                    var(--primary)
                    ${Math.max(
                      0,
                      Math.min(
                        100,
                        result.overall_match_score,
                      ),
                    ) * 3.6}deg,
                    #e8e1dc 0deg
                  )`,
                }}
              >
                <div>
                  <strong>
                    {formatScore(
                      result.overall_match_score,
                    )}
                  </strong>

                  <span>
                    {result.match_level}
                  </span>
                </div>
              </div>
            </div>

            <div className="score-breakdown-grid">
              <ScoreBar
                label="Skill Match"
                score={
                  result.score_breakdown
                    .skill_score
                }
              />

              <ScoreBar
                label="Semantic Match"
                score={
                  result.score_breakdown
                    .semantic_score
                }
              />

              <ScoreBar
                label="Experience"
                score={
                  result.score_breakdown
                    .experience_score
                }
              />

              <ScoreBar
                label="Projects"
                score={
                  result.score_breakdown
                    .project_score
                }
              />

              <ScoreBar
                label="Research"
                score={
                  result.score_breakdown
                    .research_score
                }
              />
            </div>

            <div className="experience-summary-grid">
              <article>
                <span>
                  Required Experience
                </span>

                <strong>
                  {result.required_experience_years ===
                  null
                    ? "Not specified"
                    : `${result.required_experience_years} years`}
                </strong>
              </article>

              <article>
                <span>
                  Portfolio Experience
                </span>

                <strong>
                  {
                    result.candidate_experience_years
                  }{" "}
                  years
                </strong>
              </article>

              <article>
                <span>
                  Skills Recognized
                </span>

                <strong>
                  {
                    result.recognized_job_skills
                      .length
                  }
                </strong>
              </article>

              <article>
                <span>
                  Skills Matched
                </span>

                <strong>
                  {
                    result.matched_skills
                      .length
                  }
                </strong>
              </article>
            </div>

            <div className="skill-result-grid">
              <article className="result-card">
                <div className="result-card-title result-title-success">
                  <CheckCircle2 size={21} />
                  <h3>Matched Skills</h3>
                </div>

                <div className="result-chip-list">
                  {result.matched_skills
                    .length > 0 ? (
                    result.matched_skills.map(
                      (skill) => (
                        <span
                          className="result-chip result-chip-success"
                          key={skill}
                        >
                          {skill}
                        </span>
                      ),
                    )
                  ) : (
                    <p>
                      No directly matched skills
                      were identified.
                    </p>
                  )}
                </div>
              </article>

              <article className="result-card">
                <div className="result-card-title result-title-warning">
                  <TriangleAlert
                    size={21}
                  />
                  <h3>Missing Skills</h3>
                </div>

                <div className="result-chip-list">
                  {result.missing_skills
                    .length > 0 ? (
                    result.missing_skills.map(
                      (skill) => (
                        <span
                          className="result-chip result-chip-warning"
                          key={skill}
                        >
                          {skill}
                        </span>
                      ),
                    )
                  ) : (
                    <p>
                      No missing recognized
                      skills were detected.
                    </p>
                  )}
                </div>
              </article>
            </div>

            <div className="strength-grid">
              <article className="result-card">
                <div className="result-card-title">
                  <Target size={21} />
                  <h3>Strengths</h3>
                </div>

                <ul className="result-list">
                  {result.strengths.map(
                    (strength) => (
                      <li key={strength}>
                        {strength}
                      </li>
                    ),
                  )}
                </ul>
              </article>

              <article className="result-card">
                <div className="result-card-title">
                  <Lightbulb size={21} />
                  <h3>
                    Improvement Areas
                  </h3>
                </div>

                <ul className="result-list">
                  {result.improvement_areas.map(
                    (area) => (
                      <li key={area}>
                        {area}
                      </li>
                    ),
                  )}
                </ul>
              </article>
            </div>

            <div className="evidence-section">
              <div className="evidence-heading">
                <BriefcaseBusiness
                  size={23}
                />

                <div>
                  <h3>
                    Relevant Experience
                  </h3>

                  <p>
                    Professional experience
                    ranked by similarity to the
                    role.
                  </p>
                </div>
              </div>

              <div className="evidence-grid">
                {result.relevant_experiences.map(
                  (experience) => (
                    <article
                      className="evidence-card"
                      key={experience.id}
                    >
                      <span className="evidence-score">
                        {formatScore(
                          experience.relevance_score,
                        )}
                      </span>

                      <h4>
                        {
                          experience.job_title
                        }
                      </h4>

                      <strong>
                        {
                          experience.organization
                        }
                      </strong>

                      {experience.description && (
                        <p>
                          {
                            experience.description
                          }
                        </p>
                      )}
                    </article>
                  ),
                )}
              </div>
            </div>

            <div className="evidence-section">
              <div className="evidence-heading">
                <FileSearch size={23} />

                <div>
                  <h3>Relevant Projects</h3>

                  <p>
                    Projects demonstrating
                    applicable technologies and
                    responsibilities.
                  </p>
                </div>
              </div>

              <div className="evidence-grid">
                {result.relevant_projects.map(
                  (project) => (
                    <article
                      className="evidence-card"
                      key={project.id}
                    >
                      <span className="evidence-score">
                        {formatScore(
                          project.relevance_score,
                        )}
                      </span>

                      <h4>{project.title}</h4>

                      <div className="result-chip-list">
                        {project.matched_technologies.map(
                          (technology) => (
                            <span
                              className="result-chip result-chip-neutral"
                              key={technology}
                            >
                              {technology}
                            </span>
                          ),
                        )}
                      </div>

                      <Link
                        className="text-link"
                        to={`/projects/${project.slug}`}
                      >
                        View project
                        <ArrowRight
                          size={16}
                        />
                      </Link>
                    </article>
                  ),
                )}
              </div>
            </div>

            {result.relevant_research.length >
              0 && (
              <div className="evidence-section">
                <div className="evidence-heading">
                  <FlaskConical
                    size={23}
                  />

                  <div>
                    <h3>
                      Relevant Research
                    </h3>

                    <p>
                      Research evidence related
                      to the job description.
                    </p>
                  </div>
                </div>

                <div className="evidence-grid">
                  {result.relevant_research.map(
                    (research) => (
                      <article
                        className="evidence-card"
                        key={research.id}
                      >
                        <span className="evidence-score">
                          {formatScore(
                            research.relevance_score,
                          )}
                        </span>

                        <h4>
                          {research.title}
                        </h4>

                        <div className="result-chip-list">
                          {research.models_used.map(
                            (model) => (
                              <span
                                className="result-chip result-chip-neutral"
                                key={model}
                              >
                                {model}
                              </span>
                            ),
                          )}
                        </div>

                        <Link
                          className="text-link"
                          to={`/research/${research.slug}`}
                        >
                          View research
                          <ArrowRight
                            size={16}
                          />
                        </Link>
                      </article>
                    ),
                  )}
                </div>
              </div>
            )}

            <article className="resume-recommendation">
              <div>
                <span className="eyebrow">
                  Recommended Resume
                </span>

                <h3>
                  {result.recommended_resume
                    ?.title ??
                    result.recommended_resume_type.replace(
                      /-/g,
                      " ",
                    )}
                </h3>

                <p>
                  {
                    result.recommendation_reason
                  }
                </p>
              </div>

              {resumeDownloadUrl ? (
                <a
                  className="button button-primary"
                  href={resumeDownloadUrl}
                  target="_blank"
                  rel="noreferrer"
                >
                  <Download size={18} />
                  Download Recommended Resume
                </a>
              ) : (
                <span className="resume-unavailable">
                  The recommended resume PDF has
                  not been uploaded yet.
                </span>
              )}
            </article>

            <p className="analysis-technical-note">
              Retrieval method:{" "}
              <strong>
                {result.embedding_method}
              </strong>
            </p>
          </div>
        </section>
      )}

      <section className="section">
        <div className="container interview-section-grid">
          <div>
            <span className="eyebrow">
              Recruitment
            </span>

            <h2>
              Interested in scheduling an
              interview?
            </h2>

            <p>
              Recruiters and hiring managers can
              submit preferred interview details
              directly through the portfolio.
            </p>
          </div>

          <InterviewRequestForm />
        </div>
      </section>
    </div>
  );
}