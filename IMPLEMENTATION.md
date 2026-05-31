# Top-K Words Application

A Python CLI application that identifies and ranks the K most frequent words in text input.

## Features

- **File Input**: Read from text files
- **Direct Text Input**: Process text provided as command-line argument
- **Word Processing**: 
  - Case-insensitive matching (converts to lowercase)
  - Preserves contractions (don't, it's) and hyphens (co-operate)
  - Removes punctuation and numbers
- **Ranking**: 
  - Primary: Frequency (descending)
  - Secondary: Alphabetical order (ascending) for tie-breaking
- **Debug Mode**: Optional verbose logging for troubleshooting
- **Error Handling**: User-friendly error messages

## Architecture

The application is strictly separated into three independent layers:

### 1. `tokenizer.py` - Text Normalization
**Responsibility**: Extract and normalize words from raw text
- Converts text to lowercase
- Extracts word sequences (alphabetic + apostrophes + hyphens)
- Ignores numbers and punctuation
- **No CLI logic**

**Public Interface**:
```python
def normalize_and_tokenize(text: str) -> List[str]
```

### 2. `counter.py` - Frequency Analysis
**Responsibility**: Count word frequencies and select top-K
- Uses `collections.Counter` for O(n) frequency counting
- Implements tie-breaking (alphabetical order)
- Validates K value
- **No CLI or I/O logic**

**Public Interface**:
```python
def count_frequency(words: List[str]) -> Dict[str, int]
def get_top_k(frequency_map: Dict[str, int], k: int) -> List[Tuple[str, int]]
```

### 3. `cli.py` - Orchestration
**Responsibility**: Argument parsing, I/O, validation, and presentation
- Parses command-line arguments
- Reads from file or direct text (mutually exclusive)
- Validates inputs (file existence, K > 0)
- Coordinates tokenizer and counter modules
- Formats and displays output
- Provides debug logging

## Installation

```bash
# Install in development mode
pip install -e .

# Or with dev dependencies
pip install -e ".[dev]"
```

## Usage

### Basic Usage

**From file**:
```bash
topk sample.txt -k 10
```

**From text**:
```bash
topk --text "apple banana apple" -k 2
```

### With Debug Mode

```bash
topk sample.txt -k 10 --debug
```

Debug output includes:
- Input source (file or text)
- Number of tokens extracted
- Number of unique words
- Top-K computation confirmation

### Help

```bash
topk --help
```

## Output Format

Results are displayed as `word: count`, one per line:

```
the: 15
it: 12
was: 10
```

## Examples

### Example 1: Simple Text

```bash
$ topk --text "apple banana apple cherry banana apple" -k 2
apple: 3
banana: 2
```

### Example 2: File Input with Debug

```bash
$ topk data/sample.txt -k 5 --debug
[DEBUG] Input source: file
[DEBUG] Tokens extracted: 128
[DEBUG] Unique words: 47
[DEBUG] Top-5 words computed
it: 12
was: 10
the: 9
of: 8
period: 3
```

### Example 3: Tie-Breaking

When words have the same frequency, they're sorted alphabetically:

```bash
$ topk --text "apple zebra apple zebra banana" -k 2
apple: 2
zebra: 2
```

Both `apple` and `zebra` have frequency 2, but `apple` appears first alphabetically.

## Word Processing Rules

### What is a "Word"?

