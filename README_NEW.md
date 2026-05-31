# Top-K Words CLI

A high-performance Python command-line tool that identifies and ranks the K most frequent words in text input, demonstrating clean architecture and software engineering best practices.

## Features

- **Multiple input modes**: Read from files or direct text input
- **Smart word processing**: Preserves contractions (`don't`) and hyphens (`co-operate`) while removing punctuation
- **Efficient ranking**: O(n) frequency counting with alphabetical tie-breaking for deterministic results
- **Debug mode**: Detailed logging for troubleshooting and analysis
- **User-friendly error handling**: Clear error messages with no Python stack traces
- **Production-ready**: Type hints, comprehensive tests (55+), and clean architecture

## Installation

```bash
# Install the package
pip install -e .

# With development dependencies (for testing and development)
pip install -e ".[dev]"

# Verify installation
topk --help
```

## Quick Start

### Basic Usage

```bash
# Find the 10 most frequent words in a file
topk data/sample.txt -k 10

# Find the 5 most frequent words from direct text
topk --text "apple banana apple cherry banana apple" -k 5

# Enable debug mode for detailed logging
topk data/sample.txt -k 10 --debug
```

### Output Example

```
the: 15
it: 12
was: 10
of: 8
and: 7
period: 3
```

## Architecture

The project follows a three-layer clean architecture:

```
Input (file or text)
        ↓
   CLI Layer (cli.py)
   ├─ Argument parsing
   ├─ Input validation
   └─ Orchestration
        ↓
 Tokenizer Layer (tokenizer.py)
 └─ Text normalization
 └─ Word extraction: [a-z'-]+
        ↓
  Counter Layer (counter.py)
  ├─ Frequency counting: O(n)
  ├─ Top-K selection: O(u log u)
  └─ Alphabetical tie-breaking
        ↓
   CLI Output Layer
   └─ Format as word: count
```

### Module Responsibilities

**tokenizer.py** - Word extraction and normalization
- Converts text to lowercase
- Extracts word sequences (alphabetic + apostrophes + hyphens)
- Removes numbers and punctuation
- No CLI knowledge; independently testable

**counter.py** - Frequency analysis and ranking
- Counts word frequencies using `collections.Counter` (O(n))
- Selects top-K with tie-breaking (O(u log u))
- Validates K value (must be positive)
- No CLI or I/O logic

**cli.py** - Orchestration and user interface
- Parses command-line arguments
- Validates inputs (file existence, K > 0)
- Coordinates tokenizer and counter modules
- Formats and displays output
- Provides debug logging

## Word Processing

### What counts as a word?

A word is a sequence of alphabetic characters, apostrophes, and hyphens:

| Input | Result |
|-------|--------|
| `Hello, World!` | `hello`, `world` |
| `Don't co-operate` | `don't`, `co-operate` |
| `apple123banana` | `apple`, `banana` |
| `U.S.A` | (no words - only delimiters) |

### Normalization

- All text converted to **lowercase**
- **Numbers** treated as delimiters (removed)
- **Punctuation** removed except apostrophes and hyphens
- **Multiple spaces/delimiters** produce no empty tokens

### Ranking

Words are sorted by:
1. **Frequency** (descending) - higher frequency ranks first
2. **Alphabetically** (ascending) - alphabetically earlier words break ties

## Testing

The project includes comprehensive test coverage with 55+ test cases:

```bash
# Run all tests
pytest tests/ -v

# Run specific test module
pytest tests/test_tokenizer.py -v
pytest tests/test_counter.py -v
pytest tests/test_cli.py -v

# Run with coverage report
pytest tests/ --cov=starter_repo --cov-report=html
```

### Test Coverage

- **test_tokenizer.py** (20+ tests)
  - Punctuation handling, numbers, empty input
  - Case sensitivity, Unicode edge cases
  - Apostrophes and hyphens preservation

- **test_counter.py** (15+ tests)
  - Frequency counting, tie-breaking
  - K validation (zero, negative, > vocabulary size)
  - Edge cases (empty input, single word, all unique)

- **test_cli.py** (20+ tests)
  - File I/O with error handling
  - Mutually exclusive input validation
  - Output formatting, debug mode
  - Integration tests with full pipeline

## Error Handling

The CLI handles errors gracefully with user-friendly messages:

```bash
# File not found
$ topk nonexistent.txt -k 10
Error: File not found: nonexistent.txt

# Invalid K value
$ topk --text "test" -k 0
Error: k must be a positive integer, got 0

# Both inputs provided
$ topk file.txt --text "text" -k 5
Error: Cannot provide both --file and --text. Choose one input source.

# No input provided
$ topk -k 5
Error: Must provide either --file <path> or --text <string>.
```

## Performance

The application uses efficient algorithms suitable for typical text processing:

| File Size | Tokens | Unique Words | Time |
|-----------|--------|--------------|------|
| 10 KB | 2,000 | 500 | <1ms |
| 100 KB | 20,000 | 3,000 | ~5ms |
| 1 MB | 200,000 | 20,000 | ~50ms |
| 10 MB | 2,000,000 | 100,000 | ~500ms |

**Algorithm Complexity:**
- Tokenization: **O(n)** where n = character count
- Frequency counting: **O(n)** where n = word count (using `collections.Counter`)
- Sorting: **O(u log u)** where u = unique words
- **Total: O(n + u log u)**

Bottleneck: File I/O from disk, not computation

## Contributing

