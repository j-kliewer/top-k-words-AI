"""
Text tokenization and normalization module.

This module provides functions to normalize text and extract words according to
specific rules (lowercase, extract alphabetic sequences with apostrophes and hyphens,
ignore numbers and punctuation).

Core responsibility: Convert raw text into a list of normalized words.
No CLI or formatting logic here.
"""

import re
from typing import List


def normalize_and_tokenize(text: str) -> List[str]:
    """
    Extract and normalize words from text.

    Rules:
    - Convert to lowercase
    - Extract sequences of alphabetic characters, apostrophes, and hyphens
    - Preserve apostrophes and hyphens only when internal to a word
      (leading or trailing quotes/hyphens around word tokens are removed)
    - Ignore numbers and other punctuation
    - Consecutive delimiters produce no empty tokens

    Args:
        text: Raw input text to tokenize

    Returns:
        List of normalized words (lowercase, no punctuation except ' and -)
        May contain duplicate words. Empty input returns empty list.

    Examples:
        >>> normalize_and_tokenize("Hello, World!")
        ['hello', 'world']
        >>> normalize_and_tokenize("Don't co-operate.")
        ["don't", "co-operate"]
        >>> normalize_and_tokenize("apple123banana")
        ['apple', 'banana']
        >>> normalize_and_tokenize("")
        []
        >>> normalize_and_tokenize("   ")
        []
    """
    if not text or not text.strip():
        return []

    # Convert to lowercase
    text = text.lower()

    # Extract sequences of Unicode letters with optional internal apostrophes or
    # hyphens. This preserves accented Latin letters such as é, ñ, and ï while
    # treating pure punctuation sequences like --- or ''' as delimiters.
    # Pattern explanation:
    # [^\W\d_]+ matches one or more Unicode letters
    # (?:['-][^\W\d_]+)* allows apostrophes or hyphens only when followed by letters
    return re.findall(r"[^\W\d_]+(?:['-][^\W\d_]+)*", text, flags=re.UNICODE)
