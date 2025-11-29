# jwc_parser/engine.py
from lxml import etree


def parse_schedule(html):
    tree = etree.HTML(html)
    rows = tree.xpath("//table[@id='schedule']//tr")
    result = []
    for r in rows[1:]:
        cols = r.xpath(".//td/text()")
        result.append({"course": cols[0], "time": cols[1], "teacher": cols[2]})
    return result
