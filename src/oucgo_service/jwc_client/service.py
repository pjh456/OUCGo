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

    def get_schedule(self):
        html = self.client.fetch(settings.JWC_SCHEDULE_URL)
        # 可选：计算 hash 与 last_html_hash 对比
        return html

    def get_grades(self):
        html = self.client.fetch(settings.JWC_GRADES_URL)
        return html
