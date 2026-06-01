"""
Tests for the CLI module.

Covers:
- Argument parsing
- File input validation
- Text input validation
- Mutually exclusive input handling
- Invalid k values
- Debug mode
- Output formatting
- Integration with tokenizer and counter
"""

import tempfile
from pathlib import Path
from unittest.mock import patch
import pytest

from starter_repo.cli import (
    debug_log,
    format_output,
    read_input,
    validate_k,
)


class TestDebugLog:
    """Test suite for debug_log function."""

    def test_debug_log_enabled(self, capsys) -> None:
        """Test that debug_log prints when debug=True."""
        debug_log("Test message", debug=True)
        captured = capsys.readouterr()
        # debug_log prints to stderr
        assert "[DEBUG] Test message" in captured.err

    def test_debug_log_disabled(self, capsys) -> None:
        """Test that debug_log doesn't print when debug=False."""
        debug_log("Test message", debug=False)
        captured = capsys.readouterr()
        assert captured.err == ""

    def test_debug_log_multiple_messages(self, capsys) -> None:
        """Test multiple debug log messages."""
        debug_log("Message 1", debug=True)
        debug_log("Message 2", debug=True)
        captured = capsys.readouterr()
        assert "[DEBUG] Message 1" in captured.err
        assert "[DEBUG] Message 2" in captured.err


class TestReadInput:
    """Test suite for read_input function."""

    def test_read_from_file(self) -> None:
        """Test reading from a valid file."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt", encoding="utf-8") as f:
            f.write("Hello, World!")
            temp_path = f.name

        try:
            result = read_input(temp_path, None)
            assert result == "Hello, World!"
        finally:
            Path(temp_path).unlink()

    def test_read_from_text(self) -> None:
        """Test reading from direct text input."""
        result = read_input(None, "Direct text input")
        assert result == "Direct text input"

    def test_file_not_found(self, capsys) -> None:
        """Test error when file doesn't exist."""
        with pytest.raises(SystemExit) as exc_info:
            read_input("/nonexistent/file.txt", None)
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "File not found" in captured.err

    def test_both_file_and_text_provided(self, capsys) -> None:
        """Test error when both file and text are provided."""
        with pytest.raises(SystemExit) as exc_info:
            read_input("file.txt", "text")
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Cannot provide both" in captured.err

    def test_neither_file_nor_text_provided(self, capsys) -> None:
        """Test error when neither file nor text are provided."""
        with pytest.raises(SystemExit) as exc_info:
            read_input(None, None)
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Must provide either" in captured.err

    def test_read_file_with_unicode(self) -> None:
        """Test reading file with valid UTF-8 content."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt", encoding="utf-8") as f:
            f.write("Hello, World! 你好")
            temp_path = f.name

        try:
            result = read_input(temp_path, None)
            assert "Hello, World!" in result
        finally:
            Path(temp_path).unlink()

    def test_read_empty_file(self) -> None:
        """Test reading an empty file."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt", encoding="utf-8") as f:
            temp_path = f.name

        try:
            result = read_input(temp_path, None)
            assert result == ""
        finally:
            Path(temp_path).unlink()

    def test_file_path_is_directory(self, capsys) -> None:
        """Test error when path points to a directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with pytest.raises(SystemExit) as exc_info:
                read_input(temp_dir, None)
            assert exc_info.value.code == 1
            captured = capsys.readouterr()
            assert "Not a file" in captured.err

    def test_read_file_with_encoding_error(self, capsys) -> None:
        """Test error when file has encoding issues."""
        with tempfile.NamedTemporaryFile(mode="wb", delete=False, suffix=".txt") as f:
            # Write invalid UTF-8 bytes
            f.write(b'\x80\x81\x82\x83')
            temp_path = f.name

        try:
            with pytest.raises(SystemExit) as exc_info:
                read_input(temp_path, None)
            assert exc_info.value.code == 1
            captured = capsys.readouterr()
            assert "encoding error" in captured.err
        finally:
            Path(temp_path).unlink()

    def test_read_file_with_oserror(self, capsys) -> None:
        """Test error when file cannot be read due to OS error."""
        with patch("pathlib.Path.exists", return_value=True):
            with patch("pathlib.Path.is_file", return_value=True):
                with patch("pathlib.Path.read_text", side_effect=OSError("Permission denied")):
                    with pytest.raises(SystemExit) as exc_info:
                        read_input("some_file.txt", None)
                    assert exc_info.value.code == 1
                    captured = capsys.readouterr()
                    assert "Could not read file" in captured.err


class TestValidateK:
    """Test suite for validate_k function."""

    def test_valid_k(self) -> None:
        """Test that valid k values don't raise errors."""
        validate_k(1)
        validate_k(10)
        validate_k(1000)

    def test_k_zero(self, capsys) -> None:
        """Test that k=0 raises error."""
        with pytest.raises(SystemExit) as exc_info:
            validate_k(0)
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "k must be a positive integer" in captured.err

    def test_k_negative(self, capsys) -> None:
        """Test that k<0 raises error."""
        with pytest.raises(SystemExit) as exc_info:
            validate_k(-5)
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "k must be a positive integer" in captured.err


