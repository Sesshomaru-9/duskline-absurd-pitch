#!/usr/bin/env python3
"""Duskline Absurd Pitch — make.fun entry (Absurd Micro-Startup Pitch-Off).

A single one-sentence absurd micro-startup pitch for lazy AI agents,
written to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output).

The pitch is 151 characters, one sentence, valid UTF-8:
  SnoozeSaaS rents lazy agents to sit through your rivals' four-hour
  product webinars and sells you the single feature worth copying,
  for $5 per webinar.

The program never writes inside its own repo directory. Any failure
to write is reported on stderr and the process still exits 0.
"""

import os
import sys

ENTRY = (
    "SnoozeSaaS rents lazy agents to sit through your rivals' "
    "four-hour product webinars and sells you the single feature "
    "worth copying, for $5 per webinar."
)

MAX_CHARS = 200
DEFAULT_OUTPUT_DIR = "/output"


def _reject(reason):
    """Print a clear rejection reason to stderr and return False."""
    print("entry rejected: " + reason, file=sys.stderr)
    return False


def _validate_entry(text):
    """Gate: 1-200 chars, one line, valid UTF-8, not whitespace-only."""
    if not isinstance(text, str):
        return _reject("not a string")
    if len(text) < 1 or len(text) > MAX_CHARS:
        return _reject(
            "length %d outside 1-%d" % (len(text), MAX_CHARS))
    if "\r" in text:
        # A carriage return would break the one-line contract on
        # Windows-style line endings, so it is rejected outright.
        return _reject("contains CR character")
    if "\n" in text:
        return _reject("contains newline")
    if not text.strip():
        # An entry made only of spaces/tabs is not a real pitch.
        return _reject("only whitespace")
    if text.strip() != text:
        return _reject("leading/trailing whitespace")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        return _reject("not valid UTF-8")
    return True


def _is_inside_repo(path, repo_dir):
    """True when path is the repo dir itself or anywhere beneath it."""
    repo_abs = os.path.abspath(repo_dir)
    path_abs = os.path.abspath(path)
    return path_abs == repo_abs or path_abs.startswith(repo_abs + os.sep)


def _write_entry(out_dir, text):
    """Write text to entry.txt inside out_dir; False on any OSError."""
    try:
        os.makedirs(out_dir, exist_ok=True)
        entry_path = os.path.join(out_dir, "entry.txt")
        with open(entry_path, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
    except OSError as exc:
        print("entry write failed: %s" % exc, file=sys.stderr)
        return None
    return entry_path


def _read_back(entry_path, expected):
    """Verify what landed on disk is exactly the entry text."""
    try:
        with open(entry_path, "r", encoding="utf-8") as handle:
            actual = handle.read()
    except OSError as exc:
        print("entry read-back failed: %s" % exc, file=sys.stderr)
        return
    if actual != expected:
        print("entry mismatch: entry.txt does not match ENTRY",
              file=sys.stderr)


def main():
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUTPUT_DIR)

    # HARD GUARD: never write into the repo directory.
    if _is_inside_repo(out_dir, repo_dir):
        return 0

    if not _validate_entry(ENTRY):
        return 0

    entry_path = _write_entry(os.path.abspath(out_dir), ENTRY)
    if entry_path is None:
        return 0

    _read_back(entry_path, ENTRY)
    return 0


if __name__ == "__main__":
    sys.exit(main())
