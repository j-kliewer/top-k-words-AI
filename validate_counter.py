#!/usr/bin/env python
"""Quick validation of counter functionality."""

from starter_repo.counter import count_frequency, get_top_k

print("Testing counter module...\n")

# Test count_frequency
print("=== count_frequency ===")
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
freq = count_frequency(words)
print(f"Words: {words}")
print(f"Frequency: {freq}")
expected_freq = {"apple": 3, "banana": 2, "cherry": 1}
assert freq == expected_freq, f"Expected {expected_freq}, got {freq}"
print("✓ count_frequency works\n")

# Test get_top_k
print("=== get_top_k ===")
result = get_top_k(freq, 2)
print(f"Top 2 words: {result}")
expected_result = [("apple", 3), ("banana", 2)]
assert result == expected_result, f"Expected {expected_result}, got {result}"
print("✓ get_top_k works\n")

# Test tie-breaking
print("=== Tie-breaking ===")
freq_ties = {"zebra": 5, "apple": 5, "banana": 3}
result_ties = get_top_k(freq_ties, 3)
print(f"Frequency: {freq_ties}")
print(f"Top 3 (with alphabetical tie-break): {result_ties}")
expected_ties = [("apple", 5), ("zebra", 5), ("banana", 3)]
assert result_ties == expected_ties, f"Expected {expected_ties}, got {result_ties}"
print("✓ Tie-breaking works correctly\n")

# Test error handling
print("=== Error handling ===")
try:
    get_top_k(freq, 0)
    print("✗ FAIL: Should have raised ValueError for k=0")
except ValueError as e:
    print(f"✓ Correctly raised ValueError for k=0: {e}\n")

# Test empty frequency map
print("=== Empty frequency map ===")
result_empty = get_top_k({}, 5)
print(f"Result for empty frequency map: {result_empty}")
assert result_empty == [], f"Expected [], got {result_empty}"
print("✓ Empty frequency map works\n")

# Test k larger than vocabulary
print("=== k larger than vocabulary ===")
result_large_k = get_top_k(freq, 10)
print(f"Result for k=10: {result_large_k}")
expected_large_k = [("apple", 3), ("banana", 2), ("cherry", 1)]
assert result_large_k == expected_large_k, f"Expected {expected_large_k}, got {result_large_k}"
print("✓ k larger than vocabulary returns all words\n")

print("="*50)
print("✓ All counter module tests passed!")
