"""
Word frequency counting and top-K selection module.

This module provides functions to count word frequencies and select the K most
frequent words with tie-breaking rules.

Core responsibility: Business logic for frequency analysis and ranking.
No CLI or I/O logic here.
"""

from collections import Counter
from typing import Dict, List, Tuple


def count_frequency(words: List[str]) -> Dict[str, int]:
    """
    Count the frequency of each word.

    Time Complexity: O(n) where n = number of words
    Space Complexity: O(u) where u = number of unique words

    Args:
        words: List of words (may contain duplicates)

    Returns:
        Dictionary mapping word -> count
        Returns empty dict if input is empty

    Example:
        >>> count_frequency(['apple', 'banana', 'apple'])
        {'apple': 2, 'banana': 1}
    """
    return dict(Counter(words))


def get_top_k(
    frequency_map: Dict[str, int], k: int
) -> List[Tuple[str, int]]:
    """
    Get the top-K most frequent words with tie-breaking by alphabetical order.

    Ranking criteria (in order):
    1. Frequency (descending): Higher frequency ranks first
    2. Alphabetical order (ascending): Alphabetically earlier words break ties

    Time Complexity: O(u log u) where u = number of unique words
    Space Complexity: O(k) for output

    Args:
        frequency_map: Dict mapping word -> count (e.g., from count_frequency)
        k: Number of top words to return (must be > 0)

    Returns:
        List of (word, count) tuples sorted by frequency (desc) then
        alphabetically (asc). If k >= len(frequency_map), returns all words.

    Raises:
        ValueError: If k <= 0

    Examples:
        >>> freq = {'apple': 5, 'banana': 5, 'cherry': 3}
        >>> get_top_k(freq, 2)
        [('apple', 5), ('banana', 5)]  # tie-break alphabetically
        
        >>> get_top_k({'word': 1}, 10)
        [('word', 1)]  # k > vocabulary size
        
        >>> get_top_k({}, 5)
        []  # empty frequency map
    """
    if k <= 0:
        raise ValueError(f"k must be positive, got {k}")

    if not frequency_map:
        return []

    # Sort by frequency (descending), then alphabetically (ascending)
    # sorted() is stable, so we sort by secondary key first, then primary key
    sorted_words = sorted(
        frequency_map.items(),
        key=lambda item: (-item[1], item[0]),  # (-count, word)
    )

    # Return top k (or all if k > len)
    return sorted_words[:k]
