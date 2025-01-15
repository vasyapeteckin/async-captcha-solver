import logging
from typing import Literal

from async_captcha_solver.http_client.aiohttp_client import AiohttpClient
from async_captcha_solver.http_client.abc import AbstractHTTPClient
from async_captcha_solver.abc import AbstractCaptchaClient


class CaptchaMethodsMixin(AbstractCaptchaClient):
    base_url = None
    id_key = 'taskId'

    def __init__(self,
                 api_key: str,
                 http_client: AbstractHTTPClient = None,
                 logger=None):
        super().__init__(api_key=api_key)
        self.http_client = http_client or AiohttpClient()
        self.logger = logger or logging.getLogger(f"captcha_solver.{self.__class__.__name__}")
        # self.http_client.logger = self.logger

        if self.base_url is None:
            raise ValueError("Base URL must be set")

    async def test(self):
        response = await self.http_client.request(method="POST",
                                                  url=f"{self.base_url}/test",
                                                  payload={"clientKey": self.api_key})
        self.logger.debug(response)
        return response

    async def get_balance(self):
        response = await self.http_client.request(method="POST",
                                                  url=f"{self.base_url}/getBalance",
                                                  payload={"clientKey": self.api_key})
        self.logger.debug(response)
        return response

    async def _create_task(self, task_payload: dict):
        if not task_payload.get('proxy_string', False):
            task_payload.pop("proxy_string")
        payload = {
            "clientKey": self.api_key,
            "task": task_payload
        }
        response = await self.http_client.request(method="POST",
                                                  url=f"{self.base_url}/createTask",
                                                  payload=payload,
                                                  )
        return response

    async def _get_task_result(self, task_id: str | int) -> dict:
        response = await self.http_client.request(method="POST",
                                                  url=f"{self.base_url}/getTaskResult",
                                                  payload={"clientKey": self.api_key, 'taskId': task_id})
        return response

    async def _report_incorrect_solve(self):
        pass

    async def image_to_text(self,
                            image: str,
                            phrase: bool = False,
                            case: bool = True,
                            numeric: Literal[0, 1, 2, 3, 4] = 0,
                            math: bool = False,
                            min_length: int = 0,
                            max_length: int = 0,
                            comment: str = None,
                            **kwargs):
        task_payload = {
            "type": "ImageToTextTask",
            "body": image,
            "phrase": phrase,
            "case": case,
            "numeric": numeric,
            "math": math,
            "min_length": min_length,
            "max_length": max_length,
            "comment": comment,
        }
        return await self._solve(task_payload=task_payload)

    async def recaptcha_v2(self,
                           website_url: str,
                           website_key: str,
                           is_invisible: bool = False,
                           proxy_string: str = None,
                           **kwargs):
        task_payload = {
            "type": "RecaptchaV2TaskProxyless",
            "websiteURL": website_url,
            "websiteKey": website_key,
            "isInvisible": is_invisible,
            "proxy_string": proxy_string}
        return await self._solve(task_payload=task_payload)

    async def recaptcha_v3(self,
                           website_url: str,
                           website_key: str,
                           page_action: str,
                           proxy_string: str = None,
                           **kwargs):
        task_payload = {"website_url": website_url,
                        "website_key": website_key,
                        "page_action": page_action,
                        "proxy_string": proxy_string}
        return await self._solve(task_payload=task_payload)

    async def turnstile(self,
                        website_url: str,
                        website_key: str,
                        page_action: str):
        task_payload = {"website_url": website_url,
                        "website_key": website_key,
                        "page_action": page_action}
        return await self._solve(task_payload=task_payload)