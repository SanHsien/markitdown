"""契約測試：requirements-all.txt 要涵蓋產品測試所需的額外依賴。

`bootstrap_dev.ps1 -All` 之後跑 `test_product.ps1 -AllPackages`，收集階段就會
因為缺 `yaml`／`openai` 失敗；上游把這些只宣告在 hatch-test 環境裡。
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import check_dependency_freshness as checker

ROOT = Path(__file__).resolve().parents[2]


def _hatch_test_extra_dependencies(pyproject: Path) -> list[str]:
    text = pyproject.read_text(encoding="utf-8")
    section = re.search(
        r"^\[tool\.hatch\.envs\.hatch-test\]\s*$(.*?)(?=^\[|\Z)", text, re.M | re.S
    )
    if not section:
        return []
    listing = re.search(r"extra-dependencies\s*=\s*\[(.*?)\]", section.group(1), re.S)
    return re.findall(r'"([^"]+)"', listing.group(1)) if listing else []


def test_hatch_test_extra_dependencies_are_declared_in_requirements_all() -> None:
    needed = _hatch_test_extra_dependencies(
        ROOT / "packages" / "markitdown" / "pyproject.toml"
    )
    assert needed, "pyproject 的 hatch-test 額外依賴解析不到，測試本身失效"
    declared = {
        checker.normalize_name(package["name"])
        for name in ("requirements.txt", "requirements-all.txt")
        for package in checker.parse_requirements(
            (ROOT / name).read_text(encoding="utf-8"), name
        )
    }
    missing = sorted(
        requirement
        for requirement in needed
        if checker.normalize_name(re.split(r"[<>=!~\[ ;]", requirement, 1)[0]) not in declared
    )
    assert not missing, f"requirements-all.txt 缺少產品測試依賴: {missing}"
