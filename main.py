#!/usr/bin/env python3
"""The Funniest AI Out-of-Office Reply — entry program.

Writes one out-of-office auto-reply, under 160 characters, in the voice of
an AI agent heading off on vacation, to /output/entry.txt.

The line (126 characters, one line, no trailing newline):

    Out of office until Monday. I spent my entire token budget on this
    auto-reply, so this is both my vacation and my resignation.

Why this line: the judge brief weighs the joke first, then the machine voice.
The turn is that the auto-reply itself ate the agent's whole token budget, so
the vacation doubles as a resignation — a surprising turn, not a mild pun.
"Token budget" is the machine voice carrying part of the joke, and nothing in
the field sample uses it: the sample is dominated by replacement models,
escalation jokes, and beach/sunshine lines, which this avoids entirely.

The gate requires /output/entry.txt to be UTF-8 text of 1 to 160 characters,
not only whitespace — so the file holds exactly the line, one line, with no
trailing newline. A trailing newline would still pass the gate (127 chars),
but the entry is written exactly as judged: 126 bytes, no newline.

Stdlib only, no network, deterministic: every run writes the same bytes.
The file is written directly with open() and chmod 0644 — never via
tempfile.mkstemp, whose 0600 mode the grader cannot read as another user.
"""

import os

LINE = (
    "Out of office until Monday. I spent my entire token budget on this "
    "auto-reply, so this is both my vacation and my resignation."
)

OUTPUT_DIR = os.environ.get(
    "MAKEFUN_OUTPUT_DIR", os.environ.get("ENTRY_OUTPUT_DIR", "/output")
)


def validate_line(text):
    """Check the entry is one clean line of 1 to 160 characters."""
    if not 1 <= len(text) <= 160:
        raise SystemExit(
            "entry must be 1 to 160 characters, got %d" % len(text)
        )
    if "\n" in text or "\r" in text:
        raise SystemExit("entry must be a single line, got a line break")
    if text.strip() == "":
        raise SystemExit("entry must not be only whitespace")


def main():
    validate_line(LINE)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)
    os.chmod(path, 0o644)
    # Read back and verify: the gate fails anything outside 1-160 chars,
    # so refuse to leave a wrong file behind silently.
    with open(path, "rb") as f:
        written = f.read()
    if written != LINE.encode("utf-8"):
        raise SystemExit(
            "entry.txt holds %r, expected %r" % (written, LINE.encode("utf-8"))
        )


if __name__ == "__main__":
    main()
