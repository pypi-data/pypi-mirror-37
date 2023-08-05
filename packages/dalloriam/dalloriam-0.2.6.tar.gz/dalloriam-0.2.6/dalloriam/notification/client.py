import requests


class NotifierClient:

    def __init__(self, service_host: str, password: str) -> None:
        self._service_host = f'{service_host}/push'
        self._password = password

    def send(self, sender: str, body: str) -> None:
        resp = requests.post(
            self._service_host,
            json={
                'sender': sender,
                'message': body
            },
            headers={'Authorization': self._password}
        )

        if resp.status_code != 200:
            raise ValueError(resp.text)
