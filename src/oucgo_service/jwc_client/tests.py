# jwc_client/tests.py
from django.test import TestCase
from .client import BaseJWCClient
from django.conf import settings


class JWCClientTest(TestCase):
    def test_login(self):
        client = BaseJWCClient(settings.JWC_USERNAME, settings.JWC_PASSWORD)
        try:
            success = client.login()
            if success:
                print("登录成功")
            else:
                self.fail(f"登录失败")
        except Exception as e:
            self.fail(f"登录失败: {e}")
