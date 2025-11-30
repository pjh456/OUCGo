# jwc_client/service.py
from .client import BaseJWCClient
from django.conf import settings


class JWCService:
    """
    高级封装：针对业务，处理缓存、哈希、字段抽象
    """

    def __init__(self, student_profile):
        self.profile = student_profile
        self.client = BaseJWCClient(
            student_profile.jwc_username, student_profile.jwc_password
        )

    def get_jwgl(self) -> str | None:
        success = self.client.fetch(settings.JWC_JWGL_URL)
        if success:
            return self.client.get_last_html()
        else:
            return None

    def get_schedule_table(self) -> str | None:
        success = self.client.fetch(settings.JWC_TABLE_URL)
        if success:
            return self.client.get_last_html()
        else:
            return None
