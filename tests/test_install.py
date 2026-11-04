import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("installer", ROOT / "scripts/install.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)

class InstallTest(unittest.TestCase):
    def test_copies_only_skill_and_preserves_existing_install(self):
        source = ROOT / "skills/x-article-skill"
        with tempfile.TemporaryDirectory() as temp:
            parent = Path(temp) / "skills"
            target = installer.install(source, parent)
            expected = {p.relative_to(source) for p in source.rglob("*") if p.is_file()}
            actual = {p.relative_to(target) for p in target.rglob("*") if p.is_file()}
            self.assertEqual(expected, actual)
            for rel in expected:
                self.assertEqual((source / rel).read_bytes(), (target / rel).read_bytes())
            marker = target / "SKILL.md"
            marker.write_text("user-customized", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                installer.install(source, parent)
            self.assertEqual(marker.read_text(encoding="utf-8"), "user-customized")

    def test_missing_source_does_not_create_target(self):
        with tempfile.TemporaryDirectory() as temp:
            parent = Path(temp) / "destination"
            with self.assertRaises(FileNotFoundError):
                installer.install(Path(temp) / "missing", parent)
            self.assertFalse(parent.exists())

if __name__ == "__main__":
    unittest.main()

