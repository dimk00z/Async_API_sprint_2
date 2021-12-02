import logging

from fastapi import FastAPI, Request, Response
from httpx import AsyncClient, RequestError

from core.config import AUTH_HOST

logger = logging.getLogger(__name__)


def apply_middleware(app: FastAPI):
    @app.middleware("http")
    async def check_auth(request: Request, call_next):
        headers = request.headers
        oauth2_service = headers["oauth2_service"] if "oauth2_service" in headers else ""

        auth_url = (
            f"{AUTH_HOST}/api/v1/login/"
            if oauth2_service == ""
            else f"{AUTH_HOST}/api/v1/auth/{oauth2_service}"
        )
        request.state.is_authenticated = True if await get_auth_answer(auth_url, headers) else False
        response = await call_next(request)
        return response


async def get_auth_answer(auth_url, headers):
    try:
        async with AsyncClient() as client:
            auth_answer = await client.get(auth_url, headers=dict(headers))
            logger.info(auth_answer)
        return auth_answer
    except RequestError:
        return
