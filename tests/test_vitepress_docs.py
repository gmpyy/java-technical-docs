import hashlib
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


EXPECTED_FILES = [
    "index.md",
    ".vitepress/config.mts",
    "java/basic.md",
    "java/syntax.md",
    "java/string-collections.md",
    "java/oop.md",
    "java/ecosystem-database.md",
    "springboot/project.md",
    "springboot/request-di-mybatis.md",
    "springboot/web-chain.md",
    "springboot/auth.md",
    "springboot/reliability.md",
    "middleware/rabbitmq.md",
    "redis/basics.md",
    "redis/cache-lock.md",
    "redis/advanced.md",
]

REACT_FILES = [
    "react/index.md",
    "react/component-basics.md",
    "react/state-lifecycle.md",
    "react/hooks.md",
    "react/rendering.md",
    "react/router-state.md",
    "react/ecosystem-practice.md",
]

REACT_SERIES_FILES = [
    "react-series/index.md",
    "react-series/foundation.md",
    "react-series/components.md",
    "react-series/state-lifecycle.md",
    "react-series/hooks-style-animation.md",
    "react-series/routing-state.md",
    "react-series/rendering-performance.md",
    "react-series/engineering.md",
    "react-series/coverage.md",
]

REACT_NOTES_READING_FILES = [
    "react-notes/index.md",
    "react-notes/basics.md",
    "react-notes/redux.md",
    "react-notes/router.md",
    "react-notes/project-practice.md",
    "react-notes/advanced.md",
    "react-notes/zustand.md",
    "react-notes/react-ts.md",
    "react-notes/stack-selection.md",
    "react-notes/react-project.md",
    "react-notes/next-project.md",
    "react-notes/styling.md",
]

REACT_NOTES_FILES = [
    *REACT_NOTES_READING_FILES,
    "react-notes/source.md",
]

VUE_FILES = [
    "vue/index.md",
    "vue/project.md",
    "vue/basics.md",
    "vue/composition.md",
    "vue/components-router.md",
    "vue/state-request.md",
    "vue/ui-projects-legacy.md",
]


REQUIRED_TERMS = [
    "Java 跨平台",
    "基本数据类型",
    "StringBuilder",
    "ArrayList",
    "抽象类",
    "接口",
    "Maven",
    "MySQL",
    "DTO",
    "entity",
    "VO",
    "@RequestParam",
    "@Controller",
    "@Autowired",
    "MyBatis",
    "Filter",
    "Interceptor",
    "WebMvcConfigurer",
    "JWT",
    "验证码",
    "@Transactional",
    "@Scheduled",
    "RabbitMQ",
    "Fanout",
    "Direct",
    "Topic",
    "Redis",
    "缓存穿透",
    "缓存击穿",
    "分布式锁",
    "Redisson",
    "Stream",
    "GEO",
    "Bitmap",
    "HyperLogLog",
]

REACT_REQUIRED_TERMS = [
    "SyntheticEvent",
    "事件代理",
    "高阶组件",
    "Render props",
    "React Hooks",
    "Fiber",
    "PureComponent",
    "React Element",
    "React.createClass",
    "componentWillReceiveProps",
    "Fragment",
    "Portals",
    "React-Intl",
    "Context",
    "受控组件",
    "非受控组件",
    "forwardRef",
    "setState",
    "replaceState",
    "getDefaultProps",
    "PropTypes",
    "getDerivedStateFromProps",
    "getSnapshotBeforeUpdate",
    "shouldComponentUpdate",
    "父子组件",
    "跨级组件",
    "发布订阅",
    "React-Router",
    "Link",
    "Switch",
    "history",
    "Redux",
    "store",
    "reducer",
    "middleware",
    "connect",
    "MobX",
    "Vuex",
    "useState",
    "useEffect",
    "useLayoutEffect",
    "useMemo",
    "useCallback",
    "useRef",
    "虚拟 DOM",
    "diff",
    "key",
    "SSR",
    "JSX",
    "TypeScript",
    "严格模式",
    "React.Children",
]

