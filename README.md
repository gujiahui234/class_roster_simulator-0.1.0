# 班级花名册模拟器

这是一个使用 Python 3.10+ 开发的命令行小程序。它调用
[`alt_generate_zh_name`](https://github.com/ashida2016/alt_generate_zh_name)
生成虚构的学生姓名、性别和生日，并在终端打印完整花名册。

本程序不限定年级。可以按年、年月或具体日期限定学生的出生日期范围。

## 功能

- 默认模拟 40 名学生；
- 可限定出生日期闭区间，范围起点和终点都包含在内；
- 支持 `YYYY`、`YYYY-MM` 和 `YYYY-MM-DD` 三种日期精度；
- 打印学号、姓名、性别、出生日期和统计日周岁；
- 支持自定义班级人数、随机种子和统计日期；
- 使用相同参数和随机种子复现同一份名单。

所有学生信息均为程序随机生成的虚构数据。

## 环境要求

- Python 3.10 或更高版本
- Git（安装 GitHub 源码依赖时需要）

## 安装

建议先创建并激活虚拟环境：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

也可以只安装运行依赖：

```powershell
python -m pip install -r requirements.txt
python -m pip install -e .
```

`pyproject.toml` 和 `requirements.txt` 均将基础信息包固定到已核实的 Git
提交，以保证安装结果可复现。

## 命令行使用

推荐同时指定出生日期范围：

```powershell
class-roster --size 45 --seed 2026 --as-of 2026-07-31 `
  --birth-start 2008-09-01 --birth-end 2010-08-31
```

如果确实不需要限制出生日期，可以省略两个范围参数：

```powershell
class-roster --size 40 --seed 2026
```

也可以按年或年月指定。例如，下面的实际范围是 `2014-03-01` 至
`2014-05-31`：

```powershell
class-roster --birth-start 2014-03 --birth-end 2014-05
```

起止参数必须同时指定。三种格式的扩展规则如下：

| 输入 | 用作起点 | 用作终点 |
| --- | --- | --- |
| `2014` | `2014-01-01` | `2014-12-31` |
| `2014-03` | `2014-03-01` | `2014-03-31` |
| `2014-03-15` | `2014-03-15` | `2014-03-15` |

也可以通过 Python 模块运行：

```powershell
python -m class_roster --birth-start 2008 --birth-end 2010
```

查看全部参数：

```powershell
class-roster --help
```

输出示意：

```text
班级花名册
统计日期：2026-07-31
出生日期范围：2008-09-01 至 2010-08-31
班级人数：40 人

学号    姓名    性别    出生日期      年龄
01      张小明  男      2009-02-03    17
...
```

## Python API

使用 `datetime.date` 指定完整日期范围：

```python
from datetime import date

from class_roster import simulate_class

roster = simulate_class(
    size=5,
    seed=2026,
    as_of=date(2026, 7, 31),
    birth_start=date(2008, 9, 1),
    birth_end=date(2010, 8, 31),
)

print(roster.render())

for student in roster.students:
    print(student.number, student.name, student.gender, student.birthday)
```

也可以使用字符串按年或年月限定范围：

```python
roster = simulate_class(
    size=5,
    seed=2026,
    birth_start="2008-09",
    birth_end="2010-08",
)
```

如果不传 `birth_start` 和 `birth_end`，主程序不会附加固定年级的出生日期限制。

## 底层生成器扩展功能

项目依赖的 `alt_generate_zh_name.generate()` 还支持指定姓氏和名字长度，并返回列名为
`姓名`、`性别`、`生日` 的 `pandas.DataFrame`。

指定姓氏，随机生成名字：

```python
from alt_generate_zh_name import generate

students = generate(
    10,
    surname="王",
    birth_start="2008-09-01",
    birth_end="2010-08-31",
    seed=2026,
)
assert students["姓名"].str.startswith("王").all()
```

`surname` 支持复姓。`name_length=1` 表示单名，`name_length=2` 表示双名：

```python
students = generate(
    30,
    surname="欧阳",
    name_length=2,
    birth_start="2008-09-01",
    birth_end="2010-08-31",
    seed=2026,
)
```

`name_length` 只计算名字部分，不包含姓氏。

## 测试

```powershell
python -m pytest
```

## 项目结构

```text
.
├── pyproject.toml
├── requirements.txt
├── README.md
├── src/
│   └── class_roster/
│       ├── cli.py
│       ├── models.py
│       └── simulation.py
└── tests/
```
