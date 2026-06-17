import {
  ArrowLeft,
  ExternalLink,
  Eye,
  GitBranch,
  LoaderCircle,
} from "lucide-react";
import {
  useEffect,
  useState,
} from "react";
import {
  Link,
  useParams,
} from "react-router";

import {
  publicApi,
  resolveApiUrl,
} from "../lib/api";
import type {
  Project,
} from "../types/portfolio";

export default function ProjectDetailPage() {
  const { slug } = useParams();

  const [project, setProject] =
    useState<Project | null>(null);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState<string | null>(null);

  useEffect(() => {
    if (!slug) {
      setError("Project slug is missing.");
      setLoading(false);
      return;
    }

    const controller = new AbortController();

    async function loadProject() {
      try {
        const projectData =
          await publicApi.getProject(
            slug!,
            controller.signal,
          );

        setProject(projectData);

        const trackingKey =
          `bajirao_project_view:${slug}`;

        const previousTrackingTime =
          Number(
            sessionStorage.getItem(
              trackingKey,
            ) ?? "0",
          );

        if (
          Date.now() -
            previousTrackingTime >
          2000
        ) {
          sessionStorage.setItem(
            trackingKey,
            String(Date.now()),
          );

          void publicApi
            .trackProjectView(slug!)
            .catch(() => {
              // View analytics must not break the page.
            });
        }
      } catch (loadError) {
        if (
          loadError instanceof DOMException &&
          loadError.name === "AbortError"
        ) {
          return;
        }

        setError(
          loadError instanceof Error
            ? loadError.message
            : "Could not load project.",
        );
      } finally {
        setLoading(false);
      }
    }

    void loadProject();

    return () => {
      controller.abort();
    };
  }, [slug]);

  if (loading) {
    return (
      <div className="page-state">
        <LoaderCircle
          className="spin"
          size={42}
        />
        <h2>Loading project</h2>
      </div>
    );
  }

  if (error || !project) {
    return (
      <div className="page-state">
        <h2>Project not found</h2>
        <p>{error}</p>

        <Link
          className="button button-primary"
          to="/#projects"
        >
          <ArrowLeft size={18} />
          Back to projects
        </Link>
      </div>
    );
  }

  return (
    <article className="detail-page">
      <div className="detail-hero">
        <div className="container">
          <Link
            className="back-link"
            to="/#projects"
          >
            <ArrowLeft size={17} />
            Back to projects
          </Link>

          <span className="eyebrow">
            {project.category}
          </span>

          <h1>{project.title}</h1>

          <p>{project.short_description}</p>

          <div className="detail-meta">
            <span>
              <Eye size={17} />
              {project.view_count} views
            </span>

            {project.is_featured && (
              <span>Featured Project</span>
            )}
          </div>

          <div className="detail-actions">
            {project.github_url && (
              <a
                className="button button-secondary"
                href={project.github_url}
                target="_blank"
                rel="noreferrer"
              >
                <GitBranch size={18} />
                Source Code
              </a>
            )}

            {project.live_demo_url && (
              <a
                className="button button-primary"
                href={project.live_demo_url}
                target="_blank"
                rel="noreferrer"
              >
                <ExternalLink size={18} />
                Live Demo
              </a>
            )}
          </div>
        </div>
      </div>

      <div className="container detail-content">
        {project.images.length > 0 && (
          <div className="image-gallery">
            {project.images.map((image) => {
              const imageUrl =
                resolveApiUrl(
                  image.image_url,
                );

              if (!imageUrl) {
                return null;
              }

              return (
                <figure key={image.id}>
                  <img
                    src={imageUrl}
                    alt={image.alt_text}
                  />

                  {image.caption && (
                    <figcaption>
                      {image.caption}
                    </figcaption>
                  )}
                </figure>
              );
            })}
          </div>
        )}

        <section className="detail-section">
          <h2>Project Overview</h2>
          <p>{project.description}</p>
        </section>

        <section className="detail-section">
          <h2>Technology Stack</h2>

          <div className="tag-list tag-list-large">
            {project.tech_stack.map(
              (technology) => (
                <span key={technology}>
                  {technology}
                </span>
              ),
            )}
          </div>
        </section>

        <div className="detail-two-column">
          {project.challenges && (
            <section className="detail-card">
              <h2>Challenges</h2>
              <p>{project.challenges}</p>
            </section>
          )}

          {project.solutions && (
            <section className="detail-card">
              <h2>Solutions</h2>
              <p>{project.solutions}</p>
            </section>
          )}
        </div>

        {project.results && (
          <section className="detail-section detail-result">
            <h2>Results and Impact</h2>
            <p>{project.results}</p>
          </section>
        )}
      </div>
    </article>
  );
}