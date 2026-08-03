"""班级数据模型测试。"""

import datetime as dt

from class_roster.models import ClassRoster, Student


def test_student_age_on_birthday_boundary() -> None:
    """生日当天才增加一周岁。"""

    student = Student(1, "张小明", "男", dt.date(2014, 8, 1))

    assert student.age_on(dt.date(2026, 7, 31)) == 11
    assert student.age_on(dt.date(2026, 8, 1)) == 12


def test_roster_render_contains_every_student() -> None:
    """花名册文本包含摘要、表头与每名学生。"""

    roster = ClassRoster(
        as_of=dt.date(2026, 7, 31),
        academic_year_start=2025,
        birth_start=dt.date(2013, 9, 1),
        birth_end=dt.date(2014, 8, 31),
        students=(
            Student(1, "张小明", "男", dt.date(2014, 2, 3)),
            Student(2, "李小红", "女", dt.date(2013, 10, 4)),
        ),
    )

    rendered = roster.render()

    assert "小学六年级班级花名册" in rendered
    assert "班级人数：2 人" in rendered
    assert "学号\t姓名\t性别\t出生日期\t年龄" in rendered
    assert "01\t张小明\t男\t2014-02-03\t12" in rendered
    assert "02\t李小红\t女\t2013-10-04\t12" in rendered

