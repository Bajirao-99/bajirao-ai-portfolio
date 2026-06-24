import os
import sys

import httpx


API_BASE_URL = os.getenv(
    "PRODUCTION_API_BASE_URL",
    "https://api.bajiraosalunke.com",
).rstrip("/")


def check_endpoint(path: str) -> None:
    url = f"{API_BASE_URL}{path}"

    response = httpx.get(
        url,
        timeout=30.0,
    )

    print(
        f"{response.status_code} {url}"
    )

    if response.status_code != 200:
        print(response.text)
        raise SystemExit(1)


def main() -> None:
    endpoints = [
        "/api/v1/health",
        "/api/v1/ready",
        "/api/v1/profile",
    ]

    for endpoint in endpoints:
        check_endpoint(endpoint)

    print(
        "Production API smoke test passed."
    )


if __name__ == "__main__":
    try:
        main()
    except httpx.HTTPError as error:
        print(
            f"HTTP error: {error}",
            file=sys.stderr,
        )
        raise SystemExit(1)