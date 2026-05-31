"""
Command-line interface for the top-K words application.

This module handles:
- Argument parsing and validation
- File reading with error handling
- Orchestration of tokenizer and counter
- Debug logging
- Output formatting

Responsibilities:
- All user-facing I/O and error handling
- Input validation (file existence, k values)
- Presentation layer (output formatting)

Core logic (tokenization, counting) is independent and testable separately.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from starter_repo.counter import count_frequency, get_top_k
from starter_repo.tokenizer import normalize_and_tokenize


def debug_log(message: str, debug: bool) -> None:
    """
    Print a debug message if debug mode is enabled.

    Args:
        message: Message to print
        debug: Whether debug mode is enabled
    """
    if debug:
        print(f"[DEBUG] {message}", file=sys.stderr)


def read_input(filepath: Optional[str], text: Optional[str]) -> str:
    """
    Read input from either a file or direct text.

    Validates that exactly one input source is provided (file XOR text).
    Handles file not found and read errors gracefully.

    Args:
        filepath: Path to file to read (if provided)
        text: Direct text input (if provided)

    Returns:
        Raw input text

    Raises:
        SystemExit: On validation errors (prints user-friendly message)
    """
    # Validate: exactly one input source
    if filepath and text:
        print(
            "Error: Cannot provide both --file and --text. Choose one input source.",
            file=sys.stderr,
        )
        sys.exit(1)

    if not filepath and not text:
        print(
            "Error: Must provide either --file <path> or --text <string>.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Read from file
    if filepath:
        try:
            path = Path(filepath)
            if not path.exists():
                print(f"Error: File not found: {filepath}", file=sys.stderr)
                sys.exit(1)
            if not path.is_file():
                print(f"Error: Not a file: {filepath}", file=sys.stderr)
                sys.exit(1)
            return path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            print(f"Error: Could not read file (encoding error): {filepath}", file=sys.stderr)
            sys.exit(1)
        except OSError as e:
            print(f"Error: Could not read file: {e}", file=sys.stderr)
            sys.exit(1)

    # Use direct text
    return text


def validate_k(k: int) -> None:
    """
    Validate that k is a positive integer.

    Args:
        k: The k value to validate

    Raises:
        SystemExit: If k is invalid
    """
    if k <= 0:
        print(f"Error: k must be a positive integer, got {k}", file=sys.stderr)
        sys.exit(1)


def format_output(results: list) -> str:
    """
    Format top-k results for display.

    Args:
        results: List of (word, count) tuples

    Returns:
        Formatted string with one word:count per line
    """
    if not results:
        return ""

    lines = [f"{word}: {count}" for word, count in results]
    return "\n".join(lines)


def main() -> None:
    """
    Main entry point for the application.

    Orchestrates:
    1. Argument parsing
    2. Input reading and validation
    3. Tokenization
    4. Frequency counting
    5. Top-K selection
    6. Output formatting
    """
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Find the K most frequent words in a text.",
        epilog="Example: topk sample.txt -k 10",
    )

    parser.add_argument(
        "file",
        nargs="?",
        default=None,
        help="Path to input file (mutually exclusive with --text)",
    )
    parser.add_argument(
        "--text",
        type=str,
        default=None,
        help="Direct text input (mutually exclusive with file)",
    )
    parser.add_argument(
        "-k",
        type=int,
        required=True,
        help="Number of top words to return (must be positive)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )

    args = parser.parse_args()

    # Validate k
    validate_k(args.k)

    # Read input
    raw_text = read_input(args.file, args.text)
    debug_log(f"Input source: {'file' if args.file else 'text'}", args.debug)

    # Handle empty input gracefully
    if not raw_text or not raw_text.strip():
        debug_log("Empty input detected", args.debug)
        # Output nothing (no words to display)
        return

    # Tokenize
    words = normalize_and_tokenize(raw_text)
    debug_log(f"Tokens extracted: {len(words)}", args.debug)

    # Count frequencies
    freq_map = count_frequency(words)
    debug_log(f"Unique words: {len(freq_map)}", args.debug)

    # Get top-k
    results = get_top_k(freq_map, args.k)
    debug_log(f"Top-{args.k} words computed", args.debug)

    # Format and output
    output = format_output(results)
    if output:
        print(output)


if __name__ == "__main__":
    main()
