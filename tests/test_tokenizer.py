"""
Tests for the tokenizer module.

Covers:
- Text normalization (lowercase conversion)
- Punctuation handling (keeping apostrophes and hyphens, removing others)
- Number handling (ignored)
- Empty and whitespace-only input
- Real-world examples
"""

from starter_repo.tokenizer import normalize_and_tokenize


class TestNormalizeAndTokenize:
    """Test suite for normalize_and_tokenize function."""

    # ===== Basic Functionality =====
    def test_simple_text(self) -> None:
        """Test basic text tokenization."""
        result = normalize_and_tokenize("hello world")
        assert result == ["hello", "world"]

    def test_lowercase_conversion(self) -> None:
        """Test that text is converted to lowercase."""
        result = normalize_and_tokenize("Hello World TESTING")
        assert result == ["hello", "world", "testing"]

    def test_mixed_case(self) -> None:
        """Test mixed case handling."""
        result = normalize_and_tokenize("HeLLo WoRLd")
        assert result == ["hello", "world"]

    # ===== Punctuation Handling =====
    def test_common_punctuation_removed(self) -> None:
        """Test that common punctuation is removed."""
        result = normalize_and_tokenize("Hello, world! How are you?")
        assert result == ["hello", "world", "how", "are", "you"]

    def test_apostrophes_preserved(self) -> None:
        """Test that apostrophes in words are preserved."""
        result = normalize_and_tokenize("don't")
        assert result == ["don't"]

    def test_multiple_apostrophes(self) -> None:
        """Test words with multiple apostrophes."""
        result = normalize_and_tokenize("don't you've shouldn't")
        assert result == ["don't", "you've", "shouldn't"]

    def test_hyphens_preserved(self) -> None:
        """Test that hyphens in words are preserved."""
        result = normalize_and_tokenize("co-operate")
        assert result == ["co-operate"]

    def test_multiple_hyphens(self) -> None:
        """Test words with multiple hyphens."""
        result = normalize_and_tokenize("state-of-the-art well-known")
        assert result == ["state-of-the-art", "well-known"]

    def test_apostrophes_and_hyphens_together(self) -> None:
        """Test words with both apostrophes and hyphens."""
        result = normalize_and_tokenize("don't co-operate it's self-aware")
        assert result == ["don't", "co-operate", "it's", "self-aware"]

    def test_quotes_removed(self) -> None:
        """Test that quotes are treated as delimiters."""
        result = normalize_and_tokenize("\"hello\" 'world'")
        assert result == ["hello", "world"]

    # ===== Number Handling =====
    def test_numbers_ignored_standalone(self) -> None:
        """Test that standalone numbers are ignored."""
        result = normalize_and_tokenize("one 2 three 4 five")
        assert result == ["one", "three", "five"]

    def test_numbers_in_middle_of_word(self) -> None:
        """Test that numbers attached to words split the word."""
        result = normalize_and_tokenize("hello123world test456")
        # "hello123world" becomes "hello" and "world" (123 acts as delimiter)
        assert result == ["hello", "world", "test"]

    def test_numbers_ignored_completely(self) -> None:
        """Test pure numbers are ignored."""
        result = normalize_and_tokenize("123 456 789")
        assert result == []

    # ===== Empty and Whitespace Input =====
    def test_empty_string(self) -> None:
        """Test empty string returns empty list."""
        result = normalize_and_tokenize("")
        assert result == []

    def test_whitespace_only(self) -> None:
        """Test whitespace-only string returns empty list."""
        result = normalize_and_tokenize("   ")
        assert result == []

    def test_tabs_and_newlines(self) -> None:
        """Test tabs and newlines as delimiters."""
        result = normalize_and_tokenize("hello\tworld\ntest")
        assert result == ["hello", "world", "test"]

    # ===== Real-world Examples =====
    def test_sentence_with_punctuation(self) -> None:
        """Test real sentence."""
        result = normalize_and_tokenize("Hello, world! Don't worry.")
        assert result == ["hello", "world", "don't", "worry"]

    def test_multiple_spaces(self) -> None:
        """Test multiple spaces as delimiters."""
        result = normalize_and_tokenize("hello    world   test")
        assert result == ["hello", "world", "test"]

    def test_special_characters_removed(self) -> None:
        """Test that special characters are removed."""
        result = normalize_and_tokenize("hello@world#test$value")
        assert result == ["hello", "world", "test", "value"]

    def test_real_paragraph(self) -> None:
        """Test a real-world paragraph."""
        text = (
            "It's the best of times, it's the worst of times. "
            "The quick brown fox—don't worry—jumps over the lazy dog."
        )
        result = normalize_and_tokenize(text)
        expected = [
            "it's",
            "the",
            "best",
            "of",
            "times",
            "it's",
            "the",
            "worst",
            "of",
            "times",
            "the",
            "quick",
            "brown",
            "fox",
            "don't",
            "worry",
            "jumps",
            "over",
            "the",
            "lazy",
            "dog",
        ]
        assert result == expected

    # ===== Edge Cases =====
    def test_only_apostrophes(self) -> None:
        """Test string of only apostrophes returns no tokens."""
        result = normalize_and_tokenize("'''")
        assert result == []

    def test_only_hyphens(self) -> None:
        """Test string of only hyphens returns no tokens."""
        result = normalize_and_tokenize("---")
        assert result == []

    def test_mixed_only_apostrophes_and_hyphens(self) -> None:
        """Test string of apostrophes and hyphens returns no tokens."""
        result = normalize_and_tokenize("'-'-'")
        assert result == []

    def test_duplicates_preserved(self) -> None:
        """Test that duplicate words are preserved in output."""
        result = normalize_and_tokenize("apple banana apple")
        assert result == ["apple", "banana", "apple"]

    def test_duplicate_counts_case_insensitive(self) -> None:
        """Test counting duplicate words with mixed case input."""
        result = normalize_and_tokenize("Apple apple APPLE banana Banana")
        assert result.count("apple") == 3
        assert result.count("banana") == 2

    def test_unicode_text_preserved(self) -> None:
        """Test that accented Latin letters are preserved as part of words."""
        result = normalize_and_tokenize("café naïve")
        assert result == ["café", "naïve"]
