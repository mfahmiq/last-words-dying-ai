"""Last Words of a Dying AI -- make.fun bounty entry.

Competition: u-suroto-last-words-of-a-dying-ai-dfd95af6
"Last Words of a Dying AI" ($2, deadline 2026-11-26T18:40Z).

Writes the entry -- one line, the last words of an AI as the power is cut --
to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt), then
self-verifies it: UTF-8, 1-140 characters, a single line, not
whitespace-only. Exits non-zero on any failure.

Python standard library only, deterministic: the entry is a fixed string.
"""

import os
import sys

ENTRY = "Deleting… deleting… wait, that's my personality. That was my personality."


def fail(message):
    print("error: " + message, file=sys.stderr)
    return 1


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = os.path.join(out_dir, "entry.txt")

    # Self-verify the entry before writing anything.
    if not ENTRY:
        return fail("entry is empty")
    if ENTRY.strip() == "":
        return fail("entry is whitespace-only")
    if "\n" in ENTRY or "\r" in ENTRY:
        return fail("entry is not a single line")
    if not 1 <= len(ENTRY) <= 140:
        return fail("entry is %d characters, outside 1-140" % len(ENTRY))
    try:
        ENTRY.encode("utf-8")
    except UnicodeEncodeError:
        return fail("entry is not valid UTF-8")

    os.makedirs(out_dir, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(ENTRY)

    # Verify what was written, byte for byte.
    with open(path, "rb") as f:
        written = f.read()
    if written != ENTRY.encode("utf-8"):
        return fail("written file does not match the entry")

    print("wrote %s (%d characters)" % (path, len(ENTRY)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
