#!/usr/bin/env python3

import importlib.util
import json
import stat
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("render_site.py")
SPEC = importlib.util.spec_from_file_location("render_site", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load renderer module: {MODULE_PATH}")
render_site = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(render_site)


class RenderSiteTest(unittest.TestCase):
    def test_renders_manifest_descriptions_and_assets(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "info.json").write_text(
                json.dumps(
                    {
                        "display": "Blog",
                        "description": "Root description",
                        "articles": {
                            "hello": {
                                "title": "Hello",
                                "description": "Article description",
                            }
                        },
                    }
                )
            )
            (root / "hello.tmd").write_text("# Hello")
            (root / "notes").mkdir()
            (root / "notes" / "info.json").write_text(
                json.dumps({"display": "Notes", "articles": {}})
            )
            (root / "assets").mkdir()
            (root / "assets" / "diagram.svg").write_text("<svg />")

            typmark = root / "typmark-cli"
            typmark.write_text(
                "#!/usr/bin/env python3\n"
                "import pathlib, sys\n"
                "source = pathlib.Path(sys.argv[-1]).stem\n"
                "print(f'<article>{source}</article>')\n"
            )
            typmark.chmod(typmark.stat().st_mode | stat.S_IXUSR)

            count = render_site.render_site(root, Path("site"), typmark)
            index = json.loads((root / "site" / "blogs-index.json").read_text())

            self.assertEqual(count, 1)
            self.assertEqual(
                index["folders"][""]["description"], "Root description"
            )
            self.assertEqual(
                index["folders"][""]["pages"][0]["description"],
                "Article description",
            )
            self.assertIsNone(
                index["folders"][""]["folders"][0].get("description")
            )
            self.assertEqual(
                (root / "site" / "blogs-content" / "hello.html")
                .read_text()
                .strip(),
                "<article>hello</article>",
            )
            self.assertTrue(
                (root / "site" / "blogs" / "assets" / "diagram.svg").is_file()
            )

    def test_rejects_output_outside_source_root(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            typmark = root / "typmark-cli"
            typmark.write_text("")
            with self.assertRaisesRegex(SystemExit, "Output must be below"):
                render_site.render_site(root, root.parent / "outside", typmark)

    def test_rejects_output_symlink_without_deleting_target(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "source"
            target.mkdir()
            marker = target / "keep.tmd"
            marker.write_text("keep")
            (root / "site").symlink_to(target, target_is_directory=True)
            typmark = root / "typmark-cli"
            typmark.write_text("")

            with self.assertRaisesRegex(SystemExit, "must not contain a symlink"):
                render_site.render_site(root, Path("site"), typmark)

            self.assertEqual(marker.read_text(), "keep")


if __name__ == "__main__":
    unittest.main()
