from typing_extensions import Self
from lxml import html
from .rule_node import RuleNode
from typing import Optional, Dict, Any
import json


class HTMLExtractor:
    _instance: Optional["HTMLExtractor"] | None = None
    config_tree: Dict[str, "RuleNode"]

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.config_tree = {}
        return cls._instance

    def load_config(self, config_path: str) -> None:
        with open(config_path, "r") as f:
            self.config_tree = json.load(f)

    def extract_from_html(
        self, root_html: str, config_tree: Optional[Dict[str, "RuleNode"]]
    ) -> Dict[str, Any]:
        """
        从 HTML 字符串和配置树提取数据
        """
        if config_tree is not None:
            self.config_tree = config_tree
        if len(self.config_tree) == 0:
            return {}

        root_elements = html.fragments_fromstring(root_html)
        # 过滤非 HtmlElement
        root_elements = [e for e in root_elements if isinstance(e, html.HtmlElement)]

        result = {}
        for key, node in self.config_tree.items():
            extracted = []
            for el in root_elements:
                val = self._extract_node(node, el)
                if val is None:
                    continue
                if isinstance(val, list):
                    extracted.extend(val)
                else:
                    extracted.append(val)
            result[key] = extracted
        return result

    def _extract_node(self, node: "RuleNode", element) -> Any:
        """
        递归提取单个节点
        """
        nodes = node.find_in(element)
        if not nodes:
            return None

        if "const" in node.value:
            return node.value["const"]

        if node.value.get("text") is True:
            return [n.text_content() for n in nodes]

        if "attr" in node.value:
            attr_name = node.value["attr"]
            return [n.get(attr_name) for n in nodes]

        if "list" in node.value and node.children:
            # 先提取所有子字段
            child_results = {}
            max_len = 0
            for k, child in node.children.items():
                vals = self._extract_node(child, element)
                if not isinstance(vals, list):
                    vals = [vals]
                child_results[k] = vals
                max_len = max(max_len, len(vals))

            # 按索引组合成字典列表
            merged = []
            for i in range(max_len):
                item = {}
                for k, vals in child_results.items():
                    item[k] = vals[i] if i < len(vals) else None
                merged.append(item)
            return merged

        return nodes
