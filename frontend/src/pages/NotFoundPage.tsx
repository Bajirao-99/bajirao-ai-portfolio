import {
  ArrowLeft,
} from "lucide-react";
import { Link } from "react-router";

export default function NotFoundPage() {
  return (
    <div className="page-state">
      <span className="error-code">
        404
      </span>

      <h2>Page not found</h2>

      <p>
        The page you requested does not exist.
      </p>

      <Link
        className="button button-primary"
        to="/"
      >
        <ArrowLeft size={18} />
        Return home
      </Link>
    </div>
  );
}