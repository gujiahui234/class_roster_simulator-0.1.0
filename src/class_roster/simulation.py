"""六年级班级成员模拟逻辑。"""

from __future__ import annotations

import datetime as dt
from typing import Any

from alt_generate_zh_name import generate

from class_roster.models import ClassRoster, Student

SCHOOL_YEAR_START_MONTH = 9
GRADE_SIX_BIRTH_YEAR_OFFSET = 12
DEFAULT_CLASS_SIZE = 40


def academic_year_start(on_date: dt.date) -> int:
    """获取指定日期所在学年的起始年份。

    中国学校通常在 9 月开始新学年。例如，2026 年 7 月仍属于
    2025-2026 学年。

    Args:
        on_date: 需要判断所属学年的日期。

    Returns:
        学年开始时的公历年份。
    """

    if on_date.month >= SCHOOL_YEAR_START_MONTH:
        return on_date.year
    return on_date.year - 1


def grade_six_birth_range(on_date: dt.date) -> tuple[dt.date, dt.date]:
    """推算当前六年级学生的常见出生日期范围。

    计算采用 9 月 1 日入学分界，并假设学生按常规年龄入学，不考虑
    提前入学、延迟入学或留级等个别情况。

    Args:
        on_date: 模拟所依据的当前日期。

    Returns:
        包含起始日期与结束日期的闭区间。
    """

    start_year = academic_year_start(on_date) - GRADE_SIX_BIRTH_YEAR_OFFSET
    return dt.date(start_year, 9, 1), dt.date(start_year + 1, 8, 31)


def _to_date(value: Any) -> dt.date:
    """将依赖包返回的日期值转换为 ``datetime.date``。

    Args:
        value: 日期、日期时间或具有 ``date()`` 方法的日期值。

    Returns:
        标准库的 ``datetime.date`` 对象。

    Raises:
        TypeError: 输入值无法转换为日期。
    """

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
) -> ClassRoster:
    """模拟当前小学六年级的一个班级。

    Args:
        size: 班级人数，必须大于 0。
        seed: 随机种子。指定后可重复生成相同名单。
        as_of: 模拟依据日期。省略时使用本地系统日期。

    Returns:
        包含全体模拟学生的班级花名册。

    Raises:
        ValueError: 班级人数不大于 0，或依赖包返回的数据量不正确。
    """

    if size < 1:
        raise ValueError("班级人数必须大于 0")

    current_date = as_of or dt.date.today()
    birth_start, birth_end = grade_six_birth_range(current_date)
    generated = generate(
        size,
        birth_start=birth_start,
        birth_end=birth_end,
        seed=seed,
    )

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
        as_of=current_date,
        academic_year_start=academic_year_start(current_date),
        birth_start=birth_start,
        birth_end=birth_end,
        students=students,
    )

