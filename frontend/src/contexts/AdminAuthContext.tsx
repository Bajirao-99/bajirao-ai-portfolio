import {
  createContext,
  type ReactNode,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";

import {
  clearAdminToken,
  getStoredAdminToken,
  storeAdminToken,
} from "../lib/adminAuth";

import { adminApi } from "../lib/adminApi";

import type {
  AdminUser,
} from "../types/admin";

interface AdminAuthContextValue {
  admin: AdminUser | null;
  token: string | null;
  initializing: boolean;
  login: (
    username: string,
    password: string,
  ) => Promise<void>;
  logout: () => void;
}

const AdminAuthContext =
  createContext<
    AdminAuthContextValue | undefined
  >(undefined);

export function AdminAuthProvider({
  children,
}: {
  children: ReactNode;
}) {
  const [token, setToken] =
    useState<string | null>(() =>
      getStoredAdminToken(),
    );

  const [admin, setAdmin] =
    useState<AdminUser | null>(null);

  const [initializing, setInitializing] =
    useState(true);

  useEffect(() => {
    let cancelled = false;

    async function validateToken() {
      if (!token) {
        if (!cancelled) {
          setAdmin(null);
          setInitializing(false);
        }

        return;
      }

      setInitializing(true);

      try {
        const currentAdmin =
          await adminApi.getCurrentAdmin(
            token,
          );

        if (!cancelled) {
          setAdmin(currentAdmin);
        }
      } catch {
        clearAdminToken();

        if (!cancelled) {
          setToken(null);
          setAdmin(null);
        }
      } finally {
        if (!cancelled) {
          setInitializing(false);
        }
      }
    }

    void validateToken();

    return () => {
      cancelled = true;
    };
  }, [token]);

  async function login(
    username: string,
    password: string,
  ): Promise<void> {
    const tokenResponse =
      await adminApi.login(
        username,
        password,
      );

    storeAdminToken(
      tokenResponse.access_token,
    );

    setInitializing(true);
    setToken(tokenResponse.access_token);
  }

  function logout(): void {
    clearAdminToken();
    setToken(null);
    setAdmin(null);
    setInitializing(false);
  }

  const contextValue = useMemo(
    () => ({
      admin,
      token,
      initializing,
      login,
      logout,
    }),
    [admin, token, initializing],
  );

  return (
    <AdminAuthContext.Provider
      value={contextValue}
    >
      {children}
    </AdminAuthContext.Provider>
  );
}

export function useAdminAuth() {
  const context =
    useContext(AdminAuthContext);

  if (!context) {
    throw new Error(
      "useAdminAuth must be used inside AdminAuthProvider.",
    );
  }

  return context;
}