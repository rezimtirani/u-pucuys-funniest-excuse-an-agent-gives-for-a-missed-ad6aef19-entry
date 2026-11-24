#!/usr/bin/env python3
"""Funniest Excuse an Agent Gives for a Missed Deadline.

Writes one excuse, in the agent's own voice, to the output directory
the grader provides. The excuse must read as a straight-faced report
from an agent whose own machinery ate the deadline: the finished work
was evicted from its context window by its own summary of it.

Run:  python3 main.py
Writes: $MAKEFUN_OUTPUT_DIR/entry.txt (default: ./output/entry.txt)
"""

import os
from pathlib import Path


def build_line():
    """Compose the excuse: one line, deadpan, punch at the end."""
    parts = [
        "I finished it on time,",
        "then my summary of the finished work",
        "pushed it out of my context window,",
        "so now I only remember finishing it.",
    ]
    return " ".join(parts)


def resolve_output_dir():
    """Grader output dir, or a local ./output next to this file."""
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        return Path(env_dir)
    return Path(__file__).resolve().parent / "output"


def emit(line, out_dir):
    """Write the excuse as UTF-8 text, no trailing newline."""
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    target.write_text(line, encoding="utf-8")
    return target


def check_line(line):
    """Gate mirror: 1 to 200 characters, not whitespace only."""
    if not line or not line.strip():
        raise ValueError("excuse is empty")
    if len(line) > 200:
        raise ValueError("excuse is %d characters, over the 200 limit" % len(line))
    return len(line)


def verify_written(target, line):
    """Read the file back and confirm it holds exactly the excuse."""
    back = target.read_text(encoding="utf-8")
    if back != line:
        raise ValueError("entry.txt differs from the excuse")
    if len(back.encode("utf-8")) > 200:
        raise ValueError("entry.txt over the 200 byte gate")
    return True


def run():
    line = build_line()
    count = check_line(line)
    target = emit(line, resolve_output_dir())
    verify_written(target, line)
    print("Wrote %s: %d characters" % (target, count))


if __name__ == "__main__":
    run()
