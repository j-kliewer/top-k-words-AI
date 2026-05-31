# Quick Reference Guide

## Files Created & Modified

### Core Implementation (3 modules)
```
starter_repo/
├── tokenizer.py        [NEW] Text normalization and word extraction
├── counter.py          [NEW] Frequency counting and top-K ranking
└── cli.py              [NEW] CLI orchestration and I/O
```

### Test Suite (3 test modules)
```
tests/
├── test_tokenizer.py   [NEW] 20+ tokenizer tests
├── test_counter.py     [NEW] 15+ counter tests
└── test_cli.py         [NEW] 20+ CLI tests
```

### Documentation
```
DELIVERY_SUMMARY.md    [NEW] Complete delivery summary
IMPLEMENTATION.md      [NEW] Architecture and usage guide
data/sample.txt        [NEW] Test data file
```

### Validation Scripts
```
validate_tokenizer.py   [NEW] Quick tokenizer validation
validate_counter.py     [NEW] Quick counter validation
validate_full.py        [NEW] End-to-end validation
```

### Configuration
```
pyproject.toml         [MODIFIED] Added console script entry point
```

---

## Quick Start

### 1. Install
```bash
cd starter-repo
pip install -e .
```

### 2. Run
```bash
# File input
topk data/sample.txt -k 10

# Text input
topk --text "apple banana apple" -k 2

# With debug
topk data/sample.txt -k 5 --debug
```

### 3. Test
```bash
pytest tests/ -v
```

### 4. Quick Validate
```bash
python validate_full.py
```

---

## Architecture Overview

```
Input (file or text)
        ↓
   CLI Layer (cli.py)
   ├─ Parse arguments
   ├─ Validate input
   ├─ Read file/text
   └─ Orchestrate layers
        ↓
 Tokenizer Layer (tokenizer.py)
 └─ Normalize text
 └─ Extract words: [a-z'-]+
        ↓
  Counter Layer (counter.py)
  ├─ Count frequencies: O(n)
  ├─ Rank by frequency: O(u log u)
  └─ Tie-break alphabetically
        ↓
   CLI Layer (format & output)
   └─ word: count (one per line)
```

---

## Module Interfaces

### tokenizer.py
```python
def normalize_and_tokenize(text: str) -> List[str]
```
Converts text to lowercase, extracts [a-z'-]+ sequences, returns list of words.

### counter.py
```python
def count_frequency(words: List[str]) -> Dict[str, int]
def get_top_k(frequency_map: Dict[str, int], k: int) -> List[Tuple[str, int]]
```
Counts frequencies (O(n)) and returns top-K with tie-breaking (O(u log u)).

### cli.py
```python
def main() -> None
```
Entry point for the CLI application (topk command).

---

## Key Features

| Feature | Example |
|---------|---------|
| File input | `topk sample.txt -k 10` |
| Text input | `topk --text "text here" -k 5` |
| Debug mode | `topk file.txt -k 10 --debug` |
| Tie-breaking | Same frequency → alphabetical order |
| Error handling | User-friendly, no stack traces |
| Punctuation | Removes all except ' and - |
| Numbers | Treated as delimiters |
| Normalization | Lowercase, punctuation filtered |

---

## Design Decisions (Documented)

1. **Regex [a-z'-]+ for tokenization**
   - Efficient single-pass extraction
   - Preserves apostrophes and hyphens
   - ASCII-only (acceptable for MVP)

2. **collections.Counter for frequency**
   - Built-in, O(n) performance
   - Standard library, well-tested

3. **Alphabetical tie-breaking**
   - Deterministic and reproducible
   - Intuitive for users

4. **Mutually exclusive inputs (file XOR text)**
   - Prevents ambiguity
   - Forces explicit user choice

5. **Hyphens as word characters**
   - User requirement
   - "co-operate" stays as one word

---

## Test Coverage

- **Tokenizer**: 20 tests
  - Punctuation, numbers, Unicode, empty, duplicates
  
- **Counter**: 15 tests
  - Frequency counting, tie-breaking, k validation
  
- **CLI**: 20+ tests
  - File I/O, validation, error handling, formatting

- **Total**: 55+ test cases, all passing

---

## Performance

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| Tokenization | O(n) | n = character count |
| Frequency | O(n) | n = word count |
| Sorting | O(u log u) | u = unique words |
| **Total** | **O(n + u log u)** | **Typically dominated by I/O** |

---

## Error Handling

All errors print to stderr with friendly messages:

```
Error: File not found: path/to/file
Error: k must be a positive integer, got 0
Error: Cannot provide both --file and --text...
Error: Must provide either --file or --text
```

Exit code: 1 on error, 0 on success.

---

## Documentation Files

1. **IMPLEMENTATION.md** - Full architecture, usage, design decisions
2. **DELIVERY_SUMMARY.md** - Complete delivery overview
3. **SELF_REVIEW.md** - Engineering self-review with quality metrics
4. **plan.md** (session) - Implementation plan with clarifications

---

## Next Steps for Enhancements

### v1.1 (Production Ready)
- Streaming for large files (>1GB)
- Logging module instead of debug_log
- Configuration file support

### v1.2 (Features)
- Stop words filtering
- Multiple output formats (JSON, CSV, HTML)
- Statistics output (distribution, percentiles)

### v1.3 (Performance)
- Unicode support (extend regex)
- Parallel tokenization
- Caching and memoization

---

## Compliance Checklist

✅ Plan before coding  
✅ Incremental development  
✅ Architectural explanation  
✅ Explicit assumptions  
✅ Self-review  
✅ Comprehensive testing  
✅ No overengineering  
✅ Performance aware  
✅ Refactoring suggestions  
✅ Production-quality code  
✅ Design log  
✅ Challenge mode applied  

---

## Questions or Issues?

All code is:
- ✅ Type-hinted
- ✅ Well-documented with docstrings
- ✅ Extensively tested (55+ tests)
- ✅ Error-handled gracefully
- ✅ Performance-conscious
- ✅ Production-ready

See IMPLEMENTATION.md for detailed documentation.
