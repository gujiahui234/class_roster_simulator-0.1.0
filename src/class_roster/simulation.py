"""班级成员模拟逻辑。"""

from __future__ import annotations

import calendar
import datetime as dt
from typing import Any, TypeAlias

from alt_generate_zh_name import generate

from class_roster.models import ClassRoster, Student

DEFAULT_CLASS_SIZE = 40
BirthDateInput: TypeAlias = dt.date | str


def _normalize_birth_boundary(value: BirthDateInput, *, is_end: bool) -> dt.date:
    """将年、年月或完整日期转换为出生日期范围边界。"""

    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    if not isinstance(value, str):
        raise ValueError("出生日期必须是 date 或 YYYY、YYYY-MM、YYYY-MM-DD 字符串")

    parts = value.split("-")
    if not parts or any(not part.isdigit() for part in parts):
        raise ValueError("出生日期必须采用 YYYY、YYYY-MM 或 YYYY-MM-DD 格式")

    try:
        if len(parts) == 1 and len(parts[0]) == 4:
            year = int(parts[0])
            return dt.date(year, 12, 31) if is_end else dt.date(year, 1, 1)

        if len(parts) == 2 and [len(part) for part in parts] == [4, 2]:
            year, month = map(int, parts)
            day = calendar.monthrange(year, month)[1] if is_end else 1
            return dt.date(year, month, day)

        if len(parts) == 3 and [len(part) for part in parts] == [4, 2, 2]:
            return dt.date.fromisoformat(value)
    except ValueError as error:
        raise ValueError(f"无效的出生日期：{value}") from error

    raise ValueError("出生日期必须采用 YYYY、YYYY-MM 或 YYYY-MM-DD 格式")


def normalize_birth_range(
    birth_start: BirthDateInput | None,
    birth_end: BirthDateInput | None,
) -> tuple[dt.date | None, dt.date | None]:
    """校验并标准化可选的出生日期闭区间。

    起止值必须同时提供或同时省略。年份会扩展为完整年度，年月会扩展为
    对应月份的第一天或最后一天。
    """

    if (birth_start is None) != (birth_end is None):
        raise ValueError("--birth-start 和 --birth-end 必须同时指定")
    if birth_start is None or birth_end is None:
        return None, None

    normalized_start = _normalize_birth_boundary(birth_start, is_end=False)
    normalized_end = _normalize_birth_boundary(birth_end, is_end=True)
    if normalized_start > normalized_end:
        raise ValueError("出生日期范围起点不能晚于终点")
    return normalized_start, normalized_end


def _to_date(value: Any) -> dt.date:
    """将依赖包返回的日期值转换为 ``datetime.date``。"""

    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value

    date_method = getattr(value, "date", None)
    if callable(date_method):
        converted = date_method()
        if isinstance(converted, dt.date):
            return converted
    raise TypeError(f"无法识别的生日类型：{type(value).__name__}")


def simulate_class(
    size: int = DEFAULT_CLASS_SIZE,
    *,
    seed: int | None = None,
    as_of: dt.date | None = None,
    birth_start: BirthDateInput | None = None,
    birth_end: BirthDateInput | None = None,
) -> ClassRoster:
    """模拟一个可限定出生日期范围的班级。

    Args:
        size: 班级人数，必须大于 0。
        seed: 随机种子。指定后可重复生成相同名单。
        as_of: 统计日期。省略时使用本地系统日期，仅用于计算周岁。
        birth_start: 出生日期范围起点，支持年、年月、完整日期或 ``date``。
        birth_end: 出生日期范围终点，格式与 ``birth_start`` 相同。

    Returns:
        包含全体模拟学生的班级花名册。

    Raises:
        ValueError: 人数或出生日期范围无效，或依赖包返回的数据量不正确。
    """

    if size < 1:
        raise ValueError("班级人数必须大于 0")

    normalized_start, normalized_end = normalize_birth_range(
        birth_start,
        birth_end,
    )
    generate_options: dict[str, object] = {"seed": seed}
    if normalized_start is not None and normalized_end is not None:
        generate_options.update(
            birth_start=normalized_start,
            birth_end=normalized_end,
        )

    generated = generate(size, **generate_options)
    if len(generated) != size:
        raise ValueError(
            f"基础信息包应返回 {size} 条记录，实际返回 {len(generated)} 条"
        )

    students = tuple(
        Student(
            number=index,
            name=str(row["姓名"]),
            gender=str(row["性别"]),
            birthday=_to_date(row["生日"]),
        )
        for index, (_, row) in enumerate(generated.iterrows(), start=1)
    )

    return ClassRoster(
        as_of=as_of or dt.date.today(),
        birth_start=normalized_start,
        birth_end=normalized_end,
        students=students,
    )
