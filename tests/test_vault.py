"""测试 vault 查询。"""

import tempfile
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.vault import find_note, list_notes, resolve_wikilink


class TestVault(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.vault = Path(self.tmp.name)
        (self.vault / "2025").mkdir()
        (self.vault / "2026").mkdir()
        (self.vault / ".obsidian").mkdir()
        (self.vault / "2025" / "笔记A.md").write_text("---\ntags:\n  - test\n---\n# A")
        (self.vault / "2026" / "笔记B.md").write_text("# B")
        (self.vault / ".obsidian" / "app.json").write_text("{}")

    def tearDown(self):
        self.tmp.cleanup()

    def test_find_note_by_name(self):
        p = find_note(self.vault, "笔记A")
        self.assertIsNotNone(p)
        self.assertEqual(p.name, "笔记A.md")

    def test_find_note_not_found(self):
        p = find_note(self.vault, "不存在")
        self.assertIsNone(p)

    def test_find_note_skips_obsidian(self):
        p = find_note(self.vault, "app")  # .obsidian/app.json
        self.assertIsNone(p)

    def test_list_notes(self):
        notes = list_notes(self.vault)
        self.assertEqual(len(notes), 2)

    def test_list_notes_by_folder(self):
        notes = list_notes(self.vault, "2025")
        self.assertEqual(len(notes), 1)
        self.assertIn("笔记A.md", [n.name for n in notes])

    def test_resolve_wikilink_with_alias(self):
        p = resolve_wikilink(self.vault, "笔记A|别名")
        self.assertIsNotNone(p)
        self.assertEqual(p.name, "笔记A.md")

    def test_resolve_wikilink_with_heading(self):
        p = resolve_wikilink(self.vault, "笔记B#标题")
        self.assertIsNotNone(p)
        self.assertEqual(p.name, "笔记B.md")


if __name__ == "__main__":
    unittest.main()
