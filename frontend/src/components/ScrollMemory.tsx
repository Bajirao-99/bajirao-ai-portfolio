import {
  useEffect,
  useRef,
} from "react";

import {
  useLocation,
  useNavigationType,
} from "react-router";

const STORAGE_KEY =
  "bajirao-portfolio-scroll-positions";

function getPageKey(
  pathname: string,
  search: string,
): string {
  return `${pathname}${search}`;
}

function readPositions(): Record<string, number> {
  try {
    const stored =
      sessionStorage.getItem(
        STORAGE_KEY,
      );

    return stored
      ? JSON.parse(stored)
      : {};
  } catch {
    return {};
  }
}

function savePosition(
  key: string,
): void {
  const positions = readPositions();

  positions[key] = window.scrollY;

  sessionStorage.setItem(
    STORAGE_KEY,
    JSON.stringify(positions),
  );
}

function getSavedPosition(
  key: string,
): number {
  const positions = readPositions();

  return positions[key] ?? 0;
}

function restoreWithRetry(
  targetY: number,
): void {
  let attempts = 0;

  const maxAttempts = 25;

  const restore = () => {
    attempts += 1;

    window.scrollTo({
      top: targetY,
      left: 0,
      behavior: "auto",
    });

    const currentDifference = Math.abs(
      window.scrollY - targetY,
    );

    const pageReady =
      document.documentElement.scrollHeight >
      targetY + window.innerHeight / 2;

    if (
      currentDifference > 8 &&
      attempts < maxAttempts &&
      !pageReady
    ) {
      window.setTimeout(
        restore,
        100,
      );
      return;
    }

    if (
      attempts < 8 &&
      Math.abs(window.scrollY - targetY) > 8
    ) {
      window.setTimeout(
        restore,
        100,
      );
    }
  };

  window.setTimeout(
    restore,
    0,
  );

  window.setTimeout(
    restore,
    150,
  );

  window.setTimeout(
    restore,
    350,
  );

  window.setTimeout(
    restore,
    700,
  );

  window.setTimeout(
    restore,
    1200,
  );
}

function scrollToHashWithRetry(
  hash: string,
): void {
  const elementId = hash.replace(
    "#",
    "",
  );

  if (!elementId) {
    return;
  }

  let attempts = 0;

  const scroll = () => {
    attempts += 1;

    const element =
      document.getElementById(elementId);

    if (element) {
      element.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });

      return;
    }

    if (attempts < 20) {
      window.setTimeout(
        scroll,
        100,
      );
    }
  };

  scroll();
}

export default function ScrollMemory() {
  const location = useLocation();
  const navigationType =
    useNavigationType();

  const currentKeyRef =
    useRef(
      getPageKey(
        location.pathname,
        location.search,
      ),
    );

  useEffect(() => {
    if (
      "scrollRestoration" in
      window.history
    ) {
      window.history.scrollRestoration =
        "manual";
    }
  }, []);

  useEffect(() => {
    currentKeyRef.current = getPageKey(
      location.pathname,
      location.search,
    );
  }, [
    location.pathname,
    location.search,
  ]);

  useEffect(() => {
    let ticking = false;

    const handleScroll = () => {
      if (ticking) {
        return;
      }

      ticking = true;

      window.requestAnimationFrame(() => {
        savePosition(
          currentKeyRef.current,
        );

        ticking = false;
      });
    };

    const handlePageHide = () => {
      savePosition(
        currentKeyRef.current,
      );
    };

    window.addEventListener(
      "scroll",
      handleScroll,
      {
        passive: true,
      },
    );

    window.addEventListener(
      "pagehide",
      handlePageHide,
    );

    window.addEventListener(
      "beforeunload",
      handlePageHide,
    );

    return () => {
      savePosition(
        currentKeyRef.current,
      );

      window.removeEventListener(
        "scroll",
        handleScroll,
      );

      window.removeEventListener(
        "pagehide",
        handlePageHide,
      );

      window.removeEventListener(
        "beforeunload",
        handlePageHide,
      );
    };
  }, []);

  useEffect(() => {
    const pageKey = getPageKey(
      location.pathname,
      location.search,
    );

    if (location.hash) {
      scrollToHashWithRetry(
        location.hash,
      );
      return;
    }

    if (navigationType === "POP") {
      const savedY =
        getSavedPosition(pageKey);

      restoreWithRetry(savedY);
      return;
    }

    window.scrollTo({
      top: 0,
      left: 0,
      behavior: "auto",
    });
  }, [
    location.key,
    location.pathname,
    location.search,
    location.hash,
    navigationType,
  ]);

  return null;
}