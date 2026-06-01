"""
Tests for the CLI main function.

Covers:
- Full pipeline execution with file input
- Full pipeline execution with text input
- Debug mode output
- Empty and whitespace-only input handling
- Argument parsing integration
- Integration with tokenizer and counter
- Output to stdout
"""

import tempfile
from pathlib import Path
from unittest.mock import patch
import pytest

from starter_repo.cli import main


class TestMainWithFileInput:
    """Test suite for main() function with file input."""

    def test_main_with_file_and_debug_enabled(self, capsys) -> None:
        """Test main() with file input and debug logging enabled."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write("apple banana apple cherry banana apple")
            temp_path = f.name

        try:
            with patch("sys.argv", ["topk", temp_path, "-k", "2", "--debug"]):
                main()

            captured = capsys.readouterr()
            # Check output contains top-2 words
            assert "apple: 3" in captured.out
            assert "banana: 2" in captured.out
            # Check debug output is present
            assert "[DEBUG]" in captured.err
            assert "Input source: file" in captured.err
            assert "Tokens extracted:" in captured.err
            assert "Unique words:" in captured.err
            assert "Top-2 words computed" in captured.err
        finally:
            Path(temp_path).unlink()

    def test_main_with_file_and_debug_disabled(self, capsys) -> None:
        """Test main() with file input and debug logging disabled."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write("apple banana apple cherry banana apple")
            temp_path = f.name

        try:
            with patch("sys.argv", ["topk", temp_path, "-k", "2"]):
                main()

            captured = capsys.readouterr()
            # Check output contains top-2 words
            assert "apple: 3" in captured.out
            assert "banana: 2" in captured.out
            # Check debug output is NOT present
            assert "[DEBUG]" not in captured.err
        finally:
            Path(temp_path).unlink()

    def test_main_with_file_single_top_result(self, capsys) -> None:
        """Test main() with file input requesting single top result."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write("dog dog dog cat cat bird")
            temp_path = f.name

        try:
            with patch("sys.argv", ["topk", temp_path, "-k", "1"]):
                main()

            captured = capsys.readouterr()
            assert "dog: 3" in captured.out
            # Should not have other words
            assert "cat:" not in captured.out
            assert "bird:" not in captured.out
        finally:
            Path(temp_path).unlink()

    def test_main_with_file_k_larger_than_unique_words(self, capsys) -> None:
        """Test main() when k is larger than number of unique words."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write("apple banana cherry")
            temp_path = f.name

        try:
            with patch("sys.argv", ["topk", temp_path, "-k", "10"]):
                main()

            captured = capsys.readouterr()
            # Should return all 3 words
            assert "apple: 1" in captured.out
            assert "banana: 1" in captured.out
            assert "cherry: 1" in captured.out
        finally:
            Path(temp_path).unlink()

    def test_main_with_file_empty_file(self, capsys) -> None:
        """Test main() with empty file."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            temp_path = f.name

        try:
            with patch("sys.argv", ["topk", temp_path, "-k", "5"]):
                main()

            captured = capsys.readouterr()
            # Should produce no output
            assert captured.out == ""
        finally:
            Path(temp_path).unlink()

    def test_main_with_file_whitespace_only(self, capsys) -> None:
        """Test main() with file containing only whitespace."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write("   \n\t\n   ")
            temp_path = f.name

        try:
            with patch("sys.argv", ["topk", temp_path, "-k", "3"]):
                main()

            captured = capsys.readouterr()
            # Should produce no output
            assert captured.out == ""
        finally:
            Path(temp_path).unlink()


class TestMainWithTextInput:
    """Test suite for main() function with text input."""

    def test_main_with_text_input_and_debug_enabled(self, capsys) -> None:
        """Test main() with text input and debug logging enabled."""
        with patch("sys.argv", ["topk", "--text", "apple banana apple cherry banana apple", "-k", "2", "--debug"]):
            main()

        captured = capsys.readouterr()
        # Check output contains top-2 words
        assert "apple: 3" in captured.out
        assert "banana: 2" in captured.out
        # Check debug output is present
        assert "[DEBUG]" in captured.err
        assert "Input source: text" in captured.err

    def test_main_with_text_input_and_debug_disabled(self, capsys) -> None:
        """Test main() with text input and debug logging disabled."""
        with patch("sys.argv", ["topk", "--text", "apple banana apple cherry banana apple", "-k", "2"]):
            main()

        captured = capsys.readouterr()
        # Check output contains top-2 words
        assert "apple: 3" in captured.out
        assert "banana: 2" in captured.out
        # Check debug output is NOT present
        assert "[DEBUG]" not in captured.err

    def test_main_with_text_single_word(self, capsys) -> None:
        """Test main() with text containing single word."""
        with patch("sys.argv", ["topk", "--text", "hello", "-k", "1"]):
            main()

        captured = capsys.readouterr()
        assert "hello: 1" in captured.out

    def test_main_with_text_whitespace_only(self, capsys) -> None:
        """Test main() with whitespace-only text input."""
        with patch("sys.argv", ["topk", "--text", "   \n\t\n   ", "-k", "3"]):
            main()

        captured = capsys.readouterr()
        # Should produce no output
        assert captured.out == ""

    def test_main_with_text_special_characters(self, capsys) -> None:
        """Test main() with text containing special characters."""
        with patch("sys.argv", ["topk", "--text", "hello! world? hello, world.", "-k", "2"]):
            main()

        captured = capsys.readouterr()
        # Punctuation should be removed by tokenizer
        assert "hello: 2" in captured.out
        assert "world: 2" in captured.out


