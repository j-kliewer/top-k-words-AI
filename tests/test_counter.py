"""
Tests for the counter module.

Covers:
- Frequency counting
- Top-K selection with proper sorting
- Tie-breaking (alphabetical order)
- Edge cases (k > vocabulary, k = 0, k < 0, empty input)
"""

import pytest

from starter_repo.counter import count_frequency, get_top_k


class TestCountFrequency:
    """Test suite for count_frequency function."""

    def test_simple_count(self) -> None:
        """Test basic frequency counting."""
        words = ["apple", "banana", "apple"]
        result = count_frequency(words)
        assert result == {"apple": 2, "banana": 1}

    def test_single_word(self) -> None:
        """Test counting single unique word."""
        result = count_frequency(["hello"])
        assert result == {"hello": 1}

    def test_all_same_word(self) -> None:
        """Test when all words are identical."""
        result = count_frequency(["word", "word", "word"])
        assert result == {"word": 3}

    def test_all_unique_words(self) -> None:
        """Test when all words are unique."""
        words = ["apple", "banana", "cherry"]
        result = count_frequency(words)
        assert result == {"apple": 1, "banana": 1, "cherry": 1}

    def test_empty_list(self) -> None:
        """Test empty word list."""
        result = count_frequency([])
        assert result == {}

    def test_preserves_case(self) -> None:
        """Test that case is preserved in keys (already lowercased by tokenizer)."""
        words = ["apple", "Apple", "APPLE"]  # Assuming tokenizer already lowercased
        # But just to be explicit, we test the counter behavior
        result = count_frequency(words)
        assert result == {"apple": 1, "Apple": 1, "APPLE": 1}  # Case-sensitive

    def test_large_frequency(self) -> None:
        """Test counting large frequencies."""
        words = ["word"] * 1000
        result = count_frequency(words)
        assert result == {"word": 1000}


class TestGetTopK:
    """Test suite for get_top_k function."""

    # ===== Basic Functionality =====
    def test_simple_top_k(self) -> None:
        """Test basic top-k selection."""
        freq = {"apple": 5, "banana": 3, "cherry": 2}
        result = get_top_k(freq, 2)
        assert result == [("apple", 5), ("banana", 3)]

    def test_k_equals_one(self) -> None:
        """Test k=1 returns only the top word."""
        freq = {"apple": 5, "banana": 3}
        result = get_top_k(freq, 1)
        assert result == [("apple", 5)]

    def test_k_equals_vocabulary_size(self) -> None:
        """Test k equals the number of unique words."""
        freq = {"apple": 5, "banana": 3, "cherry": 2}
        result = get_top_k(freq, 3)
        assert result == [("apple", 5), ("banana", 3), ("cherry", 2)]

    # ===== Tie-Breaking Tests =====
    def test_tie_breaking_alphabetical(self) -> None:
        """Test that ties are broken alphabetically."""
        freq = {"apple": 5, "banana": 5, "cherry": 5}
        result = get_top_k(freq, 3)
        # All have same frequency, so sorted alphabetically
        assert result == [("apple", 5), ("banana", 5), ("cherry", 5)]

    def test_tie_breaking_partial(self) -> None:
        """Test alphabetical tie-breaking with mixed frequencies."""
        freq = {"zebra": 5, "apple": 5, "banana": 3}
        result = get_top_k(freq, 3)
        # First two are tied at 5, should be alphabetical
        assert result == [("apple", 5), ("zebra", 5), ("banana", 3)]

    def test_tie_breaking_two_words(self) -> None:
        """Test tie-breaking with exactly two tied words."""
        freq = {"zulu": 10, "alpha": 10}
        result = get_top_k(freq, 2)
        assert result == [("alpha", 10), ("zulu", 10)]

    def test_tie_breaking_at_cutoff(self) -> None:
        """Test tie-breaking when k is at the boundary of a tie."""
        freq = {"apple": 5, "banana": 5, "cherry": 3}
        result = get_top_k(freq, 2)
        # Both have frequency 5, should return alphabetically first two
        assert result == [("apple", 5), ("banana", 5)]

    # ===== Edge Cases =====
    def test_k_greater_than_vocabulary(self) -> None:
        """Test when k > number of unique words."""
        freq = {"apple": 5, "banana": 3}
        result = get_top_k(freq, 10)
        # Should return all words, not pad with anything
        assert result == [("apple", 5), ("banana", 3)]

    def test_empty_frequency_map(self) -> None:
        """Test with empty frequency map."""
        result = get_top_k({}, 5)
        assert result == []

    def test_k_zero_raises_error(self) -> None:
        """Test that k=0 raises ValueError."""
        freq = {"apple": 5}
        with pytest.raises(ValueError, match="k must be positive"):
            get_top_k(freq, 0)

    def test_k_negative_raises_error(self) -> None:
        """Test that k<0 raises ValueError."""
        freq = {"apple": 5}
        with pytest.raises(ValueError, match="k must be positive"):
            get_top_k(freq, -1)

    def test_k_negative_large_raises_error(self) -> None:
        """Test that large negative k raises ValueError."""
        freq = {"apple": 5}
        with pytest.raises(ValueError, match="k must be positive"):
            get_top_k(freq, -100)

    # ===== Real-world Examples =====
    def test_realistic_frequency_distribution(self) -> None:
        """Test realistic frequency distribution (Zipfian)."""
        freq = {
            "the": 1000,
            "a": 500,
            "and": 450,
            "to": 400,
            "of": 350,
            "apple": 10,
            "banana": 8,
            "cherry": 5,
        }
        result = get_top_k(freq, 5)
        assert result == [
            ("the", 1000),
            ("a", 500),
            ("and", 450),
            ("to", 400),
            ("of", 350),
        ]

    def test_all_same_frequency(self) -> None:
        """Test when all words have the same frequency."""
        freq = {word: 5 for word in ["zebra", "apple", "banana", "cherry"]}
        result = get_top_k(freq, 2)
        # Should return first two alphabetically
        assert result == [("apple", 5), ("banana", 5)]

    def test_complex_tie_scenario(self) -> None:
        """Test complex tie scenario with multiple frequency levels."""
        freq = {
            "dog": 10,
            "cat": 10,
            "bird": 8,
            "apple": 8,
            "zebra": 5,
            "alpha": 5,
        }
        result = get_top_k(freq, 4)
        assert result == [
            ("cat", 10),      # Tied at 10, alphabetically first
            ("dog", 10),      # Tied at 10, alphabetically second
            ("apple", 8),     # Tied at 8, alphabetically first
            ("bird", 8),      # Tied at 8, alphabetically second
        ]

    def test_single_word_frequency_map(self) -> None:
        """Test with single word in frequency map."""
        freq = {"hello": 42}
        result = get_top_k(freq, 5)
        assert result == [("hello", 42)]


class TestIntegration:
    """Integration tests for count_frequency and get_top_k."""

    def test_full_pipeline(self) -> None:
        """Test full pipeline: count -> get_top_k."""
        words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
        freq = count_frequency(words)
        result = get_top_k(freq, 2)
        assert result == [("apple", 3), ("banana", 2)]

    def test_full_pipeline_with_ties(self) -> None:
        """Test full pipeline with tie-breaking."""
        words = ["apple", "apple", "zebra", "zebra", "banana"]
        freq = count_frequency(words)
        result = get_top_k(freq, 3)
        # apple and zebra tied at 2, banana at 1
        assert result == [("apple", 2), ("zebra", 2), ("banana", 1)]
