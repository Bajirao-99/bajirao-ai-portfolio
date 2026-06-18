import {
  ArrowLeft,
  LoaderCircle,
  LockKeyhole,
  ShieldCheck,
} from "lucide-react";

import {
  type FormEvent,
  useEffect,
  useState,
} from "react";

import {
  Link,
  useLocation,
  useNavigate,
} from "react-router";

import {
  useAdminAuth,
} from "../../contexts/AdminAuthContext";

interface LocationState {
  from?: string;
}

export default function AdminLoginPage() {
  const [username, setUsername] =
    useState("");

  const [password, setPassword] =
    useState("");

  const [submitting, setSubmitting] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);

  const {
    admin,
    initializing,
    login,
  } = useAdminAuth();

  const navigate = useNavigate();
  const location = useLocation();

  const requestedLocation =
    (
      location.state as
        | LocationState
        | null
    )?.from ?? "/admin";

  useEffect(() => {
    if (!initializing && admin) {
      navigate(
        requestedLocation,
        {
          replace: true,
        },
      );
    }
  }, [
    admin,
    initializing,
    navigate,
    requestedLocation,
  ]);

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    setSubmitting(true);
    setError(null);

    try {
      await login(
        username.trim(),
        password,
      );
    } catch (loginError) {
      setError(
        loginError instanceof Error
          ? loginError.message
          : "Admin login failed.",
      );

      setSubmitting(false);
    }
  }

  return (
    <div className="admin-login-page">
      <div className="admin-login-decoration admin-login-decoration-one" />
      <div className="admin-login-decoration admin-login-decoration-two" />

      <div className="admin-login-card">
        <Link
          className="admin-login-back"
          to="/"
        >
          <ArrowLeft size={17} />
          Public Portfolio
        </Link>

        <span className="admin-login-icon">
          <ShieldCheck size={31} />
        </span>

        <h1>Admin Login</h1>

        <p>
          Sign in to manage portfolio
          content, messages, analytics and
          AI activity.
        </p>

        <form onSubmit={handleSubmit}>
          <label>
            Username
            <input
              required
              autoComplete="username"
              value={username}
              onChange={(event) => {
                setUsername(
                  event.target.value,
                );
              }}
              placeholder="bajirao"
            />
          </label>

          <label>
            Password
            <input
              required
              type="password"
              autoComplete="current-password"
              value={password}
              onChange={(event) => {
                setPassword(
                  event.target.value,
                );
              }}
              placeholder="Enter admin password"
            />
          </label>

          {error && (
            <div 
              className="admin-login-error"
              role="alert"
            >
              {error}
            </div>
          )}

          <button
            type="submit"
            className="button button-primary button-full"
            disabled={
              submitting ||
              initializing
            }
          >
            {submitting ||
            initializing ? (
              <>
                <LoaderCircle
                  className="spin"
                  size={18}
                />
                Signing In
              </>
            ) : (
              <>
                <LockKeyhole
                  size={18}
                />
                Sign In
              </>
            )}
          </button>
        </form>

        <small>
          This area is restricted to the
          portfolio administrator.
        </small>
      </div>
    </div>
  );
}