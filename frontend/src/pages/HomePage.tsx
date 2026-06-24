import {
  ArrowRight,
  Award,
  BookOpen,
  BriefcaseBusiness,
  CheckCircle2,
  Code2,
  Download,
  ExternalLink,
  GitBranch,
  GraduationCap,
  LoaderCircle,
  Mail,
  MapPin,
  Send,
  Sparkles,
  Star,
  Trophy,
  UserRound,
} from "lucide-react";
import {
  type FormEvent,
  useMemo,
  useState,
} from "react";
import { Link } from "react-router";

import {
  publicApi,
  resolveApiUrl,
} from "../lib/api";
import {
  usePortfolioData,
} from "../hooks/usePortfolioData";
import type {
  Skill,
} from "../types/portfolio";

function formatDate(
  value: string | null,
): string {
  if (!value) {
    return "Present";
  }

  return new Intl.DateTimeFormat(
    "en-IN",
    {
      month: "short",
      year: "numeric",
    },
  ).format(new Date(value));
}

function formatFileSize(
  bytes: number,
): string {
  if (bytes < 1024 * 1024) {
    return `${Math.max(
      1,
      Math.round(bytes / 1024),
    )} KB`;
  }

  return `${(
    bytes /
    (1024 * 1024)
  ).toFixed(1)} MB`;
}

function getInitials(
  fullName: string,
): string {
  return fullName
    .split(/\s+/)
    .slice(0, 2)
    .map((part) => part.charAt(0))
    .join("")
    .toUpperCase();
}

function SectionHeading({
  eyebrow,
  title,
  description,
}: {
  eyebrow: string;
  title: string;
  description?: string;
}) {
  return (
    <div className="section-heading">
      <span className="eyebrow">
        {eyebrow}
      </span>

      <h2>{title}</h2>

      {description && <p>{description}</p>}
    </div>
  );
}

function LoadingScreen() {
  return (
    <div className="page-state">
      <LoaderCircle
        className="spin"
        size={42}
      />

      <h2>Loading portfolio</h2>

      <p>
        Retrieving profile, projects and research
        information.
      </p>
    </div>
  );
}

function ErrorScreen({
  message,
  onRetry,
}: {
  message: string;
  onRetry: () => void;
}) {
  return (
    <div className="page-state">
      <h2>Could not load the portfolio</h2>

      <p>{message}</p>

      <button
        type="button"
        className="button button-primary"
        onClick={onRetry}
      >
        Try again
      </button>
    </div>
  );
}

