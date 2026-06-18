import { useEffect } from "react";
import { useLocation } from "react-router";

interface SeoMetadata {
  title: string;
  description: string;
  image?: string;
}

const configuredSiteUrl =
  import.meta.env.VITE_SITE_URL ||
  "https://bajirao-ai-portfolio.vercel.app";

const SITE_URL = configuredSiteUrl.replace(
  /\/+$/,
  "",
);

const DEFAULT_IMAGE =
  `${SITE_URL}/og-image.png`;

const defaultMetadata: SeoMetadata = {
  title:
    "Bajirao Salunke | AI/ML Engineer, Backend Developer & Educator",
  description:
    "Portfolio of Bajirao Ramling Salunke featuring software projects, Hindi NLP research, technical skills, an AI job matcher and a RAG portfolio chatbot.",
};

const routeMetadata: Record<
  string,
  SeoMetadata
> = {
  "/": defaultMetadata,

  "/ai-tools": {
    title:
      "AI Job Matcher & Portfolio Chatbot | Bajirao Salunke",
    description:
      "Analyze job descriptions against Bajirao Salunke's skills, projects, experience and research using semantic matching and explainable AI.",
  },

  "/projects/recruitai-pro": {
    title:
      "RecruitAI Pro — AI Recruitment Platform | Bajirao Salunke",
    description:
      "Explore RecruitAI Pro, an AI-powered candidate-ranking system using semantic search, NLP, FastAPI and hybrid relevance scoring.",
  },

  "/research/hindi-event-extraction": {
    title:
      "Hindi Event Extraction Research | Bajirao Salunke",
    description:
      "Research on event detection and classification from Hindi children's narratives using LSTM and BiLSTM models, achieving 79.3% Macro F1.",
  },
};

function setMetaTag(
  selectorAttribute: "name" | "property",
  selectorValue: string,
  content: string,
): void {
  let element =
    document.head.querySelector<HTMLMetaElement>(
      `meta[${selectorAttribute}="${selectorValue}"]`,
    );

  if (!element) {
    element =
      document.createElement("meta");

    element.setAttribute(
      selectorAttribute,
      selectorValue,
    );

    document.head.appendChild(element);
  }

  element.setAttribute(
    "content",
    content,
  );
}

function setCanonicalUrl(
  url: string,
): void {
  let canonical =
    document.head.querySelector<HTMLLinkElement>(
      'link[rel="canonical"]',
    );

  if (!canonical) {
    canonical =
      document.createElement("link");

    canonical.rel = "canonical";
    document.head.appendChild(
      canonical,
    );
  }

  canonical.href = url;
}

function metadataForPath(
  pathname: string,
): SeoMetadata {
  const exactMetadata =
    routeMetadata[pathname];

  if (exactMetadata) {
    return exactMetadata;
  }

  if (
    pathname.startsWith(
      "/projects/",
    )
  ) {
    return {
      title:
        "Software Project | Bajirao Salunke",
      description:
        "Explore a software engineering and AI project from Bajirao Salunke's professional portfolio.",
    };
  }

  if (
    pathname.startsWith(
      "/research/",
    )
  ) {
    return {
      title:
        "Research Publication | Bajirao Salunke",
      description:
        "Explore artificial intelligence and natural language processing research by Bajirao Salunke.",
    };
  }

  return defaultMetadata;
}

export default function RouteSeo() {
  const location = useLocation();

  useEffect(() => {
    const metadata =
      metadataForPath(
        location.pathname,
      );

    const canonicalUrl =
      location.pathname === "/"
        ? `${SITE_URL}/`
        : `${SITE_URL}${location.pathname}`;

    const image =
      metadata.image ??
      DEFAULT_IMAGE;

    document.title =
      metadata.title;

    setMetaTag(
      "name",
      "description",
      metadata.description,
    );

    setMetaTag(
      "name",
      "robots",
      "index, follow, max-image-preview:large",
    );

    setMetaTag(
      "property",
      "og:title",
      metadata.title,
    );

    setMetaTag(
      "property",
      "og:description",
      metadata.description,
    );

    setMetaTag(
      "property",
      "og:url",
      canonicalUrl,
    );

    setMetaTag(
      "property",
      "og:image",
      image,
    );

    setMetaTag(
      "name",
      "twitter:title",
      metadata.title,
    );

    setMetaTag(
      "name",
      "twitter:description",
      metadata.description,
    );

    setMetaTag(
      "name",
      "twitter:image",
      image,
    );

    setCanonicalUrl(
      canonicalUrl,
    );
  }, [location.pathname]);

  return null;
}