# jwc_client/client.py
import requests
from django.conf import settings


class BaseJWCClient:
    """
    低级封装：只负责登录、抓取 HTML
    """

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.logged_in = False

    def login(self):
        resp = self.session.post(
            settings.JWC_LOGIN_URL,
            data={"username": self.username, "password": self.password},
            params={"noAutoRedirect": 1, "service": settings.JWC_SERVICE_URL},
        )
        if resp.status_code == 200 and "登录成功" in resp.text:
            self.logged_in = True
        else:
            self.logged_in = False

        return self.logged_in

    def fetch(self, url) -> str:
        if not self.logged_in:
            self.login()
        return self.session.get(url).text