export default function HomePage() {
  const {
    data,
    loading,
    error,
    refetch,
  } = usePortfolioData();

  const [contactForm, setContactForm] =
    useState({
      name: "",
      email: "",
      phone: "",
      subject: "",
      message: "",
    });

  const [
    profileImageFailed, 
    setProfileImageFailed
  ] = useState(false);

  const [
    contactSubmitting,
    setContactSubmitting,
  ] = useState(false);

  const [
    contactSuccess,
    setContactSuccess,
  ] = useState<string | null>(null);

  const [
    contactError,
    setContactError,
  ] = useState<string | null>(null);

  const skillGroups = useMemo(() => {
    if (!data) {
      return [];
    }

    const groups = new Map<
      string,
      Skill[]
    >();

    for (const skill of data.skills) {
      const existingGroup =
        groups.get(skill.category) ?? [];

      existingGroup.push(skill);
      groups.set(
        skill.category,
        existingGroup,
      );
    }

    return Array.from(groups.entries());
  }, [data]);

  async function handleContactSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    setContactSubmitting(true);
    setContactSuccess(null);
    setContactError(null);

    try {
      const response =
        await publicApi.submitContact({
          name: contactForm.name.trim(),
          email: contactForm.email.trim(),
          phone:
            contactForm.phone.trim() || null,
          subject:
            contactForm.subject.trim(),
          message:
            contactForm.message.trim(),
        });

      setContactSuccess(response.message);

      setContactForm({
        name: "",
        email: "",
        phone: "",
        subject: "",
        message: "",
      });
    } catch (submissionError) {
      setContactError(
        submissionError instanceof Error
          ? submissionError.message
          : "Could not submit the message.",
      );
    } finally {
      setContactSubmitting(false);
    }
  }

  if (loading) {
    return <LoadingScreen />;
  }

  if (error || !data) {
    return (
      <ErrorScreen
        message={
          error ??
          "Portfolio information is unavailable."
        }
        onRetry={refetch}
      />
    );
  }

  const {
    profile,
    education,
    experiences,
    achievements,
    certifications,
    projects,
    research,
    resumes,
    github,
    codingProfiles,
  } = data;

  const firstResume = resumes[0];

  const resumeUrl = firstResume
    ? resolveApiUrl(
        firstResume.download_url,
      )
    : null;

  const profileImageUrl =
    profile.profile_image_url
      ? resolveApiUrl(
        profile.profile_image_url,
      )
      : null;

  return (
    <>
      <section className="hero-section">
        <div className="hero-background hero-background-one" />
        <div className="hero-background hero-background-two" />

        <div className="container hero-grid">
          <div className="hero-content">
            <span className="hero-badge">
              <Sparkles size={16} />
              AI-powered professional portfolio
            </span>

            <p className="hero-introduction">
              Hello, I am
            </p>

            <h1>{profile.full_name}</h1>

            <h2>{profile.headline}</h2>

            <p className="hero-description">
              {profile.short_bio}
            </p>

            <div className="hero-meta">
              {profile.location && (
                <span>
                  <MapPin size={17} />
                  {profile.location}
                </span>
              )}

              <span>
                <BriefcaseBusiness size={17} />
                {profile.years_experience}+
                years of experience
              </span>
            </div>

            <div className="hero-actions">
              <Link
                className="button button-primary"
                to="/#projects"
              >
                View Projects
                <ArrowRight size={18} />
              </Link>

              {resumeUrl && (
                <a
                  className="button button-secondary"
                  href={resumeUrl}
                  target="_blank"
                  rel="noreferrer"
                >
                  <Download size={18} />
                  Download Resume
                </a>
              )}
            </div>

            <div className="social-links">
              {profile.github_url && (
                <a
                  href={profile.github_url}
                  target="_blank"
                  rel="noreferrer"
                  aria-label="GitHub profile"
                >
                  <GitBranch size={21} />
                </a>
              )}

              {profile.linkedin_url && (
                <a
                  href={profile.linkedin_url}
                  target="_blank"
                  rel="noreferrer"
                >
                  in
                </a>
              )}

              <a
                href={`mailto:${profile.email}`}
                aria-label="Send email"
              >
                <Mail size={21} />
              </a>
            </div>
          </div>

          <div className="hero-visual">
            <div
              className="profile-orbit profile-orbit-large orbit-spin-clockwise"
              aria-hidden="true"
            />

            <div
              className="profile-orbit profile-orbit-small orbit-spin-reverse"
              aria-hidden="true"
            />

            <div className="profile-card">
              {profileImageUrl && !profileImageFailed ? (
                <img
                  src={profileImageUrl}
                  alt={profile.full_name}
                  loading="eager"
                  fetchPriority="high"
                  decoding="async"
                  width={480}
                  height={480}
                  onError={() => {
                    setProfileImageFailed(true);
                  }}
                />
              ) : (
                <div 
                  className="profile-initials"
                  aria-label={profile.full_name}
                >
                  {getInitials(
                    profile.full_name,
                  )}
                </div>
              )}

              <div className="profile-status">
                <span />
                Available for opportunities
              </div>
            </div>

            <div className="floating-card floating-card-code floating-card-motion-one">
              <Code2 size={20} />
              <div>
                <strong>Full Stack</strong>
                <span>React + FastAPI</span>
              </div>
            </div>

            <div className="floating-card floating-card-ai floating-card-motion-two">
              <Sparkles size={20} />
              <div>
                <strong>AI & NLP</strong>
                <span>RAG + Embeddings</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section
        className="section"
        id="about"
      >
        <div className="container about-grid">
          <div>
            <SectionHeading
              eyebrow="Professional Profile"
              title="Building intelligent software and meaningful learning experiences"
            />

            <p className="about-text">
              {profile.about_me}
            </p>

            <div className="about-contact">
              <a
                href={`mailto:${profile.email}`}
              >
                <Mail size={18} />
                {profile.email}
              </a>

              {profile.location && (
                <span>
                  <MapPin size={18} />
                  {profile.location}
                </span>
              )}
            </div>
          </div>

          <div className="stats-grid">
            <article className="stat-card">
              <strong>
                {profile.years_experience}+
              </strong>
              <span>Years Experience</span>
            </article>

            <article className="stat-card">
              <strong>
                {projects.length}+
              </strong>
              <span>Portfolio Projects</span>
            </article>

            <article className="stat-card">
              <strong>
                {data.skills.length}+
              </strong>
              <span>Technical Skills</span>
            </article>

            <article className="stat-card">
              <strong>
                {research.length}+
              </strong>
              <span>Research Works</span>
            </article>
          </div>
        </div>
      </section>

      <section
        className="section section-muted"
        id="experience"
      >
        <div className="container">
          <SectionHeading
            eyebrow="Career Journey"
            title="Experience and education"
            description="Academic, teaching, research and software development experience."
          />

          <div className="two-column-content">
            <div>
              <h3 className="content-column-title">
                <BriefcaseBusiness size={21} />
                Work Experience
              </h3>

              <div className="timeline">
                {experiences.map(
                  (experience) => (
                    <article
                      className="timeline-item"
                      key={experience.id}
                    >
                      <span className="timeline-marker" />

                      <div className="timeline-card">
                        <div className="timeline-header">
                          <div>
                            <h4>
                              {
                                experience.job_title
                              }
                            </h4>

                            <p>
                              {
                                experience.organization
                              }
                            </p>
                          </div>

                          {experience.is_current && (
                            <span className="status-pill">
                              Current
                            </span>
                          )}
                        </div>

                        <span className="timeline-date">
                          {formatDate(
                            experience.start_date,
                          )}
                          {" — "}
                          {formatDate(
                            experience.end_date,
                          )}
                        </span>

                        {experience.location && (
                          <span className="timeline-location">
                            <MapPin size={15} />
                            {
                              experience.location
                            }
                          </span>
                        )}

                        {experience.description && (
                          <p>
                            {
                              experience.description
                            }
                          </p>
                        )}
                      </div>
                    </article>
                  ),
                )}
              </div>
            </div>

            <div>
              <h3 className="content-column-title">
                <GraduationCap size={22} />
                Education
              </h3>

              <div className="timeline">
                {education.map(
                  (educationItem) => (
                    <article
                      className="timeline-item"
                      key={educationItem.id}
                    >
                      <span className="timeline-marker" />

                      <div className="timeline-card">
                        <h4>
                          {educationItem.degree}
                        </h4>

                        <p className="timeline-organization">
                          {
                            educationItem.institution
                          }
                        </p>

                        <p>
                          {
                            educationItem.field_of_study
                          }
                        </p>

                        <span className="timeline-date">
                          {formatDate(
                            educationItem.start_date,
                          )}
                          {" — "}
                          {formatDate(
                            educationItem.end_date,
                          )}
                        </span>

                        {educationItem.grade && (
                          <span className="education-grade">
                            {
                              educationItem.grade
                            }
                          </span>
                        )}

                        {educationItem.description && (
                          <p>
                            {
                              educationItem.description
                            }
                          </p>
                        )}
                      </div>
                    </article>
                  ),
                )}
              </div>
            </div>
          </div>
        </div>
      </section>

      <section
        className="section"
        id="skills"
      >
        <div className="container">
          <SectionHeading
            eyebrow="Technical Expertise"
            title="Skills and technologies"
            description="A combination of software engineering, artificial intelligence, research and academic expertise."
          />

          <div className="skill-category-grid">
            {skillGroups.map(
              ([category, categorySkills]) => (
                <article
                  className="skill-category-card"
                  key={category}
                >
                  <h3>{category}</h3>

                  <div className="skill-list">
                    {categorySkills.map(
                      (skill) => (
                        <div
                          className="skill-item"
                          key={skill.id}
                        >
                          <div className="skill-label">
                            <span>
                              {skill.name}

                              {skill.is_featured && (
                                <Star
                                  size={14}
                                  fill="currentColor"
                                />
                              )}
                            </span>

                            <strong>
                              {
                                skill.proficiency
                              }
                              %
                            </strong>
                          </div>

                          <div className="skill-progress">
                            <span
                              style={{
                                width: `${skill.proficiency}%`,
                              }}
                            />
                          </div>
                        </div>
                      ),
                    )}
                  </div>
                </article>
              ),
            )}
          </div>
        </div>
      </section>

      <section
        className="section section-muted"
        id="projects"
      >
        <div className="container">
          <SectionHeading
            eyebrow="Selected Work"
            title="Featured projects"
            description="Full-stack, artificial intelligence, NLP and systems projects focused on solving practical problems."
          />

          <div className="project-grid">
            {projects.map((project) => {
              const projectImage =
                project.images[0];

              const projectImageUrl =
                resolveApiUrl(
                  projectImage?.image_url,
                );

              return (
                <article
                  className="project-card"
                  key={project.id}
                >
                  <div className="project-image">
                    {projectImageUrl ? (
                      <img
                        src={projectImageUrl}
                        alt={
                          projectImage.alt_text ||
                          `${project.title} project screenshot`
                        }
                        loading="lazy"
                        decoding="async"
                        width={1200}
                        height={675}
                      />
                    ) : (
                      <div className="project-placeholder">
                        <Code2 size={46} />
                      </div>
                    )}

                    {project.is_featured && (
                      <span className="featured-badge">
                        Featured
                      </span>
                    )}
                  </div>

                  <div className="project-card-content">
                    <span className="project-category">
                      {project.category}
                    </span>

                    <h3>{project.title}</h3>

                    <p>
                      {
                        project.short_description
                      }
                    </p>

                    <div className="tag-list">
                      {project.tech_stack
                        .slice(0, 6)
                        .map((technology) => (
                          <span key={technology}>
                            {technology}
                          </span>
                        ))}
                    </div>

                    <div className="project-card-footer">
                      <Link
                        to={`/projects/${project.slug}`}
                      >
                        View Details
                        <ArrowRight
                          size={17}
                        />
                      </Link>

                      <span>
                        {project.view_count} views
                      </span>
                    </div>
                  </div>
                </article>
              );
            })}
          </div>
        </div>
      </section>

      <section
        className="section"
        id="research"
      >
        <div className="container">
          <SectionHeading
            eyebrow="Research"
            title="Research and publications"
            description="Natural language processing research supported by annotated datasets and neural sequence models."
          />

          <div className="research-grid">
            {research.map(
              (researchItem) => (
                <article
                  className="research-card"
                  key={researchItem.id}
                >
                  <div className="research-icon">
                    <BookOpen size={28} />
                  </div>

                  <div>
                    <div className="research-meta">
                      <span>
                        {
                          researchItem.research_type
                        }
                      </span>

                      <span>
                        {
                          researchItem.publication_status
                        }
                      </span>
                    </div>

                    <h3>
                      {researchItem.title}
                    </h3>

                    <p>
                      {
                        researchItem.short_summary
                      }
                    </p>

                    <div className="tag-list">
                      {researchItem.models_used.map(
                        (model) => (
                          <span key={model}>
                            {model}
                          </span>
                        ),
                      )}
                    </div>

                    <div className="research-metrics">
                      {Object.entries(
                        researchItem.metrics,
                      )
                        .slice(0, 4)
                        .map(
                          ([metric, value]) => (
                            <div key={metric}>
                              <strong>
                                {value}
                              </strong>

                              <span>
                                {metric}
                              </span>
                            </div>
                          ),
                        )}
                    </div>

                    <Link
                      className="text-link"
                      to={`/research/${researchItem.slug}`}
                    >
                      View research details
                      <ArrowRight size={17} />
                    </Link>
                  </div>
                </article>
              ),
            )}
          </div>
        </div>
      </section>

      {(achievements.length > 0 ||
        certifications.length > 0) && (
        <section className="section section-muted">
          <div className="container">
            <SectionHeading
              eyebrow="Recognition"
              title="Achievements and certifications"
            />

            <div className="two-column-content">
              <div>
                <h3 className="content-column-title">
                  <Trophy size={22} />
                  Achievements
                </h3>

                <div className="recognition-list">
                  {achievements.map(
                    (achievement) => (
                      <article
                        className="recognition-card"
                        key={achievement.id}
                      >
                        <span className="recognition-icon">
                          <Award size={22} />
                        </span>

                        <div>
                          <h4>
                            {achievement.title}
                          </h4>

                          {achievement.result && (
                            <strong>
                              {
                                achievement.result
                              }
                            </strong>
                          )}

                          {achievement.description && (
                            <p>
                              {
                                achievement.description
                              }
                            </p>
                          )}

                          {achievement.issuer && (
                            <span>
                              {
                                achievement.issuer
                              }
                            </span>
                          )}
                        </div>
                      </article>
                    ),
                  )}
                </div>
              </div>

              <div>
                <h3 className="content-column-title">
                  <CheckCircle2 size={22} />
                  Certifications
                </h3>

                <div className="recognition-list">
                  {certifications.length ===
                  0 ? (
                    <div className="empty-card">
                      Certifications will appear
                      here after they are added.
                    </div>
                  ) : (
                    certifications.map(
                      (certification) => (
                        <article
                          className="recognition-card"
                          key={certification.id}
                        >
                          <span className="recognition-icon">
                            <CheckCircle2
                              size={22}
                            />
                          </span>

                          <div>
                            <h4>
                              {
                                certification.name
                              }
                            </h4>

                            <strong>
                              {
                                certification.issuer
                              }
                            </strong>

                            {certification.description && (
                              <p>
                                {
                                  certification.description
                                }
                              </p>
                            )}

                            {certification.credential_url && (
                              <a
                                href={
                                  certification.credential_url
                                }
                                target="_blank"
                                rel="noreferrer"
                                className="text-link"
                              >
                                View credential
                                <ExternalLink
                                  size={15}
                                />
                              </a>
                            )}
                          </div>
                        </article>
                      ),
                    )
                  )}
                </div>
              </div>
            </div>
          </div>
        </section>
      )}

      {github && (
        <section className="section">
          <div className="container">
            <SectionHeading
              eyebrow="Open Source"
              title="GitHub activity"
              description="Featured repositories, technologies, stars and recent development work."
            />

            <div className="github-profile-card">
              <img
                src={github.profile.avatar_url}
                alt={`${github.profile.username} GitHub profile`}
                loading="lazy"
                decoding="async"
                width={460}
                height={460}
              />

              <div className="github-profile-content">
                <span className="eyebrow">
                  GitHub Profile
                </span>

                <h3>
                  {github.profile.name ??
                    github.profile.username}
                </h3>

                <p>
                  {github.profile.bio ??
                    "Software development and research repositories."}
                </p>

                <div className="github-stats">
                  <span>
                    <strong>
                      {
                        github.profile
                          .public_repos
                      }
                    </strong>
                    Repositories
                  </span>

                  <span>
                    <strong>
                      {
                        github.profile
                          .total_stars
                      }
                    </strong>
                    Stars
                  </span>

                  <span>
                    <strong>
                      {
                        github.profile
                          .total_forks
                      }
                    </strong>
                    Forks
                  </span>
                </div>
              </div>

              <a
                className="button button-secondary"
                href={github.profile.profile_url}
                target="_blank"
                rel="noreferrer"
              >
                <GitBranch size={18} />
                Open GitHub
              </a>
            </div>

            <div className="repository-grid">
              {github.repositories
                .slice(0, 6)
                .map((repository) => (
                  <article
                    className="repository-card"
                    key={repository.id}
                  >
                    <div className="repository-heading">
                      <GitBranch size={20} />

                      {repository.is_featured && (
                        <span>
                          Featured
                        </span>
                      )}
                    </div>

                    <h3>{repository.name}</h3>

                    <p>
                      {repository.description ??
                        "GitHub repository"}
                    </p>

                    <div className="repository-details">
                      {repository.language && (
                        <span>
                          {
                            repository.language
                          }
                        </span>
                      )}

                      <span>
                        ★{" "}
                        {
                          repository.stars_count
                        }
                      </span>

                      <span>
                        Forks{" "}
                        {
                          repository.forks_count
                        }
                      </span>
                    </div>

                    <a
                      className="text-link"
                      href={
                        repository.repository_url
                      }
                      target="_blank"
                      rel="noreferrer"
                    >
                      View repository
                      <ExternalLink
                        size={15}
                      />
                    </a>
                  </article>
                ))}
            </div>
          </div>
        </section>
      )}

      {codingProfiles.length > 0 && (
        <section className="section section-muted">
          <div className="container">
            <SectionHeading
              eyebrow="Problem Solving"
              title="Coding profiles"
            />

            <div className="coding-profile-grid">
              {codingProfiles.map(
                (codingProfile) => (
                  <article
                    className="coding-profile-card"
                    key={codingProfile.id}
                  >
                    <Code2 size={28} />

                    <h3>
                      {
                        codingProfile.display_name
                      }
                    </h3>

                    {codingProfile.total_solved !==
                      null && (
                      <strong className="coding-total">
                        {
                          codingProfile.total_solved
                        }
                        +
                        <span>
                          Problems solved
                        </span>
                      </strong>
                    )}

                    {codingProfile.ranking && (
                      <p>
                        {
                          codingProfile.ranking
                        }
                      </p>
                    )}

                    {codingProfile.achievement_summary && (
                      <p>
                        {
                          codingProfile.achievement_summary
                        }
                      </p>
                    )}

                    {codingProfile.profile_url && (
                      <a
                        className="text-link"
                        href={
                          codingProfile.profile_url
                        }
                        target="_blank"
                        rel="noreferrer"
                      >
                        Open profile
                        <ExternalLink
                          size={15}
                        />
                      </a>
                    )}
                  </article>
                ),
              )}
            </div>
          </div>
        </section>
      )}

      <section
        className="section"
        id="resumes"
      >
        <div className="container">
          <SectionHeading
            eyebrow="Resume"
            title="Choose the most relevant resume"
            description="Different resume versions tailored for software engineering, AI/ML and academic opportunities."
          />

          <div className="resume-grid">
            {resumes.map((resume) => {
              const downloadUrl =
                resolveApiUrl(
                  resume.download_url,
                );

              return (
                <article
                  className="resume-card"
                  key={resume.id}
                >
                  <div className="resume-icon">
                    <Download size={25} />
                  </div>

                  <span className="resume-type">
                    {resume.resume_type.replace(
                      /-/g,
                      " ",
                    )}
                  </span>

                  <h3>{resume.title}</h3>

                  <p>
                    {resume.description ??
                      "Download the latest resume version."}
                  </p>

                  <div className="resume-meta">
                    <span>
                      {formatFileSize(
                        resume.file_size_bytes,
                      )}
                    </span>

                    <span>
                      {
                        resume.download_count
                      }{" "}
                      downloads
                    </span>
                  </div>

                  {downloadUrl && (
                    <a
                      className="button button-primary button-full"
                      href={downloadUrl}
                      target="_blank"
                      rel="noreferrer"
                    >
                      <Download size={17} />
                      Download PDF
                    </a>
                  )}
                </article>
              );
            })}
          </div>
        </div>
      </section>

      <section
        className="section contact-section"
        id="contact"
      >
        <div className="container contact-grid">
          <div>
            <SectionHeading
              eyebrow="Get in Touch"
              title="Discuss an opportunity or collaboration"
              description="Send a message regarding software roles, AI projects, research collaboration, teaching or consulting."
            />

            <div className="contact-information">
              <a
                href={`mailto:${profile.email}`}
              >
                <span>
                  <Mail size={21} />
                </span>

                <div>
                  <strong>Email</strong>
                  <p>{profile.email}</p>
                </div>
              </a>

              {profile.location && (
                <div>
                  <span>
                    <MapPin size={21} />
                  </span>

                  <div>
                    <strong>Location</strong>
                    <p>
                      {profile.location}
                    </p>
                  </div>
                </div>
              )}

              <div>
                <span>
                  <UserRound size={21} />
                </span>

                <div>
                  <strong>
                    Opportunities
                  </strong>
                  <p>
                    Software Engineering, AI/ML,
                    NLP and Academic roles
                  </p>
                </div>
              </div>
            </div>
          </div>

          <form
            className="contact-form"
            onSubmit={handleContactSubmit}
          >
            <div className="form-row">
              <label>
                Name
                <input
                  required
                  minLength={2}
                  maxLength={150}
                  value={contactForm.name}
                  onChange={(event) => {
                    setContactForm(
                      (currentForm) => ({
                        ...currentForm,
                        name: event.target.value,
                      }),
                    );
                  }}
                  placeholder="Your name"
                />
              </label>

              <label>
                Email
                <input
                  required
                  type="email"
                  value={contactForm.email}
                  onChange={(event) => {
                    setContactForm(
                      (currentForm) => ({
                        ...currentForm,
                        email:
                          event.target.value,
                      }),
                    );
                  }}
                  placeholder="you@example.com"
                />
              </label>
            </div>

            <div className="form-row">
              <label>
                Phone
                <input
                  maxLength={30}
                  value={contactForm.phone}
                  onChange={(event) => {
                    setContactForm(
                      (currentForm) => ({
                        ...currentForm,
                        phone:
                          event.target.value,
                      }),
                    );
                  }}
                  placeholder="Optional"
                />
              </label>

              <label>
                Subject
                <input
                  required
                  minLength={3}
                  maxLength={250}
                  value={contactForm.subject}
                  onChange={(event) => {
                    setContactForm(
                      (currentForm) => ({
                        ...currentForm,
                        subject:
                          event.target.value,
                      }),
                    );
                  }}
                  placeholder="Opportunity or collaboration"
                />
              </label>
            </div>

            <label>
              Message
              <textarea
                required
                minLength={10}
                maxLength={5000}
                rows={6}
                value={contactForm.message}
                onChange={(event) => {
                  setContactForm(
                    (currentForm) => ({
                      ...currentForm,
                      message:
                        event.target.value,
                    }),
                  );
                }}
                placeholder="Write your message here..."
              />
            </label>

            {contactSuccess && (
              <div 
                className="form-message form-success"
                role="status"
                aria-live="polite"
              >
                <CheckCircle2 size={18} />
                {contactSuccess}
              </div>
            )}

            {contactError && (
              <div 
                className="form-message form-error"
                role="alert"
                >
                  {contactError}
              </div>
            )}

            <button
              type="submit"
              className="button button-primary button-full"
              disabled={contactSubmitting}
            >
              {contactSubmitting ? (
                <>
                  <LoaderCircle
                    className="spin"
                    size={18}
                  />
                  Sending
                </>
              ) : (
                <>
                  <Send size={18} />
                  Send Message
                </>
              )}
            </button>
          </form>
        </div>
      </section>
    </>
  );
}