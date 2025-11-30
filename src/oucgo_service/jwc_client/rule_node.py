from __future__ import annotations
from typing import Optional, Dict, Any
from lxml import html


# -----------------------
# 规则节点类型声明
# -----------------------
class RuleNode:
    """
    HTML 配置驱动解析规则节点
    """

    def __init__(
        self,
        match: Optional[Dict[str, Any]] = None,
        value: Optional[Dict[str, Any]] = None,
        children: Optional[Dict[str, RuleNode]] = None,
    ):
        self.match: Dict[str, Any] = match or {}
        self.value: Dict[str, Any] = value or {}
        self.children: Dict[str, RuleNode] = children or {}

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> RuleNode:
        """
        根据配置字典递归创建 RuleNode 树
        """
        match = config.get("match")
        value = config.get("value")
        children = {}

        # 如果 value 是 list 字段，递归生成子节点
        if value and "list" in value and isinstance(value["list"], dict):
            for k, v in value["list"].items():
                children[k] = cls.from_config(v)

        return cls(match=match, value=value, children=children)

    def to_xpath(self) -> str:
        """
        将 match dict 转换为 xpath
        支持 tag + attrs
        """
        tag = self.match.get("tag", "*")
        attrs = self.match.get("attrs", {})
        xpath = f"//{tag}"
        if attrs:
            conditions = [f"@{k}='{v}'" for k, v in attrs.items()]
            xpath += "[" + " and ".join(conditions) + "]"
        return xpath

    def find_in(self, element):
        """
        在 lxml element 中查找符合规则的节点
        """
        xpath = self.to_xpath()
        return element.xpath(xpath)

    def traverse(self, include_self=True):
        """深度优先遍历自身及子节点，生成 RuleNode 对象"""
        if include_self:
            yield self
        for child in self.children.values():
            yield from child.traverse()

    def __repr__(self) -> str:
        return (
            f"RuleNode(match={self.match}, value={self.value}, "
            f"children={list(self.children.keys())})"
        )

    def __str__(self) -> str:
        return self._str(indent=0)

    def _str(self, indent: int = 0) -> str:
        pad = "  " * indent
        s = f"{pad}- match: {self.match}, value: {self.value}\n"
        for k, child in self.children.items():
            s += f"{pad}  [{k}]:\n{child._str(indent + 2)}"
        return s
