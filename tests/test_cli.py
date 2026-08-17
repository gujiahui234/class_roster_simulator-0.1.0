"""命令行入口测试。"""

import datetime as dt

from class_roster import cli
from class_roster.models import ClassRoster, Student


def test_main_prints_roster(monkeypatch, capsys) -> None:
    """命令行成功打印生成的花名册。"""

    roster = ClassRoster(
        as_of=dt.date(2026, 7, 31),
        birth_start=dt.date(2008, 9, 1),
        birth_end=dt.date(2010, 8, 31),
        students=(Student(1, "张小明", "男", dt.date(2014, 2, 3)),),
    )
    received: dict[str, object] = {}

    def fake_simulate_class(**kwargs: object) -> ClassRoster:
        """记录命令行参数并返回固定花名册。"""

        received.update(kwargs)
        return roster

    monkeypatch.setattr(cli, "simulate_class", fake_simulate_class)

    result = cli.main(
        [
            "--size",
            "1",
            "--seed",
            "7",
            "--as-of",
            "2026-07-31",
            "--birth-start",
            "2008-09",
            "--birth-end",
            "2010-08",
        ]
    )

    assert result == 0
    assert received == {
        "size": 1,
        "seed": 7,
        "as_of": dt.date(2026, 7, 31),
        "birth_start": "2008-09",
        "birth_end": "2010-08",
    }
    assert "张小明" in capsys.readouterr().out
