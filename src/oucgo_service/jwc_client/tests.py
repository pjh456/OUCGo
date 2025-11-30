# jwc_client/tests.py
from django.test import TestCase
from .client import BaseJWCClient
from django.conf import settings
import unittest


class JWCClientTest(TestCase):
    def test_login(self):
        client = BaseJWCClient(settings.JWC_USERNAME, settings.JWC_PASSWORD)
        try:
            success = client.login()
            if not success:
                self.fail(f"登录失败: {client.get_last_error()}")
        except Exception as e:
            self.fail(f"登录失败: {e}")

    @unittest.skipIf(settings.SKIP_CI_TEST == "true", "CI 无法连接校园网")
    def test_jwgl(self):
        client = BaseJWCClient(settings.JWC_USERNAME, settings.JWC_PASSWORD)
        try:
            success = client.fetch(settings.JWC_JWGL_URL)
            if not success:
                self.fail(f"失败: {client.get_last_error()}")
        except Exception as e:
            self.fail(f"登录失败: {e}")
