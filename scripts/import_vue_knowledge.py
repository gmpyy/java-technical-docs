"""Import the Vue knowledge article from Yuque Lake HTML into VitePress pages.

This is a one-time converter for the public source document. It validates the
source shape before writing so an upstream content change is noticed instead of
silently producing a different outline.
"""

from __future__ import annotations

import argparse
import json
import re
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag


SOURCE_URL = "https://www.yuque.com/api/docs/hswu8g?book_id=6862641"
EXPECTED_TITLE = "前端面试题之Vue篇"
EXPECTED_WORD_COUNT = 31634
EXPECTED_CHAPTERS = 7
EXPECTED_SECTIONS = 90
EXPECTED_CODE_BLOCKS = 85

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_ROOT = REPO_ROOT / "docs"
OUTPUT_DIR = DOCS_ROOT / "vue-knowledge"

CHAPTERS = [
    ("一、Vue 基础", "basics", "Vue 基础"),
    ("二、生命周期", "lifecycle", "生命周期"),
    ("三、组件通信", "component-communication", "组件通信"),
    ("四、路由", "router", "路由"),
    ("五、Vuex", "vuex", "Vuex"),
    ("六、Vue 3.0", "vue3", "Vue 3.0"),
    ("七、虚拟DOM", "virtual-dom", "虚拟 DOM"),
]

HEADING_OVERRIDES = {
    "使用 Object.defineProperty() 来进行数据劫持有什么缺点？": "使用 Object.defineProperty() 进行数据劫持的缺点",
    "slot是什么？有什么作用？原理是什么？": "slot 的概念、作用与原理",
    "过滤器的作用，如何实现一个过滤器": "过滤器的作用与实现",
    "如何保存页面的当前的状态": "保存页面当前状态的方法",
    "v-model 是如何实现的，语法糖实际是什么？": "v-model 的实现原理与语法糖",
    "v-model 可以被用在自定义组件上吗？如果可以，如何使用？": "v-model 在自定义组件中的使用方式",
    "data为什么是一个函数而不是对象": "data 使用函数而不是对象的原因",
    "对keep-alive的理解，它是如何实现的，具体缓存的是什么？": "keep-alive 的概念、实现与缓存内容",
    "$nextTick 原理及作用": "nextTick 的原理与作用",
    "Vue 中给 data 中的对象属性添加一个新的属性时会发生什么？如何解决？": "Vue 中新增 data 对象属性的表现与解决方式",
    "Vue中封装的数组方法有哪些，其如何实现页面更新": "Vue 封装的数组方法及页面更新实现",
    "Vue data 中某一个属性的值发生改变后，视图会立即同步执行重新渲染吗？": "Vue data 属性变化后的视图更新时机",
    "简述 mixin、extends 的覆盖逻辑": "mixin 与 extends 的覆盖逻辑",
    "描述下Vue自定义指令": "Vue 自定义指令",
    "子组件可以直接改变父组件的数据吗？": "子组件直接修改父组件数据的影响",
    "Vue是如何收集依赖的？": "Vue 的依赖收集机制",
    "对 React 和 Vue 的理解，它们的异同": "React 与 Vue 的理解和异同",
    "delete和Vue.delete删除数组的区别": "delete 与 Vue.delete 删除数组的区别",
    "vue如何监听对象或者数组某个属性的变化": "Vue 监听对象或数组属性变化的方法",
    "什么是 mixin ？": "mixin 的概念",
    "Vue模版编译原理": "Vue 模板编译原理",
    "对SSR的理解": "SSR 的理解",
    "Vue的性能优化有哪些": "Vue 性能优化方法",
    "对 SPA 单页面的理解，它的优缺点分别是什么？": "SPA 单页面的概念与优缺点",
    "template和jsx的有什么分别？": "template 与 JSX 的区别",
    "vue初始化页面闪动问题": "Vue 初始化页面闪动问题",
    "extend 有什么作用": "extend 的作用",
    "MVVM 的优缺点 ?": "MVVM 的优缺点",
    "v-if 和 v-for哪个优先级更高？如果同时出现，应如何优化？": "v-if 与 v-for 的优先级及同时使用优化",
    "对Vue组件化的理解": "Vue 组件化的理解",
    "对vue设计原则的理解": "Vue 设计原则的理解",
    "v-model的实现原理": "v-model 的实现原理",
    "说一下Vue的生命周期": "Vue 生命周期概览",
    "一般在哪个生命周期请求异步数据": "异步数据请求的生命周期选择",
    "keep-alive 中的生命周期哪些": "keep-alive 中的生命周期",
    "（1） props  /   $emit": "props 与 $emit 通信",
    "（2）eventBus事件总线（$emit / $on）": "EventBus 事件总线通信",
    "（3）依赖注入（provide/ inject）": "provide 与 inject 依赖注入",
    "（3）ref / $refs": "ref 与 $refs 通信",
    "（4）$parent / $children": "$parent 与 $children 通信",
    "（5）$attrs / $listeners": "$attrs 与 $listeners 通信",
    "（6）总结": "组件通信方式总结",
    "Vue-Router 的懒加载如何实现": "Vue Router 懒加载的实现",
    "路由的hash和history模式的区别": "hash 与 history 路由模式的区别",
    "如何获取页面的hash变化": "获取页面 hash 变化的方法",
    "$route 和$router 的区别": "$route 与 $router 的区别",
    "如何定义动态路由？如何获取传过来的动态参数？": "动态路由定义与参数获取",
    "Vue-router 路由钩子在生命周期的体现": "Vue Router 路由钩子在生命周期中的体现",
    "Vue-router跳转和location.href有什么区别": "Vue Router 跳转与 location.href 的区别",
    "Vue-router 导航守卫有哪些": "Vue Router 导航守卫",
    "对前端路由的理解": "前端路由的理解",
    "Vuex中action和mutation的区别": "Vuex 中 action 与 mutation 的区别",
    "Redux 和 Vuex 有什么区别，它们的共同思想": "Redux 与 Vuex 的区别和共同思想",
    "为什么要用 Vuex 或者 Redux": "使用 Vuex 或 Redux 的原因",
    "Vuex有哪几种属性？": "Vuex 的核心属性",
    "Vuex和单纯的全局对象有什么区别？": "Vuex 与普通全局对象的区别",
    "为什么 Vuex 的 mutation 中不能做异步操作？": "Vuex mutation 不执行异步操作的原因",
    "Vuex的严格模式是什么,有什么作用，如何开启？": "Vuex 严格模式的概念、作用与开启方式",
    "如何 在组件中批量使用Vuex的getter属性": "在组件中批量使用 Vuex getter 的方法",
    "如何在 组件中重复使用 Vuex的 mutation": "在组件中复用 Vuex mutation 的方法",
    "Vue3.0有什么更新": "Vue 3.0 的主要更新",
    "defineProperty和proxy的区别": "defineProperty 与 Proxy 的区别",
    "Vue3.0 为什么要用 proxy？": "Vue 3.0 使用 Proxy 的原因",
    "Vue 3.0 中的 Vue Composition API？": "Vue 3.0 中的 Composition API",
    "Composition API与React Hook很像，区别是什么": "Composition API 与 React Hook 的区别",
    "对虚拟DOM的理解？": "虚拟 DOM 的理解",
    "为什么要用虚拟DOM": "使用虚拟 DOM 的原因",
    "虚拟DOM真的比真实DOM性能好吗": "虚拟 DOM 与真实 DOM 的性能关系",
    "DIFF算法的原理": "Diff 算法的原理",
    "为什么不建议用index作为key?": "不建议使用 index 作为 key 的原因",
}

