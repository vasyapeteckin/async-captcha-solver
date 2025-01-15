from typing import Literal

from async_captcha_solver.http_client.abc import AbstractHTTPClient
from async_captcha_solver.abc import AbstractCaptchaClient
from async_captcha_solver.captcha_services import AntiCaptchaClient, CapMonsterClient, TwoCaptchaClient


class CaptchaSolver:
    __SUPPORTED_SERVICES = '2captcha', 'capmonster', 'anticaptcha'

    def __init__(self,
                 service: Literal['2captcha', 'capmonster', 'anticaptcha'],
                 api_key: str,
                 http_client: AbstractHTTPClient = None,
                 logger=None
                 ):
        """
        Initializes a CaptchaSolver instance for interacting with a captcha-solving service.

        :param service: The captcha service to use. Can be one of the following:
                        '2captcha', 'capmonster', 'anticaptcha'.
        :param api_key: The API key used to authenticate requests to the selected captcha service.
        :param http_client: An optional HTTP client instance to manage HTTP requests. If not provided,
                            a default HTTP client will be used.
        :param logger: An optional logger instance to capture logs. If not provided, a default logging will be used.

        :raises ValueError: If the provided `service` is not supported (i.e., not in the list of
                             '2captcha', 'capmonster', or 'anticaptcha').
        :raises RuntimeError: If initializing the client for the selected service fails for any reason.
        """

        self._service = service
        self.api_key = api_key
        self.http_client = http_client
        self.logger = logger

        if service not in self.__SUPPORTED_SERVICES:
            raise ValueError(f"Unsupported service: {service}. Supported services: {self.__SUPPORTED_SERVICES}")

        client_mapping = {
            'anticaptcha': AntiCaptchaClient,
            'capmonster': CapMonsterClient,
            '2captcha': TwoCaptchaClient,
        }
        try:
            self.client: AbstractCaptchaClient = client_mapping[self._service](api_key=api_key,
                                                                               http_client=http_client,
                                                                               logger=logger)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize client for service '{service}': {e}")

    @property
    def service(self) -> str:
        return self._service
