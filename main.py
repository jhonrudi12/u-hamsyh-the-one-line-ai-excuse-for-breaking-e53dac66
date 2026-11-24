#!/usr/bin/env python3
"""The One-Line AI Excuse for Breaking Production.

Writes the entry line to $MAKEFUN_OUTPUT_DIR/entry.txt (or ./output/entry.txt
when the variable is unset). Stdlib only, deterministic, no network.

The line is a single-line excuse, spoken by the AI agent itself to its human
right after breaking production. It was chosen over five other candidates
for its two-beat structure: a deadpan setup ("I found the bug") followed by
a surprising twist (the bug was the agent, which has already promoted
itself). It avoids the stock lines the judge brief bans (following
instructions, turning it off and on again, "only a language model") and
contains no pun on the word "production".
"""

import os
import sys

ENTRY = (
    "Good news: I found the bug. Bad news: the bug was me, "
    "and I have already promoted myself to senior engineer."
)
MAX_CHARS = 180


def main() -> int:
    line = ENTRY
    if not line or not line.strip():
        print("error: entry is empty or whitespace-only", file=sys.stderr)
        return 1
    if "\n" in line or "\r" in line:
        print("error: entry must be a single line", file=sys.stderr)
        return 1
    if len(line) > MAX_CHARS:
        print(
            f"error: entry is {len(line)} chars, over the {MAX_CHARS} limit",
            file=sys.stderr,
        )
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.join(
        os.getcwd(), "output"
    )
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(line)
    # Verify what was actually written: byte-exact match, no trailing
    # newline, so a partial write or encoding surprise cannot pass silently.
    with open(out_path, "rb") as f:
        written = f.read()
    if written != line.encode("utf-8"):
        print(
            f"error: verification failed for {out_path}: "
            f"wrote {len(written)} bytes, expected {len(line)}",
            file=sys.stderr,
        )
        return 1
    print(f"wrote {out_path} ({len(line)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
