from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from repo_root_line_count.cli import line_count, resolve_target


class LineCountTests(unittest.TestCase):
    def test_resolves_relative_to_scan_root(self) -> None:
        with TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            root = temp / "project"
            root.mkdir()
            (root / "file.txt").write_text("one\ntwo\nthree\n", encoding="utf-8")
            (temp / "file.txt").write_text("wrong\n", encoding="utf-8")

            self.assertEqual(line_count(root, "file.txt"), 3)

    def test_missing_relative_file_returns_minus_one(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.assertEqual(line_count(root, "missing.txt"), -1)

    def test_absolute_file_inside_root_is_accepted(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            target = root / "nested.txt"
            target.write_text("one\n", encoding="utf-8")
            self.assertEqual(line_count(root, target), 1)

    def test_relative_resolution_does_not_depend_on_current_directory(self) -> None:
        with TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            root = temp / "scan"
            root.mkdir()
            (root / "file.txt").write_text("a\nb\n", encoding="utf-8")

            with TemporaryDirectory() as other_dir:
                previous = Path.cwd()
                try:
                    import os

                    os.chdir(other_dir)
                    self.assertEqual(line_count(root, "file.txt"), 2)
                finally:
                    os.chdir(previous)

    def test_target_outside_root_is_rejected(self) -> None:
        with TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            root = temp / "root"
            root.mkdir()
            outside = temp / "outside.txt"
            outside.write_text("one\n", encoding="utf-8")

            with self.assertRaises(ValueError):
                resolve_target(root, outside)


if __name__ == "__main__":
    unittest.main()
