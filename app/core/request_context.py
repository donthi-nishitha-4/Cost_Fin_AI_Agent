from uuid import uuid4

from fastapi import Request #type:ignore

from app.core.logger import logger


async def request_context_middleware(request: Request, call_next):
    request_id = str(uuid4())

    logger.info(
        f"Request started: request_id={request_id} method={request.method} path={request.url.path}"
    )

    response = await call_next(request)

    response.headers["X-Request-ID"] = request_id

    logger.info(
        f"Request completed: request_id={request_id} status_code={response.status_code}"
    )

    return response