"""班级模拟逻辑测试。"""

import datetime as dt

import pandas as pd
import pytest

from class_roster import simulation


def test_academic_year_changes_in_september() -> None:
    """9 月开始新的学年。"""

    assert simulation.academic_year_start(dt.date(2026, 8, 31)) == 2025
    assert simulation.academic_year_start(dt.date(2026, 9, 1)) == 2026


def test_grade_six_birth_range_for_current_school_year() -> None:
    """2025-2026 学年对应六年级常见出生区间。"""

    assert simulation.grade_six_birth_range(dt.date(2026, 7, 31)) == (
        dt.date(2013, 9, 1),
        dt.date(2014, 8, 31),
    )


def test_simulate_class_maps_generated_students(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """依赖包返回的数据被编号并映射为学生模型。"""

    captured: dict[str, object] = {}

    def fake_generate(size: int, **kwargs: object) -> pd.DataFrame:
        """返回确定的基础信息测试数据。"""

        captured["size"] = size
        captured.update(kwargs)
        return pd.DataFrame(
            [
                {"姓名": "张小明", "性别": "男", "生日": dt.date(2014, 2, 3)},
                {"姓名": "李小红", "性别": "女", "生日": dt.date(2013, 10, 4)},
            ]
        )

    monkeypatch.setattr(simulation, "generate", fake_generate)

    roster = simulation.simulate_class(
        2,
        seed=42,
        as_of=dt.date(2026, 7, 31),
    )

    assert captured == {
        "size": 2,
        "birth_start": dt.date(2013, 9, 1),
        "birth_end": dt.date(2014, 8, 31),
        "seed": 42,
    }
    assert [student.number for student in roster.students] == [1, 2]
    assert [student.name for student in roster.students] == ["张小明", "李小红"]


def test_simulate_class_rejects_non_positive_size() -> None:
    """班级人数必须大于零。"""

    with pytest.raises(ValueError, match="大于 0"):
        simulation.simulate_class(0)

