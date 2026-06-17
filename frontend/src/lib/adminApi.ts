import {
  API_BASE_URL,
  ApiError,
} from "./api";

import type {
  AdminTokenResponse,
  AdminUser,
  AnalyticsDashboard,
  ChatInteractionHistory,
  ContactMessageAdmin,
  InterviewRequestAdmin,
  JobMatchHistory,
} from "../types/admin";

async function parseResponse<T>(
  response: Response,
): Promise<T> {
  if (response.status === 204) {
    return undefined as T;
  }

  const payload = await response
    .json()
    .catch(() => null);

  if (!response.ok) {
    let message =
      `Request failed with status ${response.status}.`;

    if (
      payload &&
      typeof payload === "object" &&
      "detail" in payload &&
      typeof payload.detail === "string"
    ) {
      message = payload.detail;
    }

    throw new ApiError(
      message,
      response.status,
    );
  }

  return payload as T;
}

export async function authenticatedRequest<T>(
  path: string,
  token: string,
  options: RequestInit = {},
): Promise<T> {
  const headers = new Headers(
    options.headers,
  );

  headers.set(
    "Authorization",
    `Bearer ${token}`,
  );

  if (
    options.body &&
    !(options.body instanceof FormData) &&
    !(options.body instanceof URLSearchParams) &&
    !headers.has("Content-Type")
  ) {
    headers.set(
      "Content-Type",
      "application/json",
    );
  }

  const response = await fetch(
    `${API_BASE_URL}${path}`,
    {
      ...options,
      headers,
    },
  );

  return parseResponse<T>(response);
}

function createQuery(
  values: Record<
    string,
    string | number | null | undefined
  >,
): string {
  const parameters =
    new URLSearchParams();

  for (const [key, value] of Object.entries(
    values,
  )) {
    if (
      value !== null &&
      value !== undefined &&
      String(value).length > 0
    ) {
      parameters.set(key, String(value));
    }
  }

  const query = parameters.toString();

  return query ? `?${query}` : "";
}

export const adminApi = {
  async login(
    username: string,
    password: string,
  ): Promise<AdminTokenResponse> {
    const formData =
      new URLSearchParams();

    formData.set("username", username);
    formData.set("password", password);

    const response = await fetch(
      `${API_BASE_URL}/api/v1/auth/login`,
      {
        method: "POST",
        headers: {
          "Content-Type":
            "application/x-www-form-urlencoded",
        },
        body: formData,
      },
    );

    return parseResponse<AdminTokenResponse>(
      response,
    );
  },

  getCurrentAdmin(
    token: string,
  ) {
    return authenticatedRequest<AdminUser>(
      "/api/v1/auth/me",
      token,
    );
  },

  getAnalytics(
    token: string,
    days = 30,
  ) {
    return authenticatedRequest<AnalyticsDashboard>(
      `/api/v1/admin/analytics${createQuery({
        days,
      })}`,
      token,
    );
  },

  getContactMessages(
    token: string,
    status?: string,
  ) {
    return authenticatedRequest<
      ContactMessageAdmin[]
    >(
      `/api/v1/admin/contact-messages${createQuery({
        status,
        limit: 200,
        offset: 0,
      })}`,
      token,
    );
  },

  updateContactMessage(
    token: string,
    messageId: number,
    data: {
      status?: string;
      admin_notes?: string | null;
    },
  ) {
    return authenticatedRequest<ContactMessageAdmin>(
      `/api/v1/admin/contact-messages/${messageId}`,
      token,
      {
        method: "PUT",
        body: JSON.stringify(data),
      },
    );
  },

  deleteContactMessage(
    token: string,
    messageId: number,
  ) {
    return authenticatedRequest<void>(
      `/api/v1/admin/contact-messages/${messageId}`,
      token,
      {
        method: "DELETE",
      },
    );
  },

  getInterviewRequests(
    token: string,
    status?: string,
  ) {
    return authenticatedRequest<
      InterviewRequestAdmin[]
    >(
      `/api/v1/admin/interview-requests${createQuery({
        status,
        limit: 200,
        offset: 0,
      })}`,
      token,
    );
  },

  updateInterviewRequest(
    token: string,
    requestId: number,
    data: {
      status?: string;
      admin_notes?: string | null;
      preferred_datetime?: string | null;
    },
  ) {
    return authenticatedRequest<InterviewRequestAdmin>(
      `/api/v1/admin/interview-requests/${requestId}`,
      token,
      {
        method: "PUT",
        body: JSON.stringify(data),
      },
    );
  },

  deleteInterviewRequest(
    token: string,
    requestId: number,
  ) {
    return authenticatedRequest<void>(
      `/api/v1/admin/interview-requests/${requestId}`,
      token,
      {
        method: "DELETE",
      },
    );
  },

  getJobMatchHistory(
    token: string,
  ) {
    return authenticatedRequest<
      JobMatchHistory[]
    >(
      "/api/v1/admin/job-match-analyses?limit=200&offset=0",
      token,
    );
  },

  deleteJobMatchAnalysis(
    token: string,
    analysisId: number,
  ) {
    return authenticatedRequest<void>(
      `/api/v1/admin/job-match-analyses/${analysisId}`,
      token,
      {
        method: "DELETE",
      },
    );
  },

  getChatInteractions(
    token: string,
  ) {
    return authenticatedRequest<
      ChatInteractionHistory[]
    >(
      "/api/v1/admin/chat-interactions?limit=200&offset=0",
      token,
    );
  },

  deleteChatInteraction(
    token: string,
    interactionId: number,
  ) {
    return authenticatedRequest<void>(
      `/api/v1/admin/chat-interactions/${interactionId}`,
      token,
      {
        method: "DELETE",
      },
    );
  },
};