"""扩展学生信息生成功能测试。"""

import datetime as dt

import pytest
from alt_generate_zh_name import generate


@pytest.mark.parametrize(
    ("birth_start", "birth_end", "expected_start", "expected_end"),
    [
        ("2014", "2014", dt.date(2014, 1, 1), dt.date(2014, 12, 31)),
        ("2014-03", "2014-05", dt.date(2014, 3, 1), dt.date(2014, 5, 31)),
        ("2014-04-15", "2014-04-15", dt.date(2014, 4, 15), dt.date(2014, 4, 15)),
    ],
    ids=["year", "month-range", "exact-date"],
)
def test_generate_with_birth_range(
    birth_start: str,
    birth_end: str,
    expected_start: dt.date,
    expected_end: dt.date,
) -> None:
    """年份、年月范围和具体日期都应限制生成的生日。"""

    students = generate(
        100,
        birth_start=birth_start,
        birth_end=birth_end,
        seed=2026,
    )

    assert students["生日"].map(type).eq(dt.date).all()
    assert students["生日"].between(expected_start, expected_end).all()


def test_generate_with_fixed_surname_and_random_given_name() -> None:
    """固定姓氏后，所有姓名应同姓且随机名字不应全部相同。"""

    students = generate(50, surname="王", seed=2026)
    names = students["姓名"]
    given_names = names.str.removeprefix("王")

    assert names.str.startswith("王").all()
    assert given_names.str.len().isin([1, 2]).all()
    assert given_names.nunique() > 1


@pytest.mark.parametrize("name_length", [1, 2], ids=["single-name", "double-name"])
def test_generate_with_fixed_given_name_length(name_length: int) -> None:
    """name_length=1 应生成单名，name_length=2 应生成双名。"""

    students = generate(50, surname="欧阳", name_length=name_length, seed=2026)
    given_names = students["姓名"].str.removeprefix("欧阳")

    assert given_names.str.len().eq(name_length).all()
    assert given_names.nunique() > 1
