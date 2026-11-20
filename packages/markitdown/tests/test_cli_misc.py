"""CLI behavior outside the shared file-vector matrix."""

import io
import os
import subprocess
import sys
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from markitdown import __version__
from markitdown import DocumentConverterResult
import markitdown.__main__ as cli
from markitdown.__main__ import _handle_output, main
from markitdown.converters._cu_converter import ContentUnderstandingFileType

# CLI behavior

# This file contains CLI tests that are not directly tested by the FileTestVectors.
# This includes things like help messages, version numbers, and invalid flags.


def test_version() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "markitdown", "--version"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, f"CLI exited with error: {result.stderr}"
    assert __version__ in result.stdout, f"Version not found in output: {result.stdout}"


def test_docintel_help_lists_features_and_charges() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "markitdown", "--help"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, f"CLI exited with error: {result.stderr}"
    help_text = " ".join(result.stdout.split())
    assert (
        "barcodes, formulas, keyValuePairs, languages, ocrHighResolution, and styleFont"
        in help_text
    )
    assert "incur additional charges" in help_text
    assert "No add-ons are enabled by default" in help_text
    assert "billable Document Intelligence queryFields add-on" in help_text


def test_invalid_flag() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "markitdown", "--foobar"],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0, f"CLI exited with error: {result.stderr}"
    assert (
        "unrecognized arguments" in result.stderr
    ), "Expected 'unrecognized arguments' to appear in STDERR"
    assert "SYNTAX" in result.stderr, "Expected 'SYNTAX' to appear in STDERR"


def test_windows_pipe_input_is_buffered_before_conversion(monkeypatch, capsys) -> None:
    class WindowsPipe(io.BytesIO):
        def seek(self, offset: int, whence: int = io.SEEK_SET) -> int:
            if whence == io.SEEK_END:
                return super().seek(offset, whence)
            return 0

    stdin = SimpleNamespace(
        buffer=WindowsPipe(b"<html><body><h1>Test HTML</h1></body></html>")
    )
    monkeypatch.setattr(sys, "stdin", stdin)
    monkeypatch.setattr(sys, "argv", ["markitdown", "-x", "html"])

    main()

    captured = capsys.readouterr()
    assert captured.out.strip() == "# Test HTML"


# Service flags and endpoints

# ---------------------------------------------------------------------------
# CLI argument tests
# ---------------------------------------------------------------------------


