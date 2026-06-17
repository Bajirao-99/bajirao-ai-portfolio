import time
from uuid import uuid4

from fastapi import Request
from starlette.middleware.base import (
    BaseHTTPMiddleware,
)
from starlette.responses import Response


class SecurityHeadersMiddleware(
    BaseHTTPMiddleware
):
    def __init__(
        self,
        app,
        environment: str = "development",
    ):
        super().__init__(app)
        self.environment = (
            environment.lower().strip()
        )

    async def dispatch(
        self,
        request: Request,
        call_next,
    ) -> Response:
        request_id = request.headers.get(
            "X-Request-ID",
            str(uuid4()),
        )

        start_time = time.perf_counter()

        response = await call_next(request)

        processing_time = (
            time.perf_counter() - start_time
        )

        response.headers[
            "X-Request-ID"
        ] = request_id

        response.headers[
            "X-Process-Time"
        ] = f"{processing_time:.4f}"

        response.headers[
            "X-Content-Type-Options"
        ] = "nosniff"

        response.headers[
            "X-Frame-Options"
        ] = "DENY"

        response.headers[
            "Referrer-Policy"
        ] = "strict-origin-when-cross-origin"

        response.headers[
            "Permissions-Policy"
        ] = (
            "camera=(), "
            "microphone=(), "
            "geolocation=()"
        )

        if (
            self.environment == "production"
            and request.url.scheme == "https"
        ):
            response.headers[
                "Strict-Transport-Security"
            ] = (
                "max-age=31536000; "
                "includeSubDomains"
            )

        return response