TEXT_REPLACEMENTS = [
    ("前端面试题之Vue篇", "Vue 知识体系"),
    ("面试题", "知识点"),
    ("面试官", "提问者"),
    ("面试", "交流"),
    ("校招", "招聘"),
    ("内推", "推荐"),
    ("公众号", "公开资料"),
    ("交流群", "讨论群"),
    ("PDF版", "整理版"),
    ("打卡", "记录"),
    ("Vue3.0", "Vue 3.0"),
    ("Vue3", "Vue 3"),
    ("vue3", "Vue 3"),
    ("Vue-Router", "Vue Router"),
    ("Vue-router", "Vue Router"),
    ("vue-router", "Vue Router"),
    ("vuex", "Vuex"),
    ("DIFF", "Diff"),
    ("diff", "Diff"),
    ("虚拟DOM", "虚拟 DOM"),
    ("真实DOM", "真实 DOM"),
    ("Object.defineproperty", "Object.defineProperty"),
    ("defineproperty", "defineProperty"),
    ("Object.defineProperty()", "Object.defineProperty"),
    ("kepp-alive", "keep-alive"),
    ("</kepp-alive>", "</keep-alive>"),
    ("$nextTick", "nextTick"),
    ("模版", "模板"),
    ("jsx", "JSX"),
    ("hash", "hash"),
    ("http://www.abc.com/#/Vue", "示例域名/#/vue"),
    ("http://abc.com/user/id", "示例域名/user/id"),
]


@dataclass
class Chapter:
    source_title: str
    title: str
    slug: str
    description: str
    blocks: list[Tag]


