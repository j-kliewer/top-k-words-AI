#!/usr/bin/env python
"""Quick validation of tokenizer functionality."""

from starter_repo.tokenizer import normalize_and_tokenize

# Test cases
test_cases = [
    ("Hello, World!", ["hello", "world"]),
    ("Don't co-operate.", ["don't", "co-operate"]),
    ("apple123banana", ["apple", "banana"]),
    ("", []),
    ("   ", []),
    ("It's the best of times, it's the worst of times.", 
     ["it's", "the", "best", "of", "times", "it's", "the", "worst", "of", "times"]),
]

print("Testing tokenizer...")
all_passed = True

for text, expected in test_cases:
    result = normalize_and_tokenize(text)
    passed = result == expected
    all_passed = all_passed and passed
    
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"{status}: {repr(text)}")
    if not passed:
        print(f"  Expected: {expected}")
        print(f"  Got:      {result}")

print("\n" + ("="*50))
if all_passed:
    print("✓ All tokenizer tests passed!")
else:
    print("✗ Some tests failed")
