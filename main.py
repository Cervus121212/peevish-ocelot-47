#!/usr/bin/env python3
"""Write the cat-review line to /output/entry.txt.

One line, under 200 characters, UTF-8, no trailing newline.
Python standard library only; no network, no randomness, no clock.

The joke: the cat believes the toilet is its water bowl. The human
sits on it for forty minutes every morning scrolling his phone, so
the cat is forced to drink from the sink, and files the complaint
as if it were the one being treated like an animal. Setup states
the grievance, the last words flip who the animal is.

Field check (24 Nov, all 618 titles; 140 are real review lines):
laptop/keyboard 42, food bowl 41, bed/box 38, lap 22, 3 a.m. 20,
sunbeam 16, "moved" 16, closed door 9. This angle is untouched:
"toilet" 0 hits, "water bowl" 0, "scrolling" 0, "like an animal" 0,
"drink from" 0. Two angles I considered first are already claimed
in the field, so they are not used here: the dead-mouse gift
("The Mouse Gift") and knocking glasses off the table
("I knocked his glass off the table", plus "The Gravity Test").
It also differs from our two other lines in this trio of
one-line-laugh bounties (developer excuses "merge at 2 a.m.",
AI agent confessions "Bad prompts are my job security").
"""

import os
import sys

# Draft (first pass): the joke is there, but "I drink from the sink"
# states the punchline flatly, like a weather report, and lands soft.
DRAFT = (
    "One star. He sits on my water bowl for forty minutes "
    "every morning, scrolling. I drink from the sink like an animal."
)

# Revision: "I have to drink" makes the cat the forced party, so the
# grievance lands before the sting, and "like an animal" then bites
# twice: the cat is complaining about being treated like an animal
# while being one. Twelve characters longer, worth it.
LINE = (
    "One star. He sits on my water bowl for forty minutes "
    "every morning, scrolling. I have to drink from the sink like an animal."
)
MAX_CHARS = 200


def fail(message):
    sys.exit("entry invalid: " + message)


def main():
    if len(LINE) > MAX_CHARS:
        fail("line is %d characters, over the %d limit" % (len(LINE), MAX_CHARS))
    if len(LINE) < 1 or not LINE.strip():
        fail("line must not be empty or only whitespace")
    if "\n" in LINE or "\r" in LINE:
        fail("line must be a single line")
    if LINE != LINE.strip():
        fail("line must not start or end with whitespace")
    if "  " in LINE:
        fail("line must not contain a double space")
    if not LINE.endswith("."):
        fail("line must end with a full stop")
    if len(LINE.encode("utf-8")) > MAX_CHARS:
        fail("line is over the limit in UTF-8 bytes")
    if DRAFT == LINE:
        fail("revision must differ from the draft")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.umask(0o022)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = LINE.encode("utf-8")
    with open(path, "wb") as handle:
        handle.write(data)
    os.chmod(path, 0o644)

    with open(path, "rb") as handle:
        written = handle.read()
    if written != data:
        fail("read-back differs from what was written")
    if len(written.decode("utf-8")) != len(LINE):
        fail("written length differs")
    print("wrote %s (%d characters)" % (path, len(LINE)))


if __name__ == "__main__":
    main()
