import { useEffect } from "react";
import { useLocation } from "react-router";

import { publicApi } from "../lib/api";

const VISITOR_KEY_NAME =
  "bajirao_portfolio_visitor_key";

function generateVisitorKey(): string {
  if (
    typeof crypto !== "undefined" &&
    typeof crypto.randomUUID === "function"
  ) {
    return crypto.randomUUID();
  }

  return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx"
    .replace(/[xy]/g, (character) => {
      const randomValue =
        Math.floor(Math.random() * 16);

      const replacement =
        character === "x"
          ? randomValue
          : (randomValue & 0x3) | 0x8;

      return replacement.toString(16);
    });
}

export function getVisitorKey(): string {
  const existingKey =
    localStorage.getItem(VISITOR_KEY_NAME);

  if (existingKey) {
    return existingKey;
  }

  const newKey = generateVisitorKey();

  localStorage.setItem(
    VISITOR_KEY_NAME,
    newKey,
  );

  return newKey;
}

function recentlyTracked(
  storageKey: string,
  minimumInterval = 2000,
): boolean {
  const currentTime = Date.now();

  const previousTime = Number(
    sessionStorage.getItem(storageKey) ?? "0",
  );

  if (
    currentTime - previousTime <
    minimumInterval
  ) {
    return true;
  }

  sessionStorage.setItem(
    storageKey,
    String(currentTime),
  );

  return false;
}

export function useAnalyticsTracker() {
  const location = useLocation();

  useEffect(() => {
    const pagePath =
      `${location.pathname}${location.search}`;

    const trackingKey =
      `bajirao_page_view:${pagePath}`;

    if (recentlyTracked(trackingKey)) {
      return;
    }

    void publicApi
      .trackPageView({
        visitor_key: getVisitorKey(),
        page_path: pagePath,
        referrer:
          document.referrer || null,
      })
      .catch(() => {
        // Analytics errors must not break the UI.
      });
  }, [
    location.pathname,
    location.search,
  ]);
}