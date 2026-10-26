"""契約測試：相對連結檢查要和 GitHub 的解析結果一致。"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import check_links


@pytest.fixture
def docs_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    root = tmp_path.resolve()
    monkeypatch.setattr(check_links, "ROOT", root)
    (root / "docs").mkdir()
    (root / "docs" / "Guide.md").write_text("# guide\n", encoding="utf-8")
    return root


def test_link_with_wrong_case_is_reported(docs_root: Path) -> None:
    # Windows 檔案系統不分大小寫，所以 exists() 會放行；GitHub 與 Linux 不會。
    doc = docs_root / "README.md"
    doc.write_text("[a](docs/guide.md) [b](Docs/Guide.md)\n", encoding="utf-8")
    problems = check_links.check_document(doc)
    assert len(problems) == 2


def test_link_with_exact_case_passes(docs_root: Path) -> None:
    doc = docs_root / "README.md"
    doc.write_text("[a](docs/Guide.md#top) [b](./docs/../docs/Guide.md)\n", encoding="utf-8")
    assert check_links.check_document(doc) == []
