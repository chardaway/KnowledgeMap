"""测试文件名处理。"""

import tempfile
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.naming import sanitize_filename, unique_path


class TestSanitize(unittest.TestCase):
    def test_chinese_title(self):
        self.assertEqual(sanitize_filename("为什么天空是蓝色的？"), "为什么天空是蓝色的？")

    def test_illegal_chars(self):
        self.assertEqual(sanitize_filename("a<b>c:d*e?f"), "abcdef")

    def test_strip_whitespace(self):
        self.assertEqual(sanitize_filename("  标题  "), "标题")

    def test_long_title_truncate(self):
        long = "a" * 120
        result = sanitize_filename(long)
        self.assertEqual(len(result), 100)


class TestUniquePath(unittest.TestCase):
    def test_no_conflict(self):
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            p = unique_path(d, "新笔记")
            self.assertEqual(p, d / "新笔记.md")

    def test_conflict_appends_number(self):
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            (d / "新笔记.md").write_text("")
            p = unique_path(d, "新笔记")
            self.assertEqual(p, d / "新笔记-2.md")

    def test_multiple_conflicts(self):
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            (d / "新笔记.md").write_text("")
            (d / "新笔记-2.md").write_text("")
            p = unique_path(d, "新笔记")
            self.assertEqual(p, d / "新笔记-3.md")


if __name__ == "__main__":
    unittest.main()
