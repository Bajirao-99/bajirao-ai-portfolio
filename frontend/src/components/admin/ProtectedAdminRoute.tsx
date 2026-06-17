import {
  LoaderCircle,
} from "lucide-react";

import {
  Navigate,
  Outlet,
  useLocation,
} from "react-router";

import {
  useAdminAuth,
} from "../../contexts/AdminAuthContext";

export default function ProtectedAdminRoute() {
  const location = useLocation();

  const {
    admin,
    token,
    initializing,
  } = useAdminAuth();

  if (initializing) {
    return (
      <div className="admin-auth-state">
        <LoaderCircle
          className="spin"
          size={42}
        />

        <h2>
          Verifying administrator session
        </h2>
      </div>
    );
  }

  if (!token || !admin) {
    return (
      <Navigate
        to="/admin/login"
        replace
        state={{
          from:
            location.pathname +
            location.search,
        }}
      />
    );
  }

  return <Outlet />;
}