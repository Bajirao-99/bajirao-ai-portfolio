const ADMIN_TOKEN_STORAGE_KEY =
  "bajirao_portfolio_admin_token";

interface JwtPayload {
  exp?: number;
}

function decodeJwtPayload(
  token: string,
): JwtPayload | null {
  try {
    const tokenParts = token.split(".");

    if (tokenParts.length !== 3) {
      return null;
    }

    const encodedPayload = tokenParts[1]
      .replace(/-/g, "+")
      .replace(/_/g, "/");

    const paddedPayload =
      encodedPayload.padEnd(
        Math.ceil(
          encodedPayload.length / 4,
        ) * 4,
        "=",
      );

    const decodedPayload =
      window.atob(paddedPayload);

    return JSON.parse(
      decodedPayload,
    ) as JwtPayload;
  } catch {
    return null;
  }
}

export function isAdminTokenExpired(
  token: string,
): boolean {
  const payload = decodeJwtPayload(token);

  if (!payload?.exp) {
    return true;
  }

  const currentTimeInSeconds =
    Math.floor(Date.now() / 1000);

  return payload.exp <= currentTimeInSeconds;
}

export function storeAdminToken(
  token: string,
): void {
  sessionStorage.setItem(
    ADMIN_TOKEN_STORAGE_KEY,
    token,
  );
}

export function getStoredAdminToken():
  | string
  | null {
  const token = sessionStorage.getItem(
    ADMIN_TOKEN_STORAGE_KEY,
  );

  if (!token) {
    return null;
  }

  if (isAdminTokenExpired(token)) {
    clearAdminToken();
    return null;
  }

  return token;
}

export function clearAdminToken(): void {
  sessionStorage.removeItem(
    ADMIN_TOKEN_STORAGE_KEY,
  );
}