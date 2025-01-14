import asyncio
import json
import logging
from json import JSONDecodeError
from typing import Literal

from aiohttp import ClientSession, ContentTypeError

from captcha_solver.http_client.abc import AbstractHTTPClient


class AiohttpClient(AbstractHTTPClient):
    def __init__(self, **kwargs):
        self.session: ClientSession = ClientSession(**kwargs)
        self.logger = logging.getLogger(f"captcha_solver.{self.__class__.__name__}")

    async def request(self, method: Literal['GET', 'POST'], url: str, payload: dict, **kwargs) -> dict:
        result = {}
        async with self.session.request(method, url, json=payload, **kwargs) as resp:
            try:
                json_response = await resp.json()
                result = json_response
            except ContentTypeError as e:
                try:
                    data = await resp.text()
                    data = json.loads(data)
                    result = data
                except JSONDecodeError as e:
                    self.logger.error(f"{str(e)}: {data}")
        self.logger.debug(result)
        return result

    async def close(self):
        if not self.session.closed:
            await self.session.close()

    def __del__(self):
        if not self.session.closed:
            try:
                asyncio.create_task(self.close())
            except:
                pass
