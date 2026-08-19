from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "src" / "class_roster"


def test_typed_marker_exists() -> None:
    assert (PACKAGE_ROOT / "py.typed").is_file()


def test_all_package_functions_and_methods_have_examples() -> None:
    missing_examples: list[str] = []

    for path in sorted(PACKAGE_ROOT.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            docstring = ast.get_docstring(node) or ""
            if "Example:" not in docstring:
                missing_examples.append(f"{path.name}:{node.lineno}:{node.name}")

    assert missing_examples == []


def test_all_package_functions_and_methods_are_annotated() -> None:
    missing_annotations: list[str] = []

    for path in sorted(PACKAGE_ROOT.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            location = f"{path.name}:{node.lineno}:{node.name}"
            arguments = [*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs]
            arguments.extend(
                argument
                for argument in (node.args.vararg, node.args.kwarg)
                if argument is not None
            )
            for argument in arguments:
                if argument.arg not in {"self", "cls"} and argument.annotation is None:
                    missing_annotations.append(f"{location}:{argument.arg}")
            if node.returns is None:
                missing_annotations.append(f"{location}:return")

    assert missing_annotations == []


def test_agent_guides_and_runnable_example_exist() -> None:
    assert (ROOT / "llms.txt").is_file()
    assert (ROOT / "AI_USAGE.md").is_file()
    assert (ROOT / "examples" / "basic_roster.py").is_file()
