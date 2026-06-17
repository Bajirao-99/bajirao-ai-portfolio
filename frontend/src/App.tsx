import {
  Route,
  Routes,
} from "react-router";

import AdminShell from "./components/admin/AdminShell";
import ProtectedAdminRoute from "./components/admin/ProtectedAdminRoute";
import AppShell from "./components/layout/AppShell";

import AdminAIActivityPage from "./pages/admin/AdminAIActivityPage";
import AdminContactMessagesPage from "./pages/admin/AdminContactMessagesPage";
import AdminContentPage from "./pages/admin/AdminContentPage";
import AdminDashboardPage from "./pages/admin/AdminDashboardPage";
import AdminInterviewRequestsPage from "./pages/admin/AdminInterviewRequestsPage";
import AdminLoginPage from "./pages/admin/AdminLoginPage";

import AIToolsPage from "./pages/AIToolsPage";
import HomePage from "./pages/HomePage";
import NotFoundPage from "./pages/NotFoundPage";
import ProjectDetailPage from "./pages/ProjectDetailPage";
import ResearchDetailPage from "./pages/ResearchDetailPage";

export default function App() {
  return (
    <Routes>
      <Route
        path="/admin/login"
        element={<AdminLoginPage />}
      />

      <Route
        element={<ProtectedAdminRoute />}
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

      <Route element={<AppShell />}>
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
          element={<ProjectDetailPage />}
        />

        <Route
          path="/research/:slug"
          element={<ResearchDetailPage />}
        />

        <Route
          path="*"
          element={<NotFoundPage />}
        />
      </Route>
    </Routes>
  );
}