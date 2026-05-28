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
            r"/java-technical-docs/images/source/image-\d{2}\.png",
            corpus,
        )
        self.assertEqual(len(image_refs), 56)
        self.assertEqual(len(set(image_refs)), 56)
        for index in range(1, 57):
            image_name = f"image-{index:02d}.png"
            self.assertIn(f"/java-technical-docs/images/source/{image_name}", corpus)
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


if __name__ == "__main__":
    unittest.main()