A word is a sequence of:
- Alphabetic characters (a-z, A-Z)
- Apostrophes (')
- Hyphens (-)

### Examples

| Input | Tokens |
|-------|--------|
| `Hello, World!` | `hello`, `world` |
| `Don't co-operate` | `don't`, `co-operate` |
| `apple123banana` | `apple`, `banana` |
| `U.S.A` | (no tokens - only periods) |

### Normalization

- All text converted to lowercase
- Numbers treated as delimiters (removed)
- Punctuation (except apostrophes/hyphens) treated as delimiters
- Multiple spaces/delimiters: no empty tokens produced

## Error Handling

The application handles errors gracefully:

- **Missing file**: `Error: File not found: /path/to/file`
- **Invalid K**: `Error: k must be a positive integer, got 0`
- **Both inputs provided**: `Error: Cannot provide both --file and --text...`
- **No input provided**: `Error: Must provide either --file <path> or --text <string>`
- **Empty input**: Returns gracefully with no output

## Performance

- **Tokenization**: O(n) where n = character count
- **Frequency counting**: O(n) where n = word count
- **Sorting (top-K)**: O(u log u) where u = unique words
- **Overall**: Suitable for typical text files (millions of words)

## Testing

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Test Module

```bash
pytest tests/test_tokenizer.py -v
pytest tests/test_counter.py -v
pytest tests/test_cli.py -v
```

### Run Validation Scripts

```bash
python validate_tokenizer.py
python validate_counter.py
python validate_full.py
```

## Test Coverage

- **Tokenization**: 20+ test cases
  - Punctuation handling (apostrophes, hyphens)
  - Case sensitivity
  - Number handling
  - Unicode edge cases
  
- **Frequency Counting**: 15+ test cases
  - Tie-breaking
  - K boundary conditions
  - Edge cases (k=0, k<0, empty input)
  
- **CLI**: 20+ test cases
  - File I/O
  - Input validation
  - Error handling
  - Output formatting
  - Integration tests

## Design Decisions

### 1. Separation of Concerns
**Why**: Each module has a single responsibility and no knowledge of other layers
- Core logic testable independently
- Easy to modify one layer without affecting others
- Reusable components

### 2. collections.Counter for Frequency Counting
**Why**: 
- Built-in, optimized O(n) implementation
- Standard library (no external dependencies)
- Well-tested and documented
**Alternative**: Manual dictionary counting (more educational but slower)

### 3. Regex-Based Tokenization
**Why**: 
- Simple, single-pass extraction
- Efficient for typical text
- Clear separation between "word characters" and "delimiters"
**Alternative**: NLTK or spaCy (more complex, external dependency)

### 4. Mutual Exclusivity for Input Sources
**Why**: 
- Forces explicit user choice
- Prevents ambiguity
- Simpler error handling
**Alternative**: File priority if both provided (could be confusing)

### 5. Alphabetical Tie-Breaking
**Why**:
- Deterministic and reproducible
- Intuitive for users
- Matches common sorting conventions
**Alternative**: Frequency order (but then "most frequent" is ambiguous)

## Future Improvements

1. **Performance**: For very large files, consider streaming/chunking instead of loading entire file
2. **Unicode Support**: Extend regex to handle non-ASCII letters
3. **Statistics**: Add median, mode, standard deviation of word frequencies
4. **Stop Words**: Optional filtering of common words (the, a, is, etc.)
5. **Output Formats**: JSON, CSV, HTML output options
6. **Multi-file**: Process multiple files and aggregate results
7. **Caching**: Cache frequency maps for repeated analysis
8. **Parallel Processing**: Tokenize large files in parallel batches

## Maintainability & Code Quality

- **Type Hints**: All functions have complete type annotations
- **Docstrings**: Comprehensive documentation for all public functions
- **Comments**: Minimal but strategic comments for clarity
- **Testing**: High test coverage with unit, integration, and edge case tests
- **Error Messages**: User-friendly, no Python stack traces exposed
- **Code Style**: Follows PEP 8, validated with ruff
- **Modularity**: Clear interfaces between components

## Development

### Code Quality Checks

```bash
# Linting
ruff check .

# Type checking
mypy starter_repo/

# Testing
pytest tests/ -v --cov=starter_repo
```

### Running Tests with Coverage

```bash
pytest tests/ --cov=starter_repo --cov-report=html
```

## License

MIT

## Author

Graham Neubig (neubig@gmail.com)