class TestMainArgumentParsing:
    """Test suite for main() argument parsing and validation."""

    def test_main_missing_k_argument(self, capsys) -> None:
        """Test main() fails when -k is not provided."""
        with patch("sys.argv", ["topk", "--text", "hello world"]):
            with pytest.raises(SystemExit):
                main()
        captured = capsys.readouterr()
        assert "required" in captured.err.lower() or "argument" in captured.err.lower()

    def test_main_invalid_k_value_zero(self, capsys) -> None:
        """Test main() fails when k=0."""
        with patch("sys.argv", ["topk", "--text", "hello world", "-k", "0"]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
            captured = capsys.readouterr()
            assert "k must be a positive integer" in captured.err

    def test_main_invalid_k_value_negative(self, capsys) -> None:
        """Test main() fails when k is negative."""
        with patch("sys.argv", ["topk", "--text", "hello world", "-k", "-5"]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
            captured = capsys.readouterr()
            assert "k must be a positive integer" in captured.err

    def test_main_invalid_k_value_non_integer(self, capsys) -> None:
        """Test main() fails when k is not an integer."""
        with patch("sys.argv", ["topk", "--text", "hello world", "-k", "abc"]):
            with pytest.raises(SystemExit):
                main()
        captured = capsys.readouterr()
        assert "invalid" in captured.err.lower() or "int" in captured.err.lower()

    def test_main_no_input_source(self, capsys) -> None:
        """Test main() fails when neither file nor text is provided."""
        with patch("sys.argv", ["topk", "-k", "5"]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
            captured = capsys.readouterr()
            assert "Must provide either" in captured.err

    def test_main_both_file_and_text(self, capsys) -> None:
        """Test main() fails when both file and text are provided."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write("test")
            temp_path = f.name

        try:
            with patch("sys.argv", ["topk", temp_path, "--text", "hello", "-k", "5"]):
                with pytest.raises(SystemExit) as exc_info:
                    main()
                assert exc_info.value.code == 1
                captured = capsys.readouterr()
                assert "Cannot provide both" in captured.err
        finally:
            Path(temp_path).unlink()

    def test_main_file_not_found(self, capsys) -> None:
        """Test main() fails when file does not exist."""
        with patch("sys.argv", ["topk", "/nonexistent/file.txt", "-k", "5"]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
            captured = capsys.readouterr()
            assert "File not found" in captured.err


class TestMainOutputFormatting:
    """Test suite for main() output formatting."""

    def test_main_output_format_single_line(self, capsys) -> None:
        """Test output format for single word."""
        with patch("sys.argv", ["topk", "--text", "hello", "-k", "1"]):
            main()

        captured = capsys.readouterr()
        assert captured.out == "hello: 1\n"

    def test_main_output_format_multiple_lines(self, capsys) -> None:
        """Test output format for multiple words."""
        with patch("sys.argv", ["topk", "--text", "a a b b b c c c c", "-k", "3"]):
            main()

        captured = capsys.readouterr()
        lines = captured.out.strip().split("\n")
        assert len(lines) == 3
        assert lines[0] == "c: 4"
        assert lines[1] == "b: 3"
        assert lines[2] == "a: 2"

    def test_main_output_order_by_frequency(self, capsys) -> None:
        """Test that output is ordered by frequency (descending)."""
        with patch("sys.argv", ["topk", "--text", "zebra apple apple banana banana banana", "-k", "3"]):
            main()

        captured = capsys.readouterr()
        lines = captured.out.strip().split("\n")
        # Verify order: banana (3), apple (2), zebra (1)
        assert "banana: 3" in lines[0]
        assert "apple: 2" in lines[1]
        assert "zebra: 1" in lines[2]


class TestMainIntegration:
    """Integration tests for main() with complete workflows."""

    def test_main_complex_text_workflow(self, capsys) -> None:
        """Test main() with complex text containing multiple words."""
        text = "The quick brown fox jumps over the lazy dog. The fox is clever."
        with patch("sys.argv", ["topk", "--text", text, "-k", "5"]):
            main()

        captured = capsys.readouterr()
        # "the" should be most frequent
        assert "the: 3" in captured.out

    def test_main_case_insensitive(self, capsys) -> None:
        """Test that main() treats words case-insensitively."""
        with patch("sys.argv", ["topk", "--text", "Hello HELLO hello", "-k", "1"]):
            main()

        captured = capsys.readouterr()
        # All variations should be counted together as "hello"
        assert "hello: 3" in captured.out

    def test_main_with_numbers(self, capsys) -> None:
        """Test main() with text containing numbers."""
        with patch("sys.argv", ["topk", "--text", "item 123 item 456 item", "-k", "2"]):
            main()

        captured = capsys.readouterr()
        # Numbers should be removed by tokenizer, only "item" remains
        assert "item: 3" in captured.out

    def test_main_unicode_text(self, capsys) -> None:
        """Test main() with unicode text."""
        with patch("sys.argv", ["topk", "--text", "你好 世界 你好", "-k", "2"]):
            main()

        captured = capsys.readouterr()
        assert "你好: 2" in captured.out
