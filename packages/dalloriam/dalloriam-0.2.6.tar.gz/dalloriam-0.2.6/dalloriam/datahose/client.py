import requests


class DatahoseClient:

    def __init__(self, service_host: str, password: str) -> None:
        self._push_url = f'{service_host}/event'
        self._flush_url = f'{service_host}/flush'

        self._headers = {
            'Authorization': password
        }

    def push(self, key: str, data: dict, time: float = None) -> None:
        data = {
            'key': key,
            'body': data
        }
        if time is not None:
            data['time'] = time

        resp = requests.post(self._push_url, json=data, headers=self._headers)

        if resp.status_code != 200:
            raise ValueError(resp.text)

    def flush(self) -> None:
        resp = requests.post(self._flush_url, headers=self._headers)
        if resp.status_code != 200:
            raise ValueError(resp.text)
