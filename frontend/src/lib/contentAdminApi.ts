import {
  API_BASE_URL,
  ApiError,
} from "./api";

import {
  authenticatedRequest,
} from "./adminApi";

import type {
  ProjectImage,
  Resume,
} from "../types/portfolio";

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
      "detail" in payload
    ) {
      const detail = payload.detail;

      if (typeof detail === "string") {
        message = detail;
      }
    }

    throw new ApiError(
      message,
      response.status,
    );
  }

  return payload as T;
}

async function uploadRequest<T>(
  path: string,
  token: string,
  formData: FormData,
  method = "POST",
): Promise<T> {
  const response = await fetch(
    `${API_BASE_URL}${path}`,
    {
      method,
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: formData,
    },
  );

  return parseResponse<T>(response);
}

export const contentAdminApi = {
  create<T>(
    token: string,
    endpoint: string,
    data: Record<string, unknown>,
  ) {
    return authenticatedRequest<T>(
      endpoint,
      token,
      {
        method: "POST",
        body: JSON.stringify(data),
      },
    );
  },

  update<T>(
    token: string,
    endpoint: string,
    recordId: number,
    data: Record<string, unknown>,
  ) {
    return authenticatedRequest<T>(
      `${endpoint}/${recordId}`,
      token,
      {
        method: "PUT",
        body: JSON.stringify(data),
      },
    );
  },

  remove(
    token: string,
    endpoint: string,
    recordId: number,
  ) {
    return authenticatedRequest<void>(
      `${endpoint}/${recordId}`,
      token,
      {
        method: "DELETE",
      },
    );
  },

  uploadProjectImage(
    token: string,
    projectId: number,
    data: {
      file: File;
      altText: string;
      caption: string;
      displayOrder: number;
    },
  ) {
    const formData = new FormData();

    formData.set("file", data.file);
    formData.set(
      "alt_text",
      data.altText,
    );
    formData.set(
      "caption",
      data.caption,
    );
    formData.set(
      "display_order",
      String(data.displayOrder),
    );

    return uploadRequest<ProjectImage>(
      `/api/v1/projects/${projectId}/upload-image`,
      token,
      formData,
    );
  },

  deleteProjectImage(
    token: string,
    imageId: number,
  ) {
    return authenticatedRequest<void>(
      `/api/v1/projects/images/${imageId}`,
      token,
      {
        method: "DELETE",
      },
    );
  },

  uploadResume(
    token: string,
    data: {
      title: string;
      resumeType: string;
      description: string;
      displayOrder: number;
      isVisible: boolean;
      file: File;
    },
  ) {
    const formData = new FormData();

    formData.set("title", data.title);
    formData.set(
      "resume_type",
      data.resumeType,
    );
    formData.set(
      "description",
      data.description,
    );
    formData.set(
      "display_order",
      String(data.displayOrder),
    );
    formData.set(
      "is_visible",
      String(data.isVisible),
    );
    formData.set("file", data.file);

    return uploadRequest<Resume>(
      "/api/v1/resumes",
      token,
      formData,
    );
  },

  updateResume(
    token: string,
    resumeId: number,
    data: {
      title?: string;
      resume_type?: string;
      description?: string | null;
      display_order?: number;
      is_visible?: boolean;
    },
  ) {
    return authenticatedRequest<Resume>(
      `/api/v1/resumes/${resumeId}`,
      token,
      {
        method: "PUT",
        body: JSON.stringify(data),
      },
    );
  },

  replaceResumeFile(
    token: string,
    resumeId: number,
    file: File,
  ) {
    const formData = new FormData();

    formData.set("file", file);

    return uploadRequest<Resume>(
      `/api/v1/resumes/${resumeId}/file`,
      token,
      formData,
      "PUT",
    );
  },

  deleteResume(
    token: string,
    resumeId: number,
  ) {
    return authenticatedRequest<void>(
      `/api/v1/resumes/${resumeId}`,
      token,
      {
        method: "DELETE",
      },
    );
  },
};