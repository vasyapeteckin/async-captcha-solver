from abc import ABC, abstractmethod
from typing import Literal, Any


class AbstractHTTPClient(ABC):
    # session: Any

    @abstractmethod
    def __init__(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def request(self,
                      method: Literal['GET', 'POST'],
                      url: str,
                      payload: dict) -> dict:
        raise NotImplementedError

