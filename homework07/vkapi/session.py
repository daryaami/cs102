import time
import typing as tp

import requests
from requests.adapters import HTTPAdapter
# from requests.packages.urllib3.util.retry import Retry


class Session:
    """
    Сессия.

    :param base_url: Базовый адрес, на который будут выполняться запросы.
    :param timeout: Максимальное время ожидания ответа от сервера.
    :param max_retries: Максимальное число повторных запросов.
    :param backoff_factor: Коэффициент экспоненциального нарастания задержки.
    """

    def __init__(
        self,
        base_url: str,
        timeout: float = 5.0,
        max_retries: int = 3,
        backoff_factor: float = 0.3,
    ) -> None:
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def get(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        retries = 0
        while retries <= self.max_retries:
            try:
                response = requests.get(f"{self.base_url}/{url}", *args, timeout=self.timeout, **kwargs)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                if retries == self.max_retries:
                    raise e
                retries += 1
                delay = self.backoff_factor * (2 ** retries)
                time.sleep(delay)

    def post(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        retries = 0
        while retries <= self.max_retries:
            try:
                response = requests.post(f"{self.base_url}/{url}", *args, timeout=self.timeout, **kwargs)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                if retries == self.max_retries:
                    raise e
                retries += 1
                delay = self.backoff_factor * (2 ** retries)
                time.sleep(delay)