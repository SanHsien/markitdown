from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "packages" / "markitdown" / "src" / "markitdown" / "_uri_utils.py"

# 使用 importlib 直接載入單檔，避免觸發 markitdown/__init__.py 的產品依賴 (requests)
spec = importlib.util.spec_from_file_location("_uri_utils", str(MODULE_PATH))
if spec is None or spec.loader is None:
    raise ImportError(f"Cannot load spec from {MODULE_PATH}")
uri_utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(uri_utils)

_is_unc_or_device_path = uri_utils._is_unc_or_device_path
file_uri_to_path = uri_utils.file_uri_to_path
parse_data_uri = uri_utils.parse_data_uri


def test_is_unc_or_device_path_identifies_risky_paths() -> None:
    assert _is_unc_or_device_path(r"\\server\share\file.txt")
    assert _is_unc_or_device_path("//server/share/file.txt")
    assert _is_unc_or_device_path(r"\\.\COM1")
    assert _is_unc_or_device_path(r"\\?\C:\test.txt")
    assert not _is_unc_or_device_path(r"C:\safe\path.txt")
    assert not _is_unc_or_device_path("/usr/local/bin")


def test_file_uri_to_path_rejects_unc_and_device_namespaces() -> None:
    with pytest.raises(ValueError, match="UNC and Windows device paths are not supported"):
        file_uri_to_path("file:////server/share/file.txt")

    with pytest.raises(ValueError, match="UNC and Windows device paths are not supported"):
        file_uri_to_path("file://///./COM1")

    with pytest.raises(ValueError, match="Not a file URL"):
        file_uri_to_path("https://example.com/file.txt")

    netloc, path = file_uri_to_path("file:///C:/test.txt")
    assert netloc is None
    assert path.endswith("test.txt")


def test_parse_data_uri_validates_and_extracts_payloads() -> None:
    mime, attrs, content = parse_data_uri("data:text/plain;base64,SGVsbG8gV29ybGQ=")
    assert mime == "text/plain"
    assert content == b"Hello World"

    mime, attrs, content = parse_data_uri("data:text/plain;charset=utf-8,Hello%20World")
    assert mime == "text/plain"
    assert attrs.get("charset") == "utf-8"
    assert content == b"Hello World"

    with pytest.raises(ValueError, match="Not a data URI"):
        parse_data_uri("http://example.com")

    with pytest.raises(ValueError, match="Malformed data URI"):
        parse_data_uri("data:text/plain")
