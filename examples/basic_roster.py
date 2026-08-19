"""Directly runnable application scaffold for class-roster-simulator."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from class_roster import simulate_class


def build_parser() -> argparse.ArgumentParser:
    """Build the example command-line parser.

    Example:
        >>> build_parser().parse_args(["--size", "3"]).size
        3
    """

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--size", type=int, default=3)
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--birth-start", default="2008-09-01")
    parser.add_argument("--birth-end", default="2010-08-31")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Generate and print one fictional class roster.

    Example:
        Run ``python examples/basic_roster.py --size 5`` from the repository
        root after installing the package.
    """

    args = build_parser().parse_args(argv)
    roster = simulate_class(
        size=args.size,
        seed=args.seed,
        birth_start=args.birth_start,
        birth_end=args.birth_end,
    )
    print(roster.render())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