class TestCLIArgs:
    """Test CLI argument parsing for CU flags."""

    def test_use_cu_without_endpoint_exits(self):
        """--use-cu without --cu-endpoint should exit with error."""
        import subprocess

        result = subprocess.run(
            [sys.executable, "-m", "markitdown", "--use-cu", "fake.pdf"],
            capture_output=True,
            text=True,
            env={**os.environ, "MARKITDOWN_CU_ENDPOINT": ""},
        )
        assert result.returncode != 0
        assert (
            "cu-endpoint" in result.stderr.lower()
            or "cu-endpoint" in (result.stdout or "").lower()
        )

    def test_use_cu_and_use_docintel_mutually_exclusive(self):
        """--use-cu and --use-docintel cannot be used together."""
        import subprocess

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "markitdown",
                "--use-cu",
                "--cu-endpoint",
                "https://fake",
                "--use-docintel",
                "-e",
                "https://fake-di",
                "fake.pdf",
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 2, result.stderr
        assert (
            "argument -d/--use-docintel: not allowed with argument "
            "--use-cu/--use-content-understanding"
        ) in result.stderr, result.stderr

    @pytest.mark.parametrize(
        "raw_features, expected_features",
        [
            ("formulas,ocrHighResolution", ["formulas", "ocrHighResolution"]),
            ("none", []),
        ],
    )
    def test_use_docintel_wires_configuration(
        self, monkeypatch, capsys, raw_features, expected_features
    ):
        import markitdown.__main__ as markitdown_cli

        markitdown_instance = MagicMock()
        markitdown_instance.convert.return_value.markdown = "converted"
        markitdown_cls = MagicMock(return_value=markitdown_instance)
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "markitdown",
                "--use-docintel",
                "--endpoint",
                "https://fake-di",
                "--docintel-model-id",
                "prebuilt-read",
                "--docintel-features",
                raw_features,
                "--docintel-query-fields",
                "Title,Author",
                "fake.pdf",
            ],
        )
        monkeypatch.setattr(markitdown_cli, "MarkItDown", markitdown_cls)

        markitdown_cli.main()

        markitdown_cls.assert_called_once_with(
            enable_plugins=False,
            docintel_endpoint="https://fake-di",
            docintel_model_id="prebuilt-read",
            docintel_features=expected_features,
            docintel_query_fields=["Title", "Author"],
        )
        markitdown_instance.convert.assert_called_once_with(
            "fake.pdf", stream_info=None, keep_data_uris=False
        )
        assert capsys.readouterr().out == "converted\n"

    @pytest.mark.parametrize("raw", ["pdf,jpeg,wav", " , PDF, JPEG,, WAV, "])
    @pytest.mark.parametrize(
        "filename, content_type, analyzer",
        [
            ("test.pdf", "application/pdf", "prebuilt-documentSearch"),
            ("test.jpg", "image/jpeg", "prebuilt-documentSearch"),
            ("test.wav", "audio/wav", "prebuilt-audioSearch"),
        ],
    )
    def test_cu_file_types_parsing(
        self, monkeypatch, capsys, raw, filename, content_type, analyzer
    ):
        self._check_cu_file_types(
            monkeypatch, capsys, raw, filename, content_type, analyzer
        )

    def test_cu_file_types_single_value(self, monkeypatch, capsys):
        self._check_cu_file_types(
            monkeypatch, capsys, "wav", "test.wav", "audio/wav", "prebuilt-audioSearch"
        )

    def _check_cu_file_types(
        self, monkeypatch, capsys, raw, filename, content_type, analyzer
    ):
        from azure.ai.contentunderstanding.models import AnalysisResult, DocumentContent
        from markitdown.converters import _cu_converter

        client = MagicMock()
        client.begin_analyze_binary.return_value.result.return_value = AnalysisResult(
            contents=[DocumentContent(kind="document", markdown="# Parsed CLI input")]
        )
        client_cls = MagicMock(return_value=client)
        monkeypatch.setattr(_cu_converter, "ContentUnderstandingClient", client_cls)
        monkeypatch.setenv("AZURE_API_KEY", "test-key")
        path = os.path.join(os.path.dirname(__file__), "test_files", filename)
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "markitdown",
                "--use-cu",
                "--cu-endpoint",
                "https://fake-cu",
                "--cu-file-types",
                raw,
                path,
            ],
        )

        main()

        client_cls.assert_called_once()
        client.begin_analyze_binary.assert_called_once()
        request = client.begin_analyze_binary.call_args.kwargs
        assert request["analyzer_id"] == analyzer
        assert request["content_type"] == content_type
        assert "# Parsed CLI input" in capsys.readouterr().out

        # An excluded format must use its local converter, not the CU service.
        # This also catches a CLI that silently ignores --cu-file-types.
        client.begin_analyze_binary.reset_mock()
        html_path = os.path.join(
            os.path.dirname(__file__), "test_files", "test_blog.html"
        )
        monkeypatch.setattr(sys, "argv", sys.argv[:-1] + [html_path])
        main()
        client.begin_analyze_binary.assert_not_called()
        output = capsys.readouterr().out
        assert "Large language models" in output
        assert "# Parsed CLI input" not in output

    @pytest.mark.parametrize("raw", ["nonsense", "pdf,nonsense"])
    def test_cu_file_types_invalid_value(self, monkeypatch, capsys, raw):
        from markitdown.converters import _cu_converter

        client_cls = MagicMock()
        monkeypatch.setattr(_cu_converter, "ContentUnderstandingClient", client_cls)
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "markitdown",
                "--use-cu",
                "--cu-endpoint",
                "https://fake-cu",
                "--cu-file-types",
                raw,
                "unused.pdf",
            ],
        )

        with pytest.raises(SystemExit) as exc:
            main()

        assert exc.value.code == 1
        assert "Unknown file type: nonsense" in capsys.readouterr().out
        client_cls.assert_not_called()

    def test_use_cu_wires_kwargs_to_markitdown(self, capsys):
        """--use-cu should pass CU options through to MarkItDown."""
        import markitdown.__main__ as markitdown_cli

        markitdown_instance = MagicMock()
        markitdown_instance.convert.return_value.markdown = "converted"
        markitdown_cls = MagicMock(return_value=markitdown_instance)

        with patch.object(
            sys,
            "argv",
            [
                "markitdown",
                "--use-cu",
                "--cu-endpoint",
                "https://fake-cu",
                "--cu-analyzer",
                "custom-analyzer",
                "--cu-file-types",
                "pdf,jpeg,mp4",
                "fake.pdf",
            ],
        ), patch.object(markitdown_cli, "MarkItDown", markitdown_cls):
            markitdown_cli.main()

        markitdown_cls.assert_called_once_with(
            enable_plugins=False,
            cu_endpoint="https://fake-cu",
            cu_analyzer_id="custom-analyzer",
            cu_file_types=[
                ContentUnderstandingFileType.PDF,
                ContentUnderstandingFileType.JPEG,
                ContentUnderstandingFileType.MP4,
            ],
        )
        markitdown_instance.convert.assert_called_once_with(
            "fake.pdf", stream_info=None, keep_data_uris=False
        )
        assert capsys.readouterr().out == "converted\n"

    def test_use_cu_reads_from_stdin(self, capsys):
        """--use-cu should preserve the CLI's filename-optional stdin mode."""
        import markitdown.__main__ as markitdown_cli

        input_buffer = io.BytesIO(b"fake pdf")
        stdin = MagicMock(buffer=input_buffer)
        markitdown_instance = MagicMock()
        markitdown_instance.convert_stream.return_value.markdown = "converted"
        markitdown_cls = MagicMock(return_value=markitdown_instance)

        with patch.object(
            sys,
            "argv",
            [
                "markitdown",
                "--use-cu",
                "--cu-endpoint",
                "https://fake-cu",
            ],
        ), patch.object(sys, "stdin", stdin), patch.object(
            markitdown_cli, "MarkItDown", markitdown_cls
        ):
            markitdown_cli.main()

        markitdown_cls.assert_called_once_with(
            enable_plugins=False,
            cu_endpoint="https://fake-cu",
        )

        assert markitdown_instance.convert_stream.call_count == 1
        call_args, call_kwargs = markitdown_instance.convert_stream.call_args
        assert call_args[0].read() == b"fake pdf"
        assert call_kwargs == {"stream_info": None, "keep_data_uris": False}
        assert capsys.readouterr().out == "converted\n"


