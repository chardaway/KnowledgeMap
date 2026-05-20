"""测试笔记读写。"""

import tempfile
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.note import create_note, read_frontmatter, has_frontmatter


class TestCreateNote(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_basic_note(self):
        p = self.dir / "test.md"
        create_note(p, "测试标题", ["认知地图", "线性"], "正文内容。")
        self.assertTrue(p.exists())
        content = p.read_text(encoding="utf-8")
        self.assertIn("# 测试标题", content)
        self.assertIn("  - 认知地图", content)
        self.assertIn("  - 线性", content)

    def test_note_with_backlinks(self):
        p = self.dir / "linked.md"
        create_note(p, "链接测试", ["认知地图"], "正文。", backlinks=["关联A", "关联B"])
        content = p.read_text(encoding="utf-8")
        self.assertIn("[[关联A]]", content)
        self.assertIn("[[关联B]]", content)

    def test_creates_parent_dirs(self):
        p = self.dir / "deep" / "nested" / "note.md"
        create_note(p, "深层", ["test"], "内容。")
        self.assertTrue(p.exists())

    def test_frontmatter_parse(self):
        p = self.dir / "fm.md"
        create_note(p, "标题", ["tag1", "tag2"], "正文。", backlinks=["link1"])
        fm = read_frontmatter(p)
        self.assertIn("tags", fm)
        self.assertEqual(fm["tags"], ["tag1", "tag2"])

    def test_has_frontmatter_true(self):
        p = self.dir / "hasfm.md"
        create_note(p, "标题", ["test"], "正文。")
        self.assertTrue(has_frontmatter(p))

    def test_has_frontmatter_false(self):
        p = self.dir / "nofm.md"
        p.write_text("# 没有 frontmatter", encoding="utf-8")
        self.assertFalse(has_frontmatter(p))


if __name__ == "__main__":
    unittest.main()
