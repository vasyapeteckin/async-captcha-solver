from async_captcha_solver.captcha_methods_mixin import CaptchaMethodsMixin
from async_captcha_solver.http_client.abc import AbstractHTTPClient


class AntiCaptchaClient(CaptchaMethodsMixin):
    base_url = "https://api.anti-captcha.com"

    def __init__(self, api_key, http_client: AbstractHTTPClient = None, logger=None):
        super().__init__(api_key=api_key, http_client=http_client, logger=logger)


class CapMonsterClient(CaptchaMethodsMixin):
    base_url = "https://api.capmonster.cloud"

    def __init__(self, api_key, http_client: AbstractHTTPClient = None, logger=None):
        super().__init__(api_key=api_key, http_client=http_client, logger=logger)


class TwoCaptchaClient(CaptchaMethodsMixin):
    base_url = "https://api.2captcha.com"

    def __init__(self, api_key, http_client: AbstractHTTPClient = None, logger=None):
        super().__init__(api_key=api_key, http_client=http_client, logger=logger)


__all__ = ['AntiCaptchaClient', 'CapMonsterClient', 'TwoCaptchaClient']
