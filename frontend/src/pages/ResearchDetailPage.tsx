import {
  ArrowLeft,
  BookOpen,
  ExternalLink,
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
} from "../lib/api";
import type {
  ResearchPublication,
} from "../types/portfolio";

export default function ResearchDetailPage() {
  const { slug } = useParams();

  const [research, setResearch] =
    useState<ResearchPublication | null>(
      null,
    );

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState<string | null>(null);

  useEffect(() => {
    if (!slug) {
      setError("Research slug is missing.");
      setLoading(false);
      return;
    }

    const controller = new AbortController();

    publicApi
      .getResearch(
        slug,
        controller.signal,
      )
      .then(setResearch)
      .catch((loadError) => {
        if (
          loadError instanceof DOMException &&
          loadError.name === "AbortError"
        ) {
          return;
        }

        setError(
          loadError instanceof Error
            ? loadError.message
            : "Could not load research.",
        );
      })
      .finally(() => {
        setLoading(false);
      });

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
        <h2>Loading research</h2>
      </div>
    );
  }

  if (error || !research) {
    return (
      <div className="page-state">
        <h2>Research not found</h2>
        <p>{error}</p>

        <Link
          className="button button-primary"
          to="/#research"
        >
          <ArrowLeft size={18} />
          Back to research
        </Link>
      </div>
    );
  }

  return (
    <article className="detail-page">
      <div className="detail-hero research-detail-hero">
        <div className="container">
          <Link
            className="back-link"
            to="/#research"
          >
            <ArrowLeft size={17} />
            Back to research
          </Link>

          <div className="research-detail-icon">
            <BookOpen size={30} />
          </div>

          <span className="eyebrow">
            {research.research_type}
          </span>

          <h1>{research.title}</h1>

          <p>{research.short_summary}</p>

          <div className="detail-meta">
            <span>
              {research.publication_status}
            </span>

            {research.venue && (
              <span>{research.venue}</span>
            )}
          </div>

          <div className="detail-actions">
            {research.paper_url && (
              <a
                className="button button-secondary"
                href={research.paper_url}
                target="_blank"
                rel="noreferrer"
              >
                <ExternalLink size={18} />
                View Paper
              </a>
            )}

            {research.thesis_url && (
              <a
                className="button button-primary"
                href={research.thesis_url}
                target="_blank"
                rel="noreferrer"
              >
                <ExternalLink size={18} />
                View Thesis
              </a>
            )}
          </div>
        </div>
      </div>

      <div className="container detail-content">
        <section className="detail-section">
          <h2>Abstract</h2>
          <p>{research.abstract}</p>
        </section>

        <div className="research-metrics research-metrics-large">
          {Object.entries(
            research.metrics,
          ).map(([metric, value]) => (
            <div key={metric}>
              <strong>{value}</strong>
              <span>{metric}</span>
            </div>
          ))}
        </div>

        <div className="detail-two-column">
          {research.dataset_details && (
            <section className="detail-card">
              <h2>Dataset</h2>
              <p>
                {research.dataset_details}
              </p>
            </section>
          )}

          {research.methodology && (
            <section className="detail-card">
              <h2>Methodology</h2>
              <p>{research.methodology}</p>
            </section>
          )}
        </div>

        <section className="detail-section">
          <h2>Models Used</h2>

          <div className="tag-list tag-list-large">
            {research.models_used.map(
              (model) => (
                <span key={model}>
                  {model}
                </span>
              ),
            )}
          </div>
        </section>
      </div>
    </article>
  );
}