REACT_SERIES_COVERAGE_TERMS = [
    "React 概念与特性",
    "Real DOM 与 Virtual DOM",
    "React 生命周期阶段",
    "state 与 props",
    "super() 与 super(props)",
    "setState 执行机制",
    "React 事件机制",
    "React 事件绑定方式",
    "React 组件构建方式",
    "React 组件通信",
    "key 的作用",
    "refs 的理解与应用",
    "类组件与函数组件",
    "受控组件与非受控组件",
    "高阶组件",
    "React Hooks",
    "React 中 CSS 引入方式",
    "React 组件过渡动画",
    "Redux 理解与工作原理",
    "Redux middleware",
    "React 项目中的 Redux 使用与结构划分",
    "React Router 理解与常用组件",
    "React Router 模式与实现原理",
    "immutable 在 React 中的应用",
    "React render 原理与触发时机",
    "提高组件渲染效率",
    "React diff 原理",
    "Fiber 架构",
    "JSX 转换为真实 DOM",
    "React 性能优化手段",
    "React 错误捕获",
    "React 服务端渲染",
    "React 常见问题与解决方式",
]

REACT_NOTES_TOP_LEVEL_TERMS = [
    "React",
    "状态管理工具Redux",
    "react路由",
    "实际项目开发",
    "react高级",
    "状态管理工具zustand",
    "react\\+ts",
    "项目开发技术栈选型",
    "react项目开发",
    "next项目开发",
    "样式方案",
]

VUE_REQUIRED_TERMS = [
    "create-vue",
    "Vite",
    "<script setup>",
    "Pinia",
    "defineModel",
    "Vue Router 4",
    "composables",
    "Vuex",
    "Element Plus",
    "Vant",
    "postcss-px-to-viewport",
    "axios 拦截器",
    "Drawer",
    "上传预览",
    "智慧商城",
    "文章管理系统",
]


