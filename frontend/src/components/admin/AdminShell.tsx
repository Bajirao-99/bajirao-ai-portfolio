import {
  Bot,
  CalendarDays,
  ExternalLink,
  FilePenLine,
  LayoutDashboard,
  LogOut,
  Mail,
  Menu,
  ShieldCheck,
  X,
} from "lucide-react";

import {
  Link,
  NavLink,
  Outlet,
} from "react-router";

import {
  useState,
} from "react";

import {
  useAdminAuth,
} from "../../contexts/AdminAuthContext";

const navigationItems = [
  {
    label: "Dashboard",
    to: "/admin",
    icon: LayoutDashboard,
    end: true,
  },
  {
    label: "Contact Messages",
    to: "/admin/messages",
    icon: Mail,
  },
  {
    label: "Interview Requests",
    to: "/admin/interviews",
    icon: CalendarDays,
  },
  {
    label: "AI Activity",
    to: "/admin/ai-activity",
    icon: Bot,
  },
  {
    label: "Content Manager",
    to: "/admin/content",
    icon: FilePenLine,
  },
];

export default function AdminShell() {
  const [sidebarOpen, setSidebarOpen] =
    useState(false);

  const {
    admin,
    logout,
  } = useAdminAuth();

  return (
    <div className="admin-layout">
      <aside
        className={
          sidebarOpen
            ? "admin-sidebar admin-sidebar-open"
            : "admin-sidebar"
        }
      >
        <div className="admin-sidebar-header">
          <Link
            className="admin-brand"
            to="/admin"
          >
            <span>
              <ShieldCheck size={22} />
            </span>

            <div>
              <strong>
                Portfolio Admin
              </strong>

              <small>
                Management Console
              </small>
            </div>
          </Link>

          <button
            className="admin-sidebar-close"
            type="button"
            aria-label="Close admin sidebar"
            onClick={() => {
              setSidebarOpen(false);
            }}
          >
            <X size={21} />
          </button>
        </div>

        <nav className="admin-navigation">
          {navigationItems.map((item) => {
            const Icon = item.icon;

            return (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.end}
                onClick={() => {
                  setSidebarOpen(false);
                }}
                className={({
                  isActive,
                }) =>
                  isActive
                    ? "admin-nav-link admin-nav-link-active"
                    : "admin-nav-link"
                }
              >
                <Icon size={19} />
                {item.label}
              </NavLink>
            );
          })}
        </nav>

        <div className="admin-sidebar-footer">
          <Link
            className="admin-public-link"
            to="/"
            target="_blank"
          >
            <ExternalLink size={17} />
            Open Public Portfolio
          </Link>

          <button
            type="button"
            className="admin-logout-button"
            onClick={logout}
          >
            <LogOut size={18} />
            Logout
          </button>
        </div>
      </aside>

      {sidebarOpen && (
        <button
          type="button"
          className="admin-sidebar-overlay"
          aria-label="Close admin sidebar"
          onClick={() => {
            setSidebarOpen(false);
          }}
        />
      )}

      <div className="admin-main-area">
        <header className="admin-topbar">
          <button
            type="button"
            className="admin-menu-button"
            aria-label="Open admin sidebar"
            onClick={() => {
              setSidebarOpen(true);
            }}
          >
            <Menu size={23} />
          </button>

          <div className="admin-topbar-title">
            <span>
              Administration
            </span>

            <strong>
              Bajirao AI Portfolio
            </strong>
          </div>

          <div className="admin-user">
            <span className="admin-user-avatar">
              {admin?.username
                .charAt(0)
                .toUpperCase()}
            </span>

            <div>
              <strong>
                {admin?.username}
              </strong>

              <span>
                {admin?.email}
              </span>
            </div>
          </div>
        </header>

        <main className="admin-page-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}