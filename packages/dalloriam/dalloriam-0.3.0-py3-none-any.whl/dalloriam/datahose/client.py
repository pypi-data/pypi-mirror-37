import requests


class DatahoseClient:

    def __init__(self, service_host: str, password: str) -> None:
        self._push_url = service_host

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

    def notify(self, sender: str, message: str) -> None:
        data = {
            'sender': sender,
            'message': message
        }
        self.push('notification', data=data)
