# jwc_client/tests.py
from django.test import TestCase
from .client import BaseJWCClient
from django.conf import settings
import unittest
from lxml import html

from .rule_node import RuleNode
from .html_extractor import HTMLExtractor


class JWCClientTest(TestCase):
    def setUp(self):
        self.jwc_client = BaseJWCClient(settings.JWC_USERNAME, settings.JWC_PASSWORD)

    def test_login(self):
        try:
            success = self.jwc_client.login()
            if not success:
                self.fail(f"登录失败: {self.jwc_client.get_last_error()}")
        except Exception as e:
            self.fail(f"登录失败: {e}")

    # @unittest.skipIf(settings.SKIP_CI_TEST == "true", "CI 无法连接校园网")
    def test_jwgl(self):
        try:
            success = self.jwc_client.fetch(settings.VPN_JWC_JWGL_URL)
            if not success:
                self.fail(f"课表访问失败: {self.jwc_client.get_last_error()}")
        except Exception as e:
            self.fail(f"课表访问失败: {e}")

    # @unittest.skipIf(settings.SKIP_CI_TEST == "true", "CI 无法连接校园网")
    # def test_jwgl_parse(self):
    #     try:
    #         success = self.jwc_client.fetch(settings.VPN_JWC_JWGL_URL)
    #         if not success:
    #             self.fail(f"课表解析失败: {self.jwc_client.get_last_error()}")
    #         html_text = self.jwc_client.get_last_html()
    #         extractor = HTMLExtractor()
    #     except Exception as e:
    #         self.fail(f"课表解析失败: {e}")


class HTMLExtractorTests(TestCase):
    def setUp(self):
        # HTML 测试样例
        self.html_text = """
        <dl class="layui-anim layui-anim-upbit">
            <dd lay-value="" class="layui-select-tips layui-this">全部</dd>
            <dd lay-value="1">第一周</dd>
            <dd lay-value="2">第二周</dd>
        </dl>
        """

        # 配置字典
        self.config_dict = {
            "weeks": {
                "match": {
                    "tag": "dl",
                    "attrs": {"class": "layui-anim layui-anim-upbit"},
                },
                "value": {
                    "list": {
                        "name": {"match": {"tag": "dd"}, "value": {"text": True}},
                        "value": {
                            "match": {"tag": "dd"},
                            "value": {"attr": "lay-value"},
                        },
                    }
                },
            },
            "show_online_courses": {"value": {"const": "false"}},
        }

        # 构建规则树
        self.config_tree = self.config_tree = {
            k: RuleNode.from_config(v) for k, v in self.config_dict.items()
        }

        self.extractor = HTMLExtractor()

    def test_rule_node_structure(self) -> None:
        weeks_node = self.config_tree["weeks"]
        self.assertIn("name", weeks_node.children)
        self.assertIn("value", weeks_node.children)
        self.assertEqual(weeks_node.children["name"].value["text"], True)
        self.assertEqual(weeks_node.children["value"].value["attr"], "lay-value")

    def test_rule_node_xpath(self) -> None:
        weeks_node = self.config_tree["weeks"]
        tree = html.fragment_fromstring(self.html_text, create_parent=True)
        for node in weeks_node.traverse():
            elements = node.find_in(tree)
            self.assertIsInstance(elements, list)
            self.assertGreater(len(elements), 0)

    def test_extractor(self) -> None:
        result = self.extractor.extract_from_html(self.html_text, self.config_tree)
        self.assertEqual(len(result["weeks"]), 3)
        self.assertEqual(len(result["show_online_courses"]), 1)
        self.assertEqual(result["show_online_courses"][0], "false")

    @unittest.skipIf(settings.SKIP_CI_TEST == "true", "配置文件已隐藏")
    def test_config_load(self) -> None:
        try:
            self.extractor.load_config(settings.CLASS_TABLE_PARAMS_PATH)
        except Exception as e:
            self.fail(f"配置失败: {e}")
