import ScrollMemory from "./components/ScrollMemory";

import {
  lazy,
  Suspense,
} from "react";

import {
  LoaderCircle,
} from "lucide-react";

import {
  Route,
  Routes,
} from "react-router";

const AppShell = lazy(
  () =>
    import(
      "./components/layout/AppShell"
    ),
);

const AdminShell = lazy(
  () =>
    import(
      "./components/admin/AdminShell"
    ),
);

const ProtectedAdminRoute = lazy(
  () =>
    import(
      "./components/admin/ProtectedAdminRoute"
    ),
);

const AdminAIActivityPage = lazy(
  () =>
    import(
      "./pages/admin/AdminAIActivityPage"
    ),
);

const AdminContactMessagesPage = lazy(
  () =>
    import(
      "./pages/admin/AdminContactMessagesPage"
    ),
);

const AdminContentPage = lazy(
  () =>
    import(
      "./pages/admin/AdminContentPage"
    ),
);

const AdminDashboardPage = lazy(
  () =>
    import(
      "./pages/admin/AdminDashboardPage"
    ),
);

const AdminInterviewRequestsPage = lazy(
  () =>
    import(
      "./pages/admin/AdminInterviewRequestsPage"
    ),
);

const AdminLoginPage = lazy(
  () =>
    import(
      "./pages/admin/AdminLoginPage"
    ),
);

const AIToolsPage = lazy(
  () =>
    import(
      "./pages/AIToolsPage"
    ),
);

const HomePage = lazy(
  () =>
    import(
      "./pages/HomePage"
    ),
);

const NotFoundPage = lazy(
  () =>
    import(
      "./pages/NotFoundPage"
    ),
);

const ProjectDetailPage = lazy(
  () =>
    import(
      "./pages/ProjectDetailPage"
    ),
);

const ResearchDetailPage = lazy(
  () =>
    import(
      "./pages/ResearchDetailPage"
    ),
);

function RouteLoader() {
  return (
    <div
      className="route-loader"
      role="status"
      aria-live="polite"
    >
      <LoaderCircle
        className="spin"
        size={36}
        aria-hidden="true"
      />

      <span>
        Loading page
      </span>
    </div>
  );
}

export default function App() {
  return (
    <>
      <ScrollMemory />
      
      <Suspense
        fallback={<RouteLoader />}
      >
        <Routes>
          <Route
            path="/admin/login"
            element={
              <AdminLoginPage />
            }
          />

          <Route
            element={
              <ProtectedAdminRoute />
            }
          >
            <Route
              path="/admin"
              element={<AdminShell />}
            >
              <Route
                index
                element={
                  <AdminDashboardPage />
                }
              />

              <Route
                path="messages"
                element={
                  <AdminContactMessagesPage />
                }
              />

              <Route
                path="interviews"
                element={
                  <AdminInterviewRequestsPage />
                }
              />

              <Route
                path="ai-activity"
                element={
                  <AdminAIActivityPage />
                }
              />

              <Route
                path="content"
                element={
                  <AdminContentPage />
                }
              />
            </Route>
          </Route>

          <Route
            element={<AppShell />}
          >
            <Route
              path="/"
              element={<HomePage />}
            />

            <Route
              path="/ai-tools"
              element={<AIToolsPage />}
            />

            <Route
              path="/projects/:slug"
              element={
                <ProjectDetailPage />
              }
            />

            <Route
              path="/research/:slug"
              element={
                <ResearchDetailPage />
              }
            />

            <Route
              path="*"
              element={<NotFoundPage />}
            />
          </Route>
        </Routes>
      </Suspense>
    </>
  );
}