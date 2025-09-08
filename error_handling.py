"""Error handling for the EnformionGO API wrapper."""

import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from exceptions import EnformionGOException

logger = logging.getLogger(__name__)


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handles HTTP exceptions.

    Args:
        request: The request.
        exc: The exception.

    Returns:
        The JSON response.
    """
    logger.error(f"HTTP Exception: {exc.detail}", exc_info=True)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def enformiongo_exception_handler(request: Request, exc: EnformionGOException):
    """Handles EnformionGO exceptions."""
    logger.error(f"EnformionGO Exception: {exc.detail}", exc_info=True)
    return JSONResponse(
        status_code=400,
        content={"detail": "An internal error occurred while processing the request."},
    )