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


if __name__ == "__main__":
    unittest.main()
