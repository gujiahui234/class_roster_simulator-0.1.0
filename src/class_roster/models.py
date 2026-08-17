"""班级与学生的数据模型。"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Student:
    """一名模拟学生的基础信息。

    Attributes:
        number: 班内学号，从 1 开始。
        name: 学生姓名。
        gender: 学生性别。
        birthday: 学生出生日期。
    """

    number: int
    name: str
    gender: str
    birthday: dt.date

    def age_on(self, on_date: dt.date) -> int:
        """计算学生在指定日期的周岁。

        Args:
            on_date: 用于计算年龄的日期。

        Returns:
            学生在指定日期的周岁。
        """

        birthday_has_passed = (on_date.month, on_date.day) >= (
            self.birthday.month,
            self.birthday.day,
        )
        return on_date.year - self.birthday.year - (not birthday_has_passed)


@dataclass(frozen=True, slots=True)
class ClassRoster:
    """一次班级模拟的结果。

    Attributes:
        as_of: 模拟所依据的日期。
        birth_start: 指定的出生日期范围起点；未限定时为 ``None``。
        birth_end: 指定的出生日期范围终点；未限定时为 ``None``。
        students: 班级学生，按学号排列。
    """

    as_of: dt.date
    birth_start: dt.date | None
    birth_end: dt.date | None
    students: tuple[Student, ...]

    def render(self) -> str:
        """将班级花名册渲染为适合终端输出的文本。

        Returns:
            包含班级摘要和全体学生信息的多行文本。
        """

        birth_range = "未限定"
        if self.birth_start is not None and self.birth_end is not None:
            birth_range = (
                f"{self.birth_start.isoformat()} 至 {self.birth_end.isoformat()}"
            )

        lines = [
            "班级花名册",
            f"统计日期：{self.as_of.isoformat()}",
            f"出生日期范围：{birth_range}",
            f"班级人数：{len(self.students)} 人",
            "",
            "学号\t姓名\t性别\t出生日期\t年龄",
        ]
        lines.extend(
            (
                f"{student.number:02d}\t{student.name}\t{student.gender}\t"
                f"{student.birthday.isoformat()}\t"
                f"{student.age_on(self.as_of)}"
            )
            for student in self.students
        )
        return "\n".join(lines)
