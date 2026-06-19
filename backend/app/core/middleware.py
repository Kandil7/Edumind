import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.core.logging import request_id_var, get_logger

logger = get_logger("middleware")


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Assigns a unique request ID to every incoming request."""

    async def dispatch(self, request: Request, call_next):
        req_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request_id_var.set(req_id)

        start = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start

        response.headers["X-Request-ID"] = req_id
        response.headers["X-Response-Time"] = f"{duration:.3f}s"

        logger.info(
            "%s %s -> %s (%.3fs)",
            request.method,
            request.url.path,
            response.status_code,
            duration,
        )

        return response


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    """Catches unhandled exceptions and returns structured JSON errors."""

    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as exc:
            logger.exception("Unhandled exception: %s", exc)
            return JSONResponse(
                status_code=500,
                content={
                    "error": "internal_server_error",
                    "detail": "An unexpected error occurred.",
                    "request_id": request_id_var.get("-"),
                },
            )
