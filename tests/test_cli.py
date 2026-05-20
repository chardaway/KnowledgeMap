"""测试 CLI 封装层（不依赖真实 Obsidian 的部分）。"""

import tempfile
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import src.cli as cli_mod


class TestCliAvailability(unittest.TestCase):
    def test_cli_available(self):
        result = cli_mod.cli_available()
        self.assertIsInstance(result, bool)


class TestCreateMapNote(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.vault = Path(self.tmp.name)
        # 同时 patch cli.py 和 config.py 中的引用
        self._orig_vault = cli_mod.get_vault_path
        import src.config as cfg
        self._orig_config_vault = cfg.get_vault_path
        cli_mod.get_vault_path = lambda: self.vault
        cfg.get_vault_path = lambda: self.vault

    def tearDown(self):
        self.tmp.cleanup()
        cli_mod.get_vault_path = self._orig_vault
        import src.config as cfg
        cfg.get_vault_path = self._orig_config_vault

    def test_create_without_backlinks(self):
        rel = cli_mod.create_map_note(
            "线性", "测试问题", "这是正文。",
            vault=None, use_cli=False,
        )
        self.assertIn("测试问题", rel)
        f = self.vault / rel
        self.assertTrue(f.exists(), f"预期文件存在: {f}")
        content = f.read_text(encoding="utf-8")
        self.assertIn("# 测试问题", content)
        self.assertIn("这是正文。", content)

    def test_create_with_backlinks(self):
        rel = cli_mod.create_map_note(
            "解构", "核心问题", "正文。",
            backlinks=["子问题1", "子问题2"],
            vault=None, use_cli=False,
        )
        f = self.vault / rel
        content = f.read_text(encoding="utf-8")
        self.assertIn("[[子问题1]]", content)
        self.assertIn("[[子问题2]]", content)

    def test_creates_skill_subdirs(self):
        for skill in ["线性", "解构", "拓展"]:
            rel = cli_mod.create_map_note(skill, "测试", "x", vault=None, use_cli=False)
            f = self.vault / rel
            self.assertTrue(f.exists(), f"技能 {skill}: 预期文件存在: {f}")
            self.assertIn(f"认知地图/{skill}", rel.replace("\\", "/"))


class TestAppendLinks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.vault = Path(self.tmp.name)
        self._orig_vault = cli_mod.get_vault_path
        import src.config as cfg
        self._orig_config_vault = cfg.get_vault_path
        cli_mod.get_vault_path = lambda: self.vault
        cfg.get_vault_path = lambda: self.vault

    def tearDown(self):
        self.tmp.cleanup()
        cli_mod.get_vault_path = self._orig_vault
        import src.config as cfg
        cfg.get_vault_path = self._orig_config_vault

    def test_append_to_existing(self):
        rel = cli_mod.create_map_note("线性", "节点A", "正文。", vault=None, use_cli=False)
        ok = cli_mod.append_links(rel, ["节点B"], vault=None, use_cli=False)
        self.assertTrue(ok)
        content = (self.vault / rel).read_text(encoding="utf-8")
        self.assertIn("[[节点B]]", content)

    def test_read_map_note(self):
        rel = cli_mod.create_map_note("拓展", "问题X", "这是测试内容。", vault=None, use_cli=False)
        text = cli_mod.read_map_note(rel, vault=None, use_cli=False)
        self.assertIn("问题X", text)
        self.assertIn("测试内容", text)


if __name__ == "__main__":
    unittest.main()