# ---------------------------------------------------------------------------
# Endpoint environment variables (issue #2326)
# ---------------------------------------------------------------------------


class TestEndpointEnvVars:
    """Endpoint flags fall back to operator-configured environment variables."""

    @pytest.mark.parametrize(
        "env_var, argv, kwarg",
        [
            (
                "MARKITDOWN_CU_ENDPOINT",
                ["markitdown", "--use-cu", "fake.pdf"],
                "cu_endpoint",
            ),
            (
                "MARKITDOWN_DOCINTEL_ENDPOINT",
                ["markitdown", "-d", "fake.pdf"],
                "docintel_endpoint",
            ),
        ],
    )
    def test_endpoint_read_from_environment(self, monkeypatch, env_var, argv, kwarg):
        """With the env var set, the endpoint flag can be omitted entirely."""
        from markitdown.__main__ import main

        monkeypatch.setenv(env_var, "https://from-env")
        monkeypatch.setattr(sys, "argv", argv)

        with patch("markitdown.__main__.MarkItDown") as mock_markitdown:
            mock_markitdown.return_value.convert.return_value.markdown = "ok"
            main()

        assert mock_markitdown.call_args.kwargs[kwarg] == "https://from-env"

    def test_flag_overrides_environment(self, monkeypatch):
        """Fails if the env var is ever read after parsing instead of as an argparse default."""
        from markitdown.__main__ import main

        monkeypatch.setenv("MARKITDOWN_CU_ENDPOINT", "https://from-env")
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "markitdown",
                "--use-cu",
                "--cu-endpoint",
                "https://from-flag",
                "fake.pdf",
            ],
        )

        with patch("markitdown.__main__.MarkItDown") as mock_markitdown:
            mock_markitdown.return_value.convert.return_value.markdown = "ok"
            main()

        assert mock_markitdown.call_args.kwargs["cu_endpoint"] == "https://from-flag"

    def test_empty_environment_variable_is_treated_as_unset(self, monkeypatch, capsys):
        """An empty env var must not pass as a valid endpoint."""
        from markitdown.__main__ import main

        monkeypatch.setenv("MARKITDOWN_CU_ENDPOINT", "")
        monkeypatch.setattr(sys, "argv", ["markitdown", "--use-cu", "fake.pdf"])

        with pytest.raises(SystemExit):
            main()

        assert "MARKITDOWN_CU_ENDPOINT" in capsys.readouterr().out


# Output encoding (upstream PR 2803 design, adapted to the Windows consumer)


_TEXT = "It’s “quote” 台北 café."


def _flags(utf8_mode: int) -> SimpleNamespace:
    # Copy every flag so pytest internals that read sys.flags keep working.
    names = [name for name in dir(sys.flags) if not name.startswith("_")]
    values = {name: getattr(sys.flags, name) for name in names}
    return SimpleNamespace(**dict(values, utf8_mode=utf8_mode))


def _clean_environment(**extra: str) -> dict[str, str]:
    environment = {
        key: value
        for key, value in os.environ.items()
        if key not in ("PYTHONIOENCODING", "PYTHONUTF8")
    }
    environment.update(extra)
    return environment