def normalize_spaces(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *([，。；：！？、]) *", r"\1", text)
    return text.strip()


def clean_text(text: str) -> str:
    text = normalize_spaces(text)
    for old, new in TEXT_REPLACEMENTS:
        text = text.replace(old, new)
    text = re.sub(r"https?://[^\s，。；、)）]+", "示例地址", text)
    text = re.sub(r"\bvue\b", "Vue", text)
    text = re.sub(r"\bVUE\b", "Vue", text)
    text = text.replace("Vue的", "Vue 的")
    text = text.replace("Vue中", "Vue 中")
    text = text.replace("Vuex中", "Vuex 中")
    text = text.replace("key?", "key")
    return normalize_spaces(text)


def split_heading_number(text: str, fallback_number: int) -> tuple[str, str]:
    text = normalize_spaces(text)
    numbered = re.match(r"^(\d+)\.\s*(.+)$", text)
    if numbered:
        return numbered.group(1), numbered.group(2)

    chinese_numbered = re.match(r"^（\d+）\s*(.+)$", text)
    if chinese_numbered:
        return str(fallback_number), chinese_numbered.group(1)

    return str(fallback_number), text


def technical_heading(text: str, fallback_number: int | None = None) -> str:
    if fallback_number is None:
        return clean_text(text)

    number, body = split_heading_number(text, fallback_number)
    body = HEADING_OVERRIDES.get(normalize_spaces(body), body)
    body = clean_text(body)
    body = body.rstrip("？? ")
    body = body.replace("是什么", "的概念")
    body = body.replace("为什么", "的原因")
    return f"{number}. {body}"


def decode_codeblock(card: Tag) -> tuple[str, str]:
    raw = urllib.parse.unquote(card.get("value", ""))
    if raw.startswith("data:"):
        raw = raw[5:]
    payload = json.loads(raw)
    mode = payload.get("mode") or ""
    code = payload.get("code") or ""
    language = {"javascript": "js", "plain": ""}.get(mode, mode)
    return language, clean_code(code)


def clean_code(code: str) -> str:
    code = code.replace("\r\n", "\n").replace("\r", "\n").strip("\n")
    for old, new in TEXT_REPLACEMENTS:
        code = code.replace(old, new)
    code = re.sub(r"https?://[^\s\"'`，。；、)）]+", "example-path", code)
    return code


def inline_text(node: Tag | NavigableString) -> str:
    if isinstance(node, NavigableString):
        return str(node)

    if not isinstance(node, Tag):
        return ""

    if node.name == "br":
        return "\n"

    if node.name == "card":
        return ""

    child_text = "".join(inline_text(child) for child in node.children)

    if node.name == "code":
        value = child_text.strip()
        if not value:
            return ""
        return f"`{value.replace('`', '')}`"

    if node.name == "strong":
        value = clean_text(child_text)
        return f"**{value}**" if value else ""

    if node.name == "a":
        return child_text

    return child_text


def list_item_text(li: Tag) -> str:
    parts = []
    for child in li.children:
        if isinstance(child, Tag) and child.name in {"ul", "ol"}:
            continue
        parts.append(inline_text(child))
    return clean_text("".join(parts))


def render_list(tag: Tag, ordered: bool) -> str:
    lines = []
    for index, li in enumerate(tag.find_all("li", recursive=False), 1):
        marker = f"{index}." if ordered else "-"
        text = list_item_text(li)
        if text:
            lines.append(f"{marker} {text}")
        for child in li.find_all(["ul", "ol"], recursive=False):
            nested = render_list(child, child.name == "ol")
            if nested:
                lines.extend(f"  {line}" for line in nested.splitlines())
    return "\n".join(lines)


def render_block(tag: Tag, section_number: int | None = None) -> tuple[str, bool]:
    if tag.name == "h3":
        heading = technical_heading(tag.get_text(" ", strip=True), section_number)
        return f"## {heading}", True

    if tag.name in {"h4", "h5"}:
        return f"### {technical_heading(tag.get_text(' ', strip=True))}", False

    if tag.name == "p":
        text = clean_text(inline_text(tag))
        return text, False

    if tag.name == "card" and tag.get("name") == "codeblock":
        language, code = decode_codeblock(tag)
        return f"```{language}\n{code}\n```", False

    if tag.name == "card":
        return "", False

    if tag.name in {"ul", "ol"}:
        return render_list(tag, tag.name == "ol"), False

    return "", False


def load_source(source: Path | None) -> dict:
    if source:
        return json.loads(source.read_text(encoding="utf-8"))

    with urllib.request.urlopen(SOURCE_URL, timeout=30) as response:
        if response.status != 200:
            raise RuntimeError(f"Yuque API returned HTTP {response.status}")
        return json.loads(response.read().decode("utf-8"))


def chapter_meta(title: str) -> tuple[str, str, str]:
    compact = normalize_spaces(title)
    compact = compact.replace("三、 组件通信", "三、组件通信").replace("五、 Vuex", "五、Vuex")
    compact = compact.replace("七、虚拟 DOM", "七、虚拟DOM")
    for expected_title, slug, description in CHAPTERS:
        if compact == expected_title:
            return expected_title, slug, description
    raise ValueError(f"Unexpected chapter title: {title!r}")


def parse_chapters(content: str) -> list[Chapter]:
    soup = BeautifulSoup(content, "html.parser")
    chapters: list[Chapter] = []
    current: Chapter | None = None

    for node in soup.contents:
        if not isinstance(node, Tag):
            continue
        if node.name == "meta":
            continue
        if node.name == "h2":
            title, slug, description = chapter_meta(node.get_text(" ", strip=True))
            current = Chapter(node.get_text(" ", strip=True), title, slug, description, [])
            chapters.append(current)
            continue
        if current is not None:
            current.blocks.append(node)

    return chapters


def validate_source(data: dict, chapters: list[Chapter]) -> None:
    if data.get("title") != EXPECTED_TITLE:
        raise RuntimeError(f"Unexpected title: {data.get('title')!r}")
    if data.get("word_count") != EXPECTED_WORD_COUNT:
        raise RuntimeError(f"Unexpected word_count: {data.get('word_count')!r}")
    if len(chapters) != EXPECTED_CHAPTERS:
        raise RuntimeError(f"Expected {EXPECTED_CHAPTERS} chapters, got {len(chapters)}")

    section_count = sum(1 for chapter in chapters for block in chapter.blocks if block.name == "h3")
    if section_count != EXPECTED_SECTIONS:
        raise RuntimeError(f"Expected {EXPECTED_SECTIONS} H3 sections, got {section_count}")

    code_count = sum(
        1
        for chapter in chapters
        for block in chapter.blocks
        if block.name == "card" and block.get("name") == "codeblock"
    )
    if code_count != EXPECTED_CODE_BLOCKS:
        raise RuntimeError(f"Expected {EXPECTED_CODE_BLOCKS} code blocks, got {code_count}")


def frontmatter(title: str, description: str) -> str:
    return (
        "---\n"
        f"title: {title}\n"
        f"description: {description}\n"
        "outline: [2, 3]\n"
        "---\n\n"
    )


def render_chapter(chapter: Chapter) -> str:
    lines = [
        frontmatter(chapter.title, f"Vue 知识体系专题中的{chapter.description}整理。"),
        f"# {chapter.title}",
        "",
    ]
    section_number = 0
    for block in chapter.blocks:
        if block.name == "h3":
            section_number += 1
            rendered, _ = render_block(block, section_number)
        else:
            rendered, _ = render_block(block)
        if rendered:
            lines.append(rendered)
            lines.append("")
    return normalize_markdown("\n".join(lines))


def normalize_markdown(text: str) -> str:
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def render_index() -> str:
    rows = "\n".join(
        f"| [{title}](/vue-knowledge/{slug}) | {description} |"
        for title, slug, description in CHAPTERS
    )
    text = f"""\
{frontmatter("Vue 知识体系", "按 Vue 基础、生命周期、组件通信、路由、Vuex、Vue 3.0 与虚拟 DOM 整理的系统化专题。")}# Vue 知识体系

这个专题按原始公开文档的七个主题重新整理，保留章节顺序、代码示例、列表与技术说明，并移除推广图片、二维码、外部资源引用和非技术表达。

## 目录

| 章节 | 内容范围 |
| --- | --- |
{rows}

## 整理原则

- 章节顺序与原始资料保持一致。
- 标题调整为技术文档式表达，保留编号与对应关系。
- 代码块、列表和关键术语保留为可阅读的 Markdown。
- 图片推广素材和远程资源链接不进入本站内容。
"""
    return normalize_markdown(text)


def write_files(chapters: Iterable[Chapter]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "index.md").write_text(render_index(), encoding="utf-8", newline="\n")
    for chapter in chapters:
        (OUTPUT_DIR / f"{chapter.slug}.md").write_text(render_chapter(chapter), encoding="utf-8", newline="\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, help="Read a saved Yuque API JSON response instead of fetching.")
    args = parser.parse_args()

    payload = load_source(args.source)
    data = payload["data"]
    chapters = parse_chapters(data["content"])
    validate_source(data, chapters)
    write_files(chapters)
    print(
        f"Wrote {1 + len(chapters)} files to {OUTPUT_DIR} "
        f"({EXPECTED_SECTIONS} sections, {EXPECTED_CODE_BLOCKS} code blocks)."
    )


if __name__ == "__main__":
    main()
