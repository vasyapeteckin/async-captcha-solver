import asyncio
from abc import ABC, abstractmethod
from typing import Literal


class AbstractCaptchaClient(ABC):

    def __init__(self, api_key: str):
        self.api_key = api_key
        self._id_key = 'taskId'
        self._retry_count = 10
        self._delay = 5

        if self.api_key is None:
            raise ValueError('API key is missing')


    @abstractmethod
    async def test(self):
        raise NotImplementedError

    @abstractmethod
    async def get_balance(self):
        raise NotImplementedError

    @abstractmethod
    async def _create_task(self, task_payload: dict) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def _get_task_result(self, task_id: str | int) -> dict:
        raise NotImplementedError

    async def _solve(self, task_payload: dict) -> tuple[bool, dict]:
        retry_count = 0

        task = await self._create_task(task_payload=task_payload)

        if task.get('errorId') != 0:
            return False, task

        while True:
            retry_count += 1

            if retry_count == self._retry_count:
                return False, {'RETRY_COUNT': retry_count}

            result = await self._get_task_result(task_id=task.get(self.id_key))
            if result.get('status') == 'ready':
                return True, result

            await asyncio.sleep(self._delay)

    @abstractmethod
    async def _report_incorrect_solve(self):
        raise NotImplementedError

    @abstractmethod
    async def image_to_text(self,
                            image: str,
                            phrase: bool = False,
                            case: bool = True,
                            numeric: Literal[0, 1, 2, 3, 4] = 0,
                            math: bool = False,
                            min_length: int = 0,
                            max_length: int = 0,
                            comment: str = None,
                            **kwargs) -> tuple[bool, dict]:
        raise NotImplementedError

    @abstractmethod
    async def recaptcha_v2(self,
                           website_url: str,
                           website_key: str,
                           is_invisible: bool = False,
                           proxy_string: str = None,
                           **kwargs) -> tuple[bool, dict]:
        raise NotImplementedError

    @abstractmethod
    async def recaptcha_v3(self,
                           website_url: str,
                           website_key: str,
                           page_action: str,
                           proxy_string: str = None,
                           **kwargs) -> tuple[bool, dict]:
        raise NotImplementedError

    @abstractmethod
    async def turnstile(self,
                        website_url: str,
                        website_key: str,
                        page_action: str,
                        ) -> tuple[bool, dict]:
        raise NotImplementedError

    @property
    def delay(self):
        return self._delay

    @delay.setter
    def delay(self, value):
        self._delay = value

    @property
    def retry_count(self):
        return self._retry_count

    @retry_count.setter
    def retry_count(self, value):
        self._retry_count = value

    @property
    def id_key(self):
        return self._id_key