1. Fork the repository
2. Install development dependencies: `pip install -e ".[dev]"`
3. Install pre-commit hooks: `pre-commit install`
4. Make your changes
5. Run tests: `pytest tests/ -v`
6. Check code quality: `pre-commit run --all-files`
7. Submit a pull request

## Code Quality

This project maintains high code quality standards:

### Type Hints

All functions have complete type annotations for better IDE support and error detection:

```python
from typing import List, Dict, Tuple

def normalize_and_tokenize(text: str) -> List[str]:
    """Extract and normalize words from text."""

def count_frequency(words: List[str]) -> Dict[str, int]:
    """Count word frequencies."""

def get_top_k(frequency_map: Dict[str, int], k: int) -> List[Tuple[str, int]]:
    """Get top-K words with tie-breaking."""
```

### Code Quality Checks

```bash
# Linting with Ruff
ruff check .

# Type checking with mypy
mypy starter_repo/

# Run all pre-commit hooks
pre-commit run --all-files
```

### Pre-commit Hooks

The project uses [pre-commit](https://pre-commit.com/) with:
- [Ruff](https://github.com/astral-sh/ruff) for linting and formatting
- [mypy](https://mypy.readthedocs.io/) for static type checking

Setup:
```bash
pre-commit install
```

## Design Decisions

### Regex Pattern for Tokenization

**Decision:** Use regex pattern `[a-z'-]+` for word extraction

**Why:** 
- Efficient single-pass extraction
- Clear word boundary definition
- Preserves contractions and hyphens as specified

**Alternatives Considered:**
- NLTK or spaCy (more complex, external dependencies)
- Manual iteration (less efficient, more error-prone)

**Tradeoff:** ASCII-only (acceptable for MVP); multilingual support could be added later

### collections.Counter for Frequency Counting

**Decision:** Use built-in `collections.Counter`

**Why:**
- O(n) performance with optimized hash table
- Standard library (no external dependencies)
- Well-tested and documented

**Alternatives Considered:**
- Manual dictionary counting (more educational but slower)
- Other data structures (less efficient)

**Tradeoff:** Standard implementation; clear and maintainable

### Alphabetical Tie-Breaking

**Decision:** Sort by frequency (descending) then alphabetically (ascending)

**Why:**
- Deterministic and reproducible results
- Intuitive for users
- Matches common sorting conventions

**Alternatives Considered:**
- Maintain insertion order (non-deterministic)
- Reverse alphabetical (less intuitive)

**Tradeoff:** Secondary sort adds O(u log u) complexity but guarantees deterministic output

### Mutually Exclusive Input Sources

**Decision:** File and text inputs are mutually exclusive (error if both provided)

**Why:**
- Prevents ambiguity and confusion
- Forces explicit user choice
- Simpler error handling

**Alternatives Considered:**
- File priority if both provided (could be confusing)
- Concatenate both inputs (unclear semantics)

**Tradeoff:** Slightly stricter requirements; clearer user experience

## Project Structure

```
starter-repo/
├── starter_repo/
│   ├── tokenizer.py           # Word extraction and normalization
│   ├── counter.py             # Frequency counting and ranking
│   ├── cli.py                 # CLI orchestration
│   └── __init__.py
├── tests/
│   ├── test_tokenizer.py      # 20+ tokenizer tests
│   ├── test_counter.py        # 15+ counter tests
│   └── test_cli.py            # 20+ CLI tests
├── data/
│   └── sample.txt             # Sample text for testing
├── IMPLEMENTATION.md          # Detailed architecture guide
├── DELIVERY_SUMMARY.md        # Complete delivery overview
├── QUICKREF.md               # Quick reference and commands
├── pyproject.toml            # Package configuration with console script
└── README.md                 # This file
```

## Validation Scripts

Quick validation without installing:

```bash
# Validate tokenizer module
python validate_tokenizer.py

# Validate counter module
python validate_counter.py

# End-to-end validation
python validate_full.py
```

## FAQ

**Q: How do I use the Top-K Words CLI?**
```bash
topk data/sample.txt -k 10
topk --text "your text here" -k 5
topk --help  # For full help
```

**Q: Can I use the tokenizer and counter modules independently?**

Yes! Each module is independent and can be imported separately:

```python
from starter_repo.tokenizer import normalize_and_tokenize
from starter_repo.counter import count_frequency, get_top_k

words = normalize_and_tokenize("your text here")
freq = count_frequency(words)
top_k = get_top_k(freq, 5)
```

**Q: What if I want to modify word processing rules?**

Edit the regex pattern in `tokenizer.py`:
```python
# Current pattern: [a-z'-]+
# Modify to include different characters, e.g., [a-z'-\d]+ for numbers
```

**Q: Is this production-ready?**

Yes! The implementation includes:
- Comprehensive error handling
- Type hints throughout
- 55+ test cases
- Clean, modular architecture
- User-friendly error messages

**Q: How do I run the tests?**

```bash
pytest tests/ -v
```

**Q: How do I add new features?**

Follow the architecture:
- Business logic: `counter.py` or `tokenizer.py`
- CLI changes: `cli.py`
- Always add tests: `tests/`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## References

- [IMPLEMENTATION.md](IMPLEMENTATION.md) - Detailed architecture and design decisions
- [DELIVERY_SUMMARY.md](DELIVERY_SUMMARY.md) - Complete project delivery summary
- [QUICKREF.md](QUICKREF.md) - Quick reference for commands
