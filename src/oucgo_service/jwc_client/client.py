# jwc_client/client.py
import requests
from django.conf import settings


class BaseJWCClient:
    """
    低级封装：只负责登录、抓取 HTML
    状态可查询，方法只返回 bool
    """

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.logged_in = False

        self.last_response_html: str | None = None
        self.last_status: int | None = None
        self.last_error: str | None = None

    def login(self) -> bool:
        """登录教务系统，返回 True/False"""
        try:
            resp = self.session.post(
                settings.JWC_LOGIN_URL,
                data={"username": self.username, "password": self.password},
                params={"noAutoRedirect": 1, "service": settings.JWC_LOGIN_URL},
            )
            self.last_status = resp.status_code
            if resp.status_code == 200:
                self.logged_in = True
                self.last_response_html = resp.text
                self.last_error = None
                return True
            else:
                self.last_response_html = None
                self.last_error = f"登录失败, 状态码 {resp.status_code}"
                return False
        except Exception as e:
            self.last_error = str(e)
            return False

    def fetch(self, url: str) -> bool:
        """抓取指定 URL，返回是否成功"""
        if not self.logged_in:
            if not self.login():  # 尝试登录
                return False

        try:
            resp = self.session.get(url)
            if resp.status_code == 200:
                self.last_response_html = resp.text
                self.last_status = True
                self.last_error = None
                return True
            else:
                self.last_status = False
                self.last_error = f"请求失败, 状态码 {resp.status_code}"
                return False
        except Exception as e:
            self.last_status = False
            self.last_error = str(e)
            return False

    # 可选：提供方法查询上次请求结果
    def get_last_html(self):
        return self.last_response_html

    def get_last_status(self):
        return self.last_status

    def get_last_error(self):
        return self.last_error
