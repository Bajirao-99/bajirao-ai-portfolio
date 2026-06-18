import { Analytics } from "@vercel/analytics/react";

import { SpeedInsights } from "@vercel/speed-insights/react";

import {
  StrictMode,
} from "react";

import {
  createRoot,
} from "react-dom/client";

import {
  BrowserRouter,
} from "react-router";

import App from "./App";

import {
  AdminAuthProvider,
} from "./contexts/AdminAuthContext";

import "./index.css";

const rootElement =
  document.getElementById("root");

if (!rootElement) {
  throw new Error(
    "Root element was not found.",
  );
}

createRoot(rootElement).render(
  <StrictMode>
    <BrowserRouter>
      <AdminAuthProvider>
        <App />
        <Analytics />
        <SpeedInsights />
      </AdminAuthProvider>
    </BrowserRouter>
  </StrictMode>,
);