"""班级花名册模拟器的命令行入口。"""

from __future__ import annotations

import argparse
import datetime as dt
from collections.abc import Sequence

from class_roster.simulation import DEFAULT_CLASS_SIZE, simulate_class


def _iso_date(value: str) -> dt.date:
    """解析 ISO 8601 格式的日期参数。

    Args:
        value: ``YYYY-MM-DD`` 格式的日期字符串。

    Returns:
        解析后的日期。

    Raises:
        argparse.ArgumentTypeError: 参数不是有效的 ISO 日期。
    """

    try:
        return dt.date.fromisoformat(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            "日期必须采用 YYYY-MM-DD 格式"
        ) from error


def build_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器。

    Returns:
        配置完成的参数解析器。
    """

    parser = argparse.ArgumentParser(
        description="模拟班级成员，可限定出生日期范围，并打印花名册。",
    )
    parser.add_argument(
        "--size",
        type=int,
        default=DEFAULT_CLASS_SIZE,
        help=f"班级人数（默认：{DEFAULT_CLASS_SIZE}）",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="随机种子；指定后可重复得到同一份名单",
    )
    parser.add_argument(
        "--as-of",
        type=_iso_date,
        default=None,
        metavar="YYYY-MM-DD",
        help="模拟依据日期（默认：今天）",
    )
    parser.add_argument(
        "--birth-start",
        default=None,
        metavar="DATE",
        help="出生日期范围起点，格式为 YYYY、YYYY-MM 或 YYYY-MM-DD",
    )
    parser.add_argument(
        "--birth-end",
        default=None,
        metavar="DATE",
        help="出生日期范围终点，格式为 YYYY、YYYY-MM 或 YYYY-MM-DD",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """运行命令行程序并打印班级花名册。

    Args:
        argv: 命令行参数。省略时读取系统命令行。

    Returns:
        进程退出码；成功时为 0。
    """

    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        roster = simulate_class(
            size=args.size,
            seed=args.seed,
            as_of=args.as_of,
            birth_start=args.birth_start,
            birth_end=args.birth_end,
        )
    except ValueError as error:
        parser.error(str(error))
    print(roster.render())
    return 0