@pytest.mark.parametrize("stdio_encoding", ["utf-8", "cp950", "cp1252", "ascii"])
def test_explicit_pythonioencoding_is_honored_for_redirected_output(
    tmp_path, stdio_encoding
):
    source = tmp_path / "unicode.txt"
    source.write_text(_TEXT, encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "markitdown", str(source), "-c", "utf-8"],
        capture_output=True,
        env=_clean_environment(PYTHONIOENCODING=stdio_encoding),
        check=False,
    )

    assert result.returncode == 0, result.stderr.decode("ascii", errors="replace")
    assert result.stdout.strip() == _TEXT.encode(stdio_encoding, errors="replace")


def test_stdout_redirected_to_a_file_is_utf8(tmp_path):
    # cmd.exe `>` hands the process a disk file: write UTF-8, the same as `-o`,
    # whatever the legacy code page is (upstream issue 1219).
    source = tmp_path / "unicode.txt"
    source.write_text(_TEXT, encoding="utf-8")
    target = tmp_path / "out.md"

    with open(target, "wb") as stdout:
        result = subprocess.run(
            [sys.executable, "-m", "markitdown", str(source), "-c", "utf-8"],
            stdout=stdout,
            stderr=subprocess.PIPE,
            env=_clean_environment(),
            check=False,
        )

    assert result.returncode == 0, result.stderr.decode("ascii", errors="replace")
    assert target.read_bytes().decode("utf-8").strip() == _TEXT


@pytest.mark.parametrize(
    ("platform", "code_page", "expected"),
    [
        # PowerShell decodes piped/captured native output with the console code page.
        ("win32", 950, "cp950"),
        ("win32", 437, "cp437"),
        ("win32", 65001, "utf-8"),
        # Not a pipe, or no console attached: same as `-o`.
        ("win32", None, "utf-8"),
        # A code page Python has no codec for must not crash the output.
        ("win32", 54936000, "utf-8"),
        ("linux", 950, "utf-8"),
    ],
)
def test_redirected_encoding_follows_the_consumer_without_explicit_override(
    monkeypatch, platform, code_page, expected
):
    monkeypatch.delenv("PYTHONIOENCODING", raising=False)
    monkeypatch.setattr(cli.sys, "flags", _flags(0))
    monkeypatch.setattr(cli.sys, "platform", platform)
    monkeypatch.setattr(
        cli, "_windows_pipe_console_code_page", lambda stdout: code_page
    )
    stdout = SimpleNamespace(encoding="cp1252")

    assert cli._redirected_stdout_encoding(stdout) == expected


@pytest.mark.parametrize(
    ("environment", "utf8_mode"), [({"PYTHONIOENCODING": "cp1252"}, 0), ({}, 1)]
)
def test_explicit_python_encoding_overrides_the_console_code_page(
    monkeypatch, environment, utf8_mode
):
    monkeypatch.delenv("PYTHONIOENCODING", raising=False)
    for key, value in environment.items():
        monkeypatch.setenv(key, value)
    monkeypatch.setattr(cli.sys, "flags", _flags(utf8_mode))
    monkeypatch.setattr(cli.sys, "platform", "win32")
    monkeypatch.setattr(cli, "_windows_pipe_console_code_page", lambda stdout: 950)
    stdout = SimpleNamespace(encoding="cp1252" if environment else "utf-8")

    assert cli._redirected_stdout_encoding(stdout) == stdout.encoding


def test_piped_output_in_a_code_page_replaces_unencodable_text(monkeypatch):
    buffer = io.BytesIO()
    stdout = io.TextIOWrapper(buffer, encoding="utf-8")
    monkeypatch.setattr(stdout, "isatty", lambda: False)
    monkeypatch.setattr(sys, "stdout", stdout)
    monkeypatch.setattr(cli, "_redirected_stdout_encoding", lambda stdout: "cp950")

    _handle_output(
        SimpleNamespace(output=None), DocumentConverterResult(markdown=_TEXT)
    )

    assert buffer.getvalue() == (_TEXT + "\n").encode("cp950", errors="replace")


def test_interactive_stdout_uses_the_terminal_encoding(monkeypatch):
    buffer = io.BytesIO()
    stdout = io.TextIOWrapper(buffer, encoding="cp1252")
    monkeypatch.setattr(stdout, "isatty", lambda: True)
    monkeypatch.setattr(sys, "stdout", stdout)

    _handle_output(
        SimpleNamespace(output=None), DocumentConverterResult(markdown="“台北”")
    )
    stdout.flush()

    assert buffer.getvalue().decode("cp1252").strip() == "“??”"


def test_text_only_stdout_preserves_unicode(monkeypatch):
    stdout = io.StringIO()
    monkeypatch.setattr(sys, "stdout", stdout)

    _handle_output(
        SimpleNamespace(output=None), DocumentConverterResult(markdown="“台北”")
    )

    assert stdout.getvalue() == "“台北”\n"


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
