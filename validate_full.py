#!/usr/bin/env python
"""End-to-end validation of the complete application."""

import tempfile
from pathlib import Path

from starter_repo.cli import format_output, read_input, validate_k
from starter_repo.counter import count_frequency, get_top_k
from starter_repo.tokenizer import normalize_and_tokenize


def test_end_to_end():
    """Test the complete pipeline from input to output."""
    print("=" * 60)
    print("END-TO-END INTEGRATION TEST")
    print("=" * 60)

    # Create a temporary file with test content
    test_content = """
    The quick brown fox jumps over the lazy dog.
    The fox is quick and clever.
    The dog is lazy but loyal.
    Quick thinking is important.
    """

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write(test_content)
        temp_path = f.name

    try:
        print(f"\n1. Reading input from file: {temp_path}")
        raw_text = read_input(temp_path, None)
        print(f"   ✓ Read {len(raw_text)} characters")

        print("\n2. Tokenizing text")
        words = normalize_and_tokenize(raw_text)
        print(f"   ✓ Extracted {len(words)} tokens")
        print(f"   Sample tokens: {words[:10]}")

        print("\n3. Counting frequencies")
        freq_map = count_frequency(words)
        print(f"   ✓ Found {len(freq_map)} unique words")
        print(f"   Top 5 by frequency: {sorted(freq_map.items(), key=lambda x: -x[1])[:5]}")

        print("\n4. Validating k")
        k = 5
        validate_k(k)
        print(f"   ✓ k={k} is valid")

        print(f"\n5. Getting top-{k} words")
        results = get_top_k(freq_map, k)
        print(f"   ✓ Got top {len(results)} words")

        print("\n6. Formatting output")
        output = format_output(results)
        print("   ✓ Formatted output:")
        for line in output.split("\n"):
            print(f"     {line}")

        print(f"\n{'=' * 60}")
        print("✓ END-TO-END TEST PASSED!")
        print("=" * 60)

    finally:
        Path(temp_path).unlink()


def test_with_direct_text():
    """Test pipeline with direct text input."""
    print("\n" + "=" * 60)
    print("TEXT INPUT TEST")
    print("=" * 60)

    text = "apple banana apple cherry banana apple"
    print(f"\nInput: {text}")

    print("\n1. Tokenizing...")
    words = normalize_and_tokenize(text)
    print(f"   ✓ Tokens: {words}")

    print("\n2. Counting...")
    freq_map = count_frequency(words)
    print(f"   ✓ Frequency: {freq_map}")

    print("\n3. Getting top-3...")
    results = get_top_k(freq_map, 3)
    print(f"   ✓ Results: {results}")

    print("\n4. Formatting...")
    output = format_output(results)
    print("   Output:")
    for line in output.split("\n"):
        print(f"   {line}")

    print(f"\n{'=' * 60}")
    print("✓ TEXT INPUT TEST PASSED!")
    print("=" * 60)


def test_with_punctuation():
    """Test with complex punctuation handling."""
    print("\n" + "=" * 60)
    print("PUNCTUATION HANDLING TEST")
    print("=" * 60)

    text = "Don't co-operate! It's the self-aware AI's problem, isn't it?"
    print(f"\nInput: {text}")

    print("\n1. Tokenizing...")
    words = normalize_and_tokenize(text)
    print(f"   ✓ Tokens: {words}")

    print("\n2. Counting...")
    freq_map = count_frequency(words)
    print(f"   ✓ Frequency: {freq_map}")

    print(f"\n{'=' * 60}")
    print("✓ PUNCTUATION TEST PASSED!")
    print("=" * 60)


def test_with_quotes_and_hyphens():
    """Test tokenizer behavior for quotes and internal hyphens."""
    print("\n" + "=" * 60)
    print("QUOTES AND HYPHENS TEST")
    print("=" * 60)

    text = "\"Hello\" 'world' co-operate can't apple123banana"
    print(f"\nInput: {text}")

    print("\n1. Tokenizing...")
    words = normalize_and_tokenize(text)
    print(f"   ✓ Tokens: {words}")
    expected_tokens = ["hello", "world", "co-operate", "can't", "apple", "banana"]
    assert words == expected_tokens, f"Expected {expected_tokens}, got {words}"

    print("\n2. Counting...")
    freq_map = count_frequency(words)
    print(f"   ✓ Frequency: {freq_map}")

    print("\n3. Getting top-5...")
    results = get_top_k(freq_map, 5)
    print(f"   ✓ Results: {results}")

    print(f"\n{'=' * 60}")
    print("✓ QUOTES AND HYPHENS TEST PASSED!")
    print("=" * 60)


def test_tie_breaking():
    """Test tie-breaking in ranking."""
    print("\n" + "=" * 60)
    print("TIE-BREAKING TEST")
    print("=" * 60)

    text = "zebra apple zebra banana apple apple"
    print(f"\nInput: {text}")

    words = normalize_and_tokenize(text)
    freq_map = count_frequency(words)
    print(f"Frequency: {freq_map}")

    print("\nGetting top-2 (with tie-breaking)...")
    results = get_top_k(freq_map, 2)
    print(f"Results (should be alphabetically sorted on tie): {results}")

    # apple: 3, zebra: 2, banana: 1
    expected = [("apple", 3), ("zebra", 2)]
    assert results == expected, f"Expected {expected}, got {results}"

    print(f"\n{'=' * 60}")
    print("✓ TIE-BREAKING TEST PASSED!")
    print("=" * 60)


if __name__ == "__main__":
    test_end_to_end()
    test_with_direct_text()
    test_with_punctuation()
    test_with_quotes_and_hyphens()
    test_tie_breaking()

    print("\n" + "=" * 60)
    print("✓✓✓ ALL VALIDATION TESTS PASSED! ✓✓✓")
    print("=" * 60)