class VitePressDocsTests(unittest.TestCase):
    def test_expected_vitepress_files_exist(self):
        for rel in EXPECTED_FILES:
            self.assertTrue((DOCS / rel).exists(), f"missing {rel}")

    def test_markdown_frontmatter_and_content_coverage(self):
        corpus = []
        for rel in EXPECTED_FILES:
            if not rel.endswith(".md"):
                continue
            text = (DOCS / rel).read_text(encoding="utf-8")
            corpus.append(text)
            self.assertRegex(text, r"\A---\n[\s\S]+?\n---\n", f"{rel} missing frontmatter")
            self.assertRegex(text, r"(?m)^# ", f"{rel} missing h1")
            self.assertIn("```", text, f"{rel} should preserve at least one code block")

        all_text = "\n".join(corpus)
        for term in REQUIRED_TERMS:
            self.assertIn(term, all_text, f"missing required term: {term}")

    def test_no_old_generator_or_broken_source_artifacts(self):
        self.assertFalse((ROOT / "scripts" / "build_site.py").exists())
        self.assertFalse((ROOT / "templates" / "layout.html").exists())
        self.assertFalse((ROOT / "content" / "site.json").exists())
        self.assertFalse((ROOT / "index.html").exists())
        self.assertFalse((ROOT / "java").exists())

    def test_no_mojibake_or_internal_image_links(self):
        bad_pattern = re.compile(r"锛|绛|鎶|�|internal-api-drive-stream|authcode")
        for md_file in DOCS.rglob("*.md"):
            if md_file == DOCS / "react-notes" / "source.md":
                continue
            text = md_file.read_text(encoding="utf-8")
            self.assertIsNone(bad_pattern.search(text), f"bad artifact in {md_file}")

    def test_content_is_not_overcompressed(self):
        corpus = "\n".join(
            md_file.read_text(encoding="utf-8")
            for md_file in DOCS.rglob("*.md")
        )
        self.assertGreater(len(corpus), 80000)
        self.assertGreaterEqual(corpus.count("```"), 100)

        image_refs = re.findall(
            r"/images/source/image-\d{2}\.png",
            corpus,
        )
        self.assertEqual(len(image_refs), 56)
        self.assertEqual(len(set(image_refs)), 56)
        for index in range(1, 57):
            image_name = f"image-{index:02d}.png"
            self.assertIn(f"/images/source/{image_name}", corpus)
            self.assertTrue((DOCS / "public" / "images" / "source" / image_name).exists())

    def test_github_pages_workflow_builds_vitepress(self):
        config = DOCS / ".vitepress" / "config.mts"
        config_text = config.read_text(encoding="utf-8")
        self.assertIn("base: '/java-technical-docs/'", config_text)

        workflow = ROOT / ".github" / "workflows" / "deploy.yml"
        self.assertTrue(workflow.exists(), "missing GitHub Pages workflow")
        text = workflow.read_text(encoding="utf-8")
        self.assertIn("actions/configure-pages", text)
        self.assertIn("actions/upload-pages-artifact", text)
        self.assertIn("actions/deploy-pages", text)
        self.assertIn("npm install", text)
        self.assertIn("npm run docs:build", text)
        self.assertIn("docs/.vitepress/dist", text)

    def test_react_docs_structure_and_content_coverage(self):
        for rel in REACT_FILES:
            self.assertTrue((DOCS / rel).exists(), f"missing {rel}")

        config_text = (DOCS / ".vitepress" / "config.mts").read_text(encoding="utf-8")
        self.assertIn("{ text: 'React', link: '/react/' }", config_text)
        self.assertIn("React 技术文档", config_text)

        corpus = []
        for rel in REACT_FILES:
            text = (DOCS / rel).read_text(encoding="utf-8")
            corpus.append(text)
            self.assertRegex(text, r"\A---\n[\s\S]+?\n---\n", f"{rel} missing frontmatter")
            self.assertRegex(text, r"(?m)^# ", f"{rel} missing h1")
            self.assertIn("```", text, f"{rel} should preserve code examples")

        react_text = "\n".join(corpus)
        self.assertGreater(len(react_text), 36000)
        self.assertGreaterEqual(react_text.count("```"), 30)

        for term in REACT_REQUIRED_TERMS:
            self.assertIn(term, react_text, f"missing React term: {term}")

        forbidden = re.compile(r"面试|面试题|面试官")
        self.assertIsNone(forbidden.search(react_text), "React docs should avoid interview wording")
        self.assertIsNone(forbidden.search(config_text), "config should avoid interview wording")

        remote = re.compile(r"https?://|yuque|cdn\.nlark|internal-api|alipayobjects")
        self.assertIsNone(remote.search(react_text), "React docs should not depend on remote resources")
        self.assertTrue((DOCS / "public" / "images" / "react").exists())

    def test_react_series_docs_structure_and_source_coverage(self):
        for rel in REACT_SERIES_FILES:
            self.assertTrue((DOCS / rel).exists(), f"missing {rel}")

        config_text = (DOCS / ".vitepress" / "config.mts").read_text(encoding="utf-8")
        self.assertIn("{ text: 'React 全系列', link: '/react-series/' }", config_text)
        self.assertIn("React 全系列技术文档", config_text)

        corpus = []
        for rel in REACT_SERIES_FILES:
            text = (DOCS / rel).read_text(encoding="utf-8")
            corpus.append(text)
            self.assertRegex(text, r"\A---\n[\s\S]+?\n---\n", f"{rel} missing frontmatter")
            self.assertRegex(text, r"(?m)^# ", f"{rel} missing h1")

        series_text = "\n".join(corpus)
        self.assertGreater(len(series_text), 45000)
        self.assertGreaterEqual(series_text.count("```"), 45)

        coverage_text = (DOCS / "react-series" / "coverage.md").read_text(encoding="utf-8")
        for term in REACT_SERIES_COVERAGE_TERMS:
            self.assertIn(term, coverage_text, f"missing React series coverage term: {term}")
            self.assertIn(term, series_text, f"missing React series content term: {term}")

        forbidden = re.compile(r"面试|面试题|面试官|题库|怎么回答")
        self.assertIsNone(forbidden.search(series_text), "React series docs should avoid source-site wording")
        self.assertIsNone(forbidden.search(config_text), "config should avoid source-site wording")

        remote = re.compile(r"https?://|yuque|cdn\.nlark|internal-api|alipayobjects")
        self.assertIsNone(remote.search(series_text), "React series docs should not depend on remote resources")

    def test_react_notes_preserve_source_and_align_menu(self):
        for rel in REACT_NOTES_FILES:
            self.assertTrue((DOCS / rel).exists(), f"missing {rel}")

        config_text = (DOCS / ".vitepress" / "config.mts").read_text(encoding="utf-8")
        self.assertIn("{ text: 'React 原文笔记', link: '/react-notes/' }", config_text)
        self.assertIn("React 原文笔记", config_text)
        for label in [
            "React 原文笔记总览",
            "React 基础",
            "Redux",
            "React 路由",
            "实际项目开发",
            "React 高级",
            "Zustand",
            "React + TS",
            "技术栈选型",
            "React 项目开发",
            "Next 项目开发",
            "样式方案",
            "原文归档",
        ]:
            self.assertIn(label, config_text)

        source_text = (DOCS / "react-notes" / "source.md").read_text(encoding="utf-8")
        normalized_source = source_text.replace("\r\n", "\n").replace("\r", "\n")
        self.assertEqual(len(normalized_source), 51886)
        self.assertEqual(
            hashlib.sha256(normalized_source.encode("utf-8")).hexdigest().upper(),
            "98C573EC474852CB2866F2984D19167D706466BDCEB9CA96E3EEB94E9F2DF9A6",
        )
        self.assertEqual(normalized_source.count("```"), 156)
        self.assertEqual(normalized_source.count("![Image]("), 9)

        reading_corpus = []
        for rel in REACT_NOTES_READING_FILES:
            text = (DOCS / rel).read_text(encoding="utf-8")
            reading_corpus.append(text)
            self.assertRegex(text, r"\A---\n[\s\S]+?\n---\n", f"{rel} missing frontmatter")
            self.assertRegex(text, r"(?m)^#{1,6}\s+", f"{rel} missing markdown heading")

        reading_text = "\n".join(reading_corpus)
        for term in REACT_NOTES_TOP_LEVEL_TERMS:
            self.assertIn(term, reading_text, f"missing React notes term: {term}")

        self.assertEqual(reading_text.count("/images/react-notes/image-"), 9)
        self.assertNotIn("internal-api-drive-stream.feishu.cn", reading_text)
        self.assertEqual(len(list((DOCS / "public" / "images" / "react-notes").glob("image-*.*"))), 9)

    def test_vue_docs_structure_and_content_coverage(self):
        for rel in VUE_FILES:
            self.assertTrue((DOCS / rel).exists(), f"missing {rel}")

        config_text = (DOCS / ".vitepress" / "config.mts").read_text(encoding="utf-8")
        self.assertIn("{ text: 'Vue', link: '/vue/' }", config_text)
        self.assertIn("Vue 技术文档", config_text)

        corpus = []
        for rel in VUE_FILES:
            text = (DOCS / rel).read_text(encoding="utf-8")
            corpus.append(text)
            self.assertRegex(text, r"\A---\n[\s\S]+?\n---\n", f"{rel} missing frontmatter")
            self.assertRegex(text, r"(?m)^# ", f"{rel} missing h1")
            self.assertIn("```", text, f"{rel} should preserve code examples")

        vue_text = "\n".join(corpus)
        self.assertGreater(len(vue_text), 20000)
        self.assertGreaterEqual(vue_text.count("```"), 55)

        for term in VUE_REQUIRED_TERMS:
            self.assertIn(term, vue_text, f"missing Vue term: {term}")

        forbidden = re.compile(r"面试|面试题|面试官")
        self.assertIsNone(forbidden.search(vue_text), "Vue docs should avoid interview wording")
        self.assertIsNone(forbidden.search(config_text), "config should avoid interview wording")


if __name__ == "__main__":
    unittest.main()
