import {
  useCallback,
  useEffect,
  useState,
} from "react";

import { publicApi } from "../lib/api";
import type {
  PortfolioData,
} from "../types/portfolio";

interface PortfolioState {
  data: PortfolioData | null;
  loading: boolean;
  error: string | null;
}

export function usePortfolioData() {
  const [state, setState] =
    useState<PortfolioState>({
      data: null,
      loading: true,
      error: null,
    });

  const loadPortfolio = useCallback(
    async (signal?: AbortSignal) => {
      setState((currentState) => ({
        ...currentState,
        loading: true,
        error: null,
      }));

      try {
        const data =
          await publicApi.getPortfolio(signal);

        setState({
          data,
          loading: false,
          error: null,
        });
      } catch (error) {
        if (
          error instanceof DOMException &&
          error.name === "AbortError"
        ) {
          return;
        }

        setState({
          data: null,
          loading: false,
          error:
            error instanceof Error
              ? error.message
              : "Could not load portfolio data.",
        });
      }
    },
    [],
  );

  useEffect(() => {
    const controller = new AbortController();

    void loadPortfolio(controller.signal);

    return () => {
      controller.abort();
    };
  }, [loadPortfolio]);

  return {
    ...state,
    refetch: () => loadPortfolio(),
  };
}