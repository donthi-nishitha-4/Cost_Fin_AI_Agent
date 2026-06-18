from fastapi import Request #type:ignore
from fastapi.responses import JSONResponse #type:ignore

from app.core.logger import logger


async def global_exception_handler(request: Request, exc: Exception):
    logger.error(
        f"Unhandled error on {request.method} {request.url.path}: {str(exc)}"
    )

    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal server error"
        }
    )