#!/usr/bin/env python3
"""Interpreter probe for the hook launcher.

Prints the resolved interpreter path and version, then exits 0 when the
interpreter meets the minimum supported version and 1 otherwise.

This exists as a committed file so `run-python-hook.js` never has to pass an
inline `-c` code string to a subprocess: the launcher's argument vector is
built entirely from constants and validated paths.
"""

import sys

MINIMUM_VERSION = (3, 10)


def main() -> int:
    print(sys.executable)
    print(sys.version.split()[0])
    return 0 if sys.version_info >= MINIMUM_VERSION else 1


if __name__ == "__main__":
    raise SystemExit(main())
