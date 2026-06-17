from typing import Any

import httpx

from app.core.config import settings


GITHUB_API_BASE_URL = "https://api.github.com"
MAX_REPOSITORY_PAGES = 10
REPOSITORIES_PER_PAGE = 100


class GitHubAPIError(Exception):
    pass


def build_github_headers() -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": (
            settings.github_api_version
        ),
        "User-Agent": "Bajirao-AI-Portfolio",
    }

    if settings.github_token is not None:
        token = (
            settings.github_token
            .get_secret_value()
            .strip()
        )

        if token:
            headers["Authorization"] = (
                f"Bearer {token}"
            )

    return headers


def raise_github_error(
    response: httpx.Response,
) -> None:
    if response.status_code == 404:
        raise GitHubAPIError(
            "GitHub user was not found."
        )

    if response.status_code == 403:
        remaining = response.headers.get(
            "X-RateLimit-Remaining"
        )

        if remaining == "0":
            raise GitHubAPIError(
                "GitHub API rate limit exceeded. "
                "Add a GitHub token or retry later."
            )

        raise GitHubAPIError(
            "GitHub rejected the API request."
        )

    if response.status_code == 401:
        raise GitHubAPIError(
            "The configured GitHub token is invalid."
        )

    raise GitHubAPIError(
        "GitHub synchronization failed with "
        f"status code {response.status_code}."
    )


async def fetch_github_portfolio(
    username: str,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    headers = build_github_headers()

    timeout = httpx.Timeout(
        20.0,
        connect=10.0,
    )

    try:
        async with httpx.AsyncClient(
            base_url=GITHUB_API_BASE_URL,
            headers=headers,
            timeout=timeout,
            follow_redirects=True,
        ) as client:
            profile_response = await client.get(
                f"/users/{username}"
            )

            if not profile_response.is_success:
                raise_github_error(
                    profile_response
                )

            profile_data = (
                profile_response.json()
            )

            repositories: list[
                dict[str, Any]
            ] = []

            for page_number in range(
                1,
                MAX_REPOSITORY_PAGES + 1,
            ):
                repository_response = await client.get(
                    f"/users/{username}/repos",
                    params={
                        "type": "owner",
                        "sort": "updated",
                        "direction": "desc",
                        "per_page": (
                            REPOSITORIES_PER_PAGE
                        ),
                        "page": page_number,
                    },
                )

                if not repository_response.is_success:
                    raise_github_error(
                        repository_response
                    )

                page_repositories = (
                    repository_response.json()
                )

                if not isinstance(
                    page_repositories,
                    list,
                ):
                    raise GitHubAPIError(
                        "GitHub returned an invalid "
                        "repository response."
                    )

                repositories.extend(
                    page_repositories
                )

                if (
                    len(page_repositories)
                    < REPOSITORIES_PER_PAGE
                ):
                    break

            return (
                profile_data,
                repositories,
            )

    except GitHubAPIError:
        raise

    except httpx.TimeoutException as error:
        raise GitHubAPIError(
            "GitHub synchronization timed out."
        ) from error

    except httpx.HTTPError as error:
        raise GitHubAPIError(
            "Could not connect to the GitHub API."
        ) from error