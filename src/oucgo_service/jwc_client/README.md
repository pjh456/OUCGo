# 客户端技术使用说明文档

## 一、HTML 配置驱动解析器说明文档

### 1. 概述
该解析器是一种 **配置驱动的 HTML 数据抽取工具**，采用单例模式，全局统一使用。

核心思想：
- 输入 HTML 文本
- 根据配置文件定义的匹配规则抽取数据
- 支持常量、单值、列表、递归字段
- 列表内的每个字段可以独立定义 `match + value`，和外层结构一致
- 输出标准字典/JSON结构

解析器输出结构清晰，完全解耦 HTML 与业务字段。

### 2. 配置文件结构
解析器配置文件采用 JSON 形式，统一分为 `match` 和 `value` 两部分：

```json
{
  "字段名": {
    "match": { ... },
    "value": { ... }
  }
}
```

#### 字段说明
|字段|类型|说明|
|----|----|---|
|字段名|`string`|输出数据的 key|
|match|`dict`|定位 HTML 元素的规则|
|value|`dict`|提取该元素的数据规则，可为单值、列表或常量|

### 3. `match`：元素定位规则
`match` 定义如何在 HTML 文档中找到目标元素，采用结构化描述，避免使用绝对 XPath。

#### 3.1 字段说明
|字段|类型|说明|
|----|----|---|
|tag|`string`|HTML 标签名，如 `div`、`li`、`dd`|
|attrs|`dict`|属性匹配，如 `{ "name": "kbjcmsid" }`|
|contains|`list`|模糊匹配列表，匹配元素的 `class`、文本或任意属性，只要包含该字符串即匹配|

#### 3.2 示例
匹配一个 `class` 为 `layui-anim layui-anim-upbit` 的 `<dl>` 元素：
```json
"match": {
  "tag": "dl",
  "attrs": { "class": "layui-anim layui-anim-upbit" },
  "contains": []
}
```
匹配一个 `li` 元素，要求 `name="kbjcmsid"` 并且 `class` 或文本包含 `layui-this`：
```json
"match": {
  "tag": "li",
  "attrs": { "name": "kbjcmsid" },
  "contains": ["layui-this"]
}
```

### 4. `value`：数据抽取规则
`value` 定义如何从匹配到的元素中提取数据。支持以下类型：

#### 4.1 单值提取
|字段|说明|
|----|----|
|attr|提取元素的某个属性值|
|text|如果为 true，提取元素的文本内容|
|const|常量值，不依赖 HTML|

**示例**
```json
"value": { "attr": "data-value" }
```
```json
"value": { "text": true }
```
```json
"value": { "const": "false" }
```

#### 4.2 列表提取（递归）
列表内的每个字段都可以独立定义 `match + value`，和外层保持一致：
```json
"value": {
  "list": {
    "name": {
        "match": { "tag": "dd", "attrs": {}, "contains": [] },
        "value": { "text": true }
    },
    "value": {
      "match": { "tag": "dd", "attrs": {}, "contains": [] },
      "value": { "attr": "lay-value" }
    }
  }
}
```
**解析结果示例**
HTML：
```html
<dl class="layui-anim layui-anim-upbit">
    <dd lay-value="" class="layui-select-tips layui-this">全部</dd>
    <dd lay-value="1">第一周</dd>
    <dd lay-value="2">第二周</dd>
</dl>
```
解析结果：
```json
{
  "weeks": [
    { "name": "全部", "value": "" },
    { "name": "第一周", "value": "1" },
    { "name": "第二周", "value": "2" }
  ]
}
```

#### 4.3 嵌套列表
列表内的每个字段也可以使用 `list`，实现多层递归：
```json
"value": {
  "list": {
    "section_name": {
      "match": { "tag": "dl", "attrs": {} },
      "value": { "text": true }
    },
    "items": {
      "match": { "tag": "dl", "attrs": {} },
      "value": {
        "list": {
          "name": {
            "match": { "tag": "dd" },
            "value": { "text": true }
          },
          "value": {
            "match": { "tag": "dd" },
            "value": { "attr": "lay-value" }
          }
        }
      }
    }
  }
}
```

### 5. 配置器匹配规则总结
1. `match` 定位元素：`tag` + `attrs` + `contains`
2. `value` 抽取数据：`attr` / `text` / `const` / `list`
3. 列表字段独立 `match`/`value`：列表内的每个字段都可独立匹配和抽取
4. 递归一致性：列表内字段可以继续嵌套 `list`，实现任意深度解析
5. 常量字段：不依赖 HTML，直接返回 `value`
6. 统一风格：`match`/`value` 分离，方便维护、扩展和调试
7. 可扩展功能：支持 `formatter`、`regex`、`fallback`

## 附录：课表接口参数文档
|URL|请求方式|参数|示例|备注|
|---|-------|----|----|----|
|JWC_TABLE_URL|GET|zc|3|周次|
|||xnxq01id|2025-2026-2|学年/学期|
|||kbjcmsid|16FD8C2BE55E15F9E0630100007FF6B5|校区id|
|||xswk|false|显示网课|