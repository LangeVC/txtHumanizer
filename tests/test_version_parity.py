"""Version parity tests against canonical .version.yaml."""

from pathlib import Path
import re
import unittest

REPO_ROOT = Path(__file__).resolve().parent.parent
_YAML_VERSION_RE = re.compile(r"^version:\s*[\"']?([^\s\"'#]+)[\"']?(?:\s*#.*)?$", re.MULTILINE)
_INIT_VERSION_RE = re.compile(r"^__version__\s*=\s*[\"']([^\"']+)[\"']", re.MULTILINE)
_SETUP_VERSION_RE = re.compile(r"^\s*version\s*=\s*[\"']([^\"']+)[\"']", re.MULTILINE)
_FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", re.DOTALL)


def _read_repo_text(rel_path: str) -> str:
    return (REPO_ROOT / rel_path).read_text(encoding="utf-8")


def _extract_frontmatter(content: str, rel_path: str) -> str:
    match = _FRONTMATTER_RE.match(content)
    if not match:
        raise AssertionError(f"Missing or malformed YAML frontmatter block in {rel_path}")
    return match.group(1)


def _extract_version(text: str, pattern: re.Pattern[str], source: str) -> str:
    match = pattern.search(text)
    if not match:
        raise AssertionError(f"Could not extract version from {source}")
    version = match.group(1).strip()
    if not version:
        raise AssertionError(f"Extracted empty version from {source}")
    return version


class TestVersionParity(unittest.TestCase):
    """Ensure all version declarations match .version.yaml."""

    def _canonical_version(self) -> str:
        content = _read_repo_text(".version.yaml")
        return _extract_version(content, _YAML_VERSION_RE, ".version.yaml")

    def _assert_version_matches(
        self,
        rel_path: str,
        pattern: re.Pattern[str],
        *,
        frontmatter_only: bool = False,
    ) -> None:
        canonical = self._canonical_version()
        content = _read_repo_text(rel_path)
        target_text = _extract_frontmatter(content, rel_path) if frontmatter_only else content
        found = _extract_version(target_text, pattern, rel_path)
        self.assertEqual(
            found,
            canonical,
            f"Version mismatch in {rel_path}: expected {canonical!r} (from .version.yaml), found {found!r}",
        )

    def test_capability_yaml_version_parity(self) -> None:
        self._assert_version_matches("capability.yaml", _YAML_VERSION_RE)

    def test_package_init_version_parity(self) -> None:
        self._assert_version_matches("txthumanizer/__init__.py", _INIT_VERSION_RE)

    def test_setup_py_version_parity(self) -> None:
        self._assert_version_matches("setup.py", _SETUP_VERSION_RE)

    def test_skill_md_frontmatter_version_parity(self) -> None:
        self._assert_version_matches("SKILL.md", _YAML_VERSION_RE, frontmatter_only=True)


if __name__ == "__main__":
    unittest.main()
