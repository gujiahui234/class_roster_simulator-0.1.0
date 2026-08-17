"""班级模拟逻辑测试。"""

import datetime as dt

import pandas as pd
import pytest

from class_roster import simulation


@pytest.mark.parametrize(
    ("birth_start", "birth_end", "expected"),
    [
        ("2014", "2014", (dt.date(2014, 1, 1), dt.date(2014, 12, 31))),
        (
            "2014-03",
            "2014-05",
            (dt.date(2014, 3, 1), dt.date(2014, 5, 31)),
        ),
        (
            "2014-04-15",
            "2014-04-15",
            (dt.date(2014, 4, 15), dt.date(2014, 4, 15)),
        ),
    ],
)
def test_normalize_birth_range(
    birth_start: str,
    birth_end: str,
    expected: tuple[dt.date, dt.date],
) -> None:
    """年、年月和完整日期都能转换为准确的闭区间。"""

    assert simulation.normalize_birth_range(birth_start, birth_end) == expected


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
        birth_start="2008-09",
        birth_end="2010-08",
    )

    assert captured == {
        "size": 2,
        "birth_start": dt.date(2008, 9, 1),
        "birth_end": dt.date(2010, 8, 31),
        "seed": 42,
    }
    assert [student.number for student in roster.students] == [1, 2]
    assert [student.name for student in roster.students] == ["张小明", "李小红"]
    assert roster.birth_start == dt.date(2008, 9, 1)
    assert roster.birth_end == dt.date(2010, 8, 31)


def test_simulate_class_does_not_apply_a_grade_limit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """未指定范围时不向生成器添加固定年级的出生日期限制。"""

    captured: dict[str, object] = {}

    def fake_generate(size: int, **kwargs: object) -> pd.DataFrame:
        captured.update(kwargs)
        return pd.DataFrame(
            [{"姓名": "王一", "性别": "男", "生日": dt.date(2000, 1, 1)}]
        )

    monkeypatch.setattr(simulation, "generate", fake_generate)

    roster = simulation.simulate_class(1, seed=7)

    assert captured == {"seed": 7}
    assert roster.birth_start is None
    assert roster.birth_end is None


@pytest.mark.parametrize(
    ("birth_start", "birth_end", "message"),
    [
        ("2014", None, "必须同时指定"),
        ("2015", "2014", "起点不能晚于终点"),
        ("2014/01", "2014-12", "必须采用"),
    ],
)
def test_simulate_class_rejects_invalid_birth_range(
    birth_start: str | None,
    birth_end: str | None,
    message: str,
) -> None:
    """不完整、倒置或格式错误的出生日期范围会被拒绝。"""

    with pytest.raises(ValueError, match=message):
        simulation.simulate_class(
            1,
            birth_start=birth_start,
            birth_end=birth_end,
        )


def test_simulate_class_rejects_non_positive_size() -> None:
    """班级人数必须大于零。"""

    with pytest.raises(ValueError, match="大于 0"):
        simulation.simulate_class(0)