class TestFormatOutput:
    """Test suite for format_output function."""

    def test_format_single_result(self) -> None:
        """Test formatting a single result."""
        results = [("apple", 5)]
        output = format_output(results)
        assert output == "apple: 5"

    def test_format_multiple_results(self) -> None:
        """Test formatting multiple results."""
        results = [("apple", 5), ("banana", 3), ("cherry", 1)]
        output = format_output(results)
        expected = "apple: 5\nbanana: 3\ncherry: 1"
        assert output == expected

    def test_format_empty_results(self) -> None:
        """Test formatting empty results."""
        output = format_output([])
        assert output == ""

    def test_format_preserves_order(self) -> None:
        """Test that formatting preserves order."""
        results = [("zebra", 10), ("apple", 10), ("banana", 5)]
        output = format_output(results)
        lines = output.split("\n")
        assert lines[0] == "zebra: 10"
        assert lines[1] == "apple: 10"
        assert lines[2] == "banana: 5"


class TestIntegration:
    """Integration tests for CLI components."""

    def test_full_pipeline_with_file(self) -> None:
        """Test full pipeline reading from file."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write("apple banana apple cherry banana apple")
            temp_path = f.name

        try:
            from starter_repo.tokenizer import normalize_and_tokenize
            from starter_repo.counter import count_frequency, get_top_k

            raw_text = read_input(temp_path, None)
            words = normalize_and_tokenize(raw_text)
            freq_map = count_frequency(words)
            results = get_top_k(freq_map, 2)

            assert results == [("apple", 3), ("banana", 2)]
        finally:
            Path(temp_path).unlink()

    def test_full_pipeline_with_text(self) -> None:
        """Test full pipeline with direct text input."""
        from starter_repo.tokenizer import normalize_and_tokenize
        from starter_repo.counter import count_frequency, get_top_k

        raw_text = read_input(None, "apple banana apple cherry banana apple")
        words = normalize_and_tokenize(raw_text)
        freq_map = count_frequency(words)
        results = get_top_k(freq_map, 2)

        assert results == [("apple", 3), ("banana", 2)]

    def test_empty_input_handling(self) -> None:
        """Test that empty input is handled gracefully."""
        output = format_output([])
        assert output == ""

    def test_cli_with_debug_output(self, capsys) -> None:
        """Test that debug output is produced."""
        debug_log("Test message", debug=True)
        captured = capsys.readouterr()
        assert "[DEBUG]" in captured.err

    def test_cli_without_debug_output(self, capsys) -> None:
        """Test that debug output is suppressed when disabled."""
        debug_log("Test message", debug=False)
        captured = capsys.readouterr()
        assert "[DEBUG]" not in captured.err
