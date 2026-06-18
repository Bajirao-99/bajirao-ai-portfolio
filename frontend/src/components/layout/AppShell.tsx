import PortfolioChatWidget from "../PortfolioChatWidget";

import RouteSeo from "../RouteSeo";

import {
  BrainCircuit,
  Download,
  Menu,
  X,
} from "lucide-react";
import {
  Link,
  Outlet,
  useLocation,
} from "react-router";
import {
  useEffect,
  useState,
} from "react";

import {
  useAnalyticsTracker,
} from "../../hooks/useAnalyticsTracker";

const navigationItems = [
  { label: "About", target: "/#about" },
  {
    label: "Experience",
    target: "/#experience",
  },
  { label: "Skills", target: "/#skills" },
  {
    label: "Projects",
    target: "/#projects",
  },
  {
    label: "Research",
    target: "/#research",
  },
  {
    label: "AI Tools",
    target: "/ai-tools",
  },
  { label: "Resume", target: "/#resumes" },
  { label: "Contact", target: "/#contact" },
];

export default function AppShell() {
  const location = useLocation();

  const [mobileMenuOpen, setMobileMenuOpen] =
    useState(false);

  useAnalyticsTracker();

  useEffect(() => {
    setMobileMenuOpen(false);

    if (location.hash) {
      const sectionId =
        location.hash.replace("#", "");

      window.setTimeout(() => {
        document
          .getElementById(sectionId)
          ?.scrollIntoView({
            behavior: "smooth",
            block: "start",
          });
      }, 50);

      return;
    }

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  }, [
    location.pathname,
    location.hash,
  ]);

  return (
    <div className="site-shell">
      <RouteSeo />

      <a
        className="skip-link"
        href="#main-content"
      >
        Skip to main content
      </a>

      <header className="site-header">
        <div className="container navbar">
          <Link
            className="brand"
            to="/"
            aria-label="Bajirao portfolio home"
          >
            <span className="brand-icon">
              <BrainCircuit size={22} />
            </span>

            <span>
              Bajirao
              <strong>AI</strong>
            </span>
          </Link>

          <nav
            className={
              mobileMenuOpen
                ? "nav-links nav-links-open"
                : "nav-links"
            }
          >
            {navigationItems.map((item) => (
              <Link
                key={item.target}
                to={item.target}
              >
                {item.label}
              </Link>
            ))}

            <Link
              className="button button-small button-primary"
              to="/#resumes"
            >
              <Download size={16} />
              Resume
            </Link>
          </nav>

          <button
            type="button"
            className="menu-button"
            aria-label="Toggle navigation menu"
            aria-expanded={mobileMenuOpen}
            onClick={() => {
              setMobileMenuOpen(
                (currentValue) => !currentValue,
              );
            }}
          >
            {mobileMenuOpen ? (
              <X size={24} />
            ) : (
              <Menu size={24} />
            )}
          </button>
        </div>
      </header>

      <main
        id="main-content"
        tabIndex={-1}
      >
        <Outlet />
      </main>

      <PortfolioChatWidget />

      <footer className="site-footer">
        <div className="container footer-content">
          <div>
            <Link
              className="brand footer-brand"
              to="/"
            >
              <span className="brand-icon">
                <BrainCircuit size={20} />
              </span>

              <span>
                Bajirao
                <strong>AI</strong>
              </span>
            </Link>

            <p>
              AI-powered professional portfolio
              built with React, FastAPI,
              PostgreSQL, RAG and semantic
              matching.
            </p>
          </div>

          <div className="footer-links">
            <Link to="/#projects">
              Projects
            </Link>

            <Link to="/#research">
              Research
            </Link>

            <Link to="/#resumes">
              Resumes
            </Link>

            <Link to="/#contact">
              Contact
            </Link>
          </div>

          <p className="footer-copyright">
            © {new Date().getFullYear()} Bajirao
            Ramling Salunke
          </p>
        </div>
      </footer>
    </div>
  );
}