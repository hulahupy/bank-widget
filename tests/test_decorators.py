"""
Tests for decorators module.
"""

import os
import tempfile
from typing import List

import pytest

from src.decorators import log


def test_log_decorator_console_success(capsys: pytest.CaptureFixture) -> None:
    """Test logging to console on successful function execution."""

    @log()
    def add(a: int, b: int) -> int:
        result: int = a + b
        return result

    result = add(2, 3)
    assert result == 5

    captured = capsys.readouterr()
    assert "add ok" in captured.out


def test_log_decorator_console_error(capsys: pytest.CaptureFixture) -> None:
    """Test logging to console on function error."""

    @log()
    def divide(a: int, b: int) -> float:
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    captured = capsys.readouterr()
    assert "divide error: ZeroDivisionError" in captured.out
    assert "Inputs: (10, 0), {}" in captured.out


def test_log_decorator_file_success() -> None:
    """Test logging to file on successful function execution."""

    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp_file:
        filename: str = tmp_file.name

    try:

        @log(filename=filename)
        def multiply(a: int, b: int) -> int:
            result: int = a * b
            return result

        result = multiply(4, 5)
        assert result == 20

        with open(filename, "r", encoding="utf-8") as f:
            content: str = f.read()

        assert "multiply ok" in content
    finally:
        os.unlink(filename)


def test_log_decorator_file_error() -> None:
    """Test logging to file on function error."""

    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp_file:
        filename: str = tmp_file.name

    try:

        @log(filename=filename)
        def get_item(lst: List[int], index: int) -> int:
            return lst[index]

        with pytest.raises(IndexError):
            get_item([1, 2, 3], 5)

        with open(filename, "r", encoding="utf-8") as f:
            content: str = f.read()

        assert "get_item error: IndexError" in content
        assert "Inputs: ([1, 2, 3], 5), {}" in content
    finally:
        os.unlink(filename)


def test_log_decorator_multiple_calls(capsys: pytest.CaptureFixture) -> None:
    """Test multiple function calls with logging."""

    @log()
    def power(base: int, exp: int) -> int:
        result: int = base**exp
        return result

    power(2, 3)
    power(3, 2)

    captured = capsys.readouterr()
    lines: List[str] = captured.out.strip().split("\n")
    assert len(lines) == 2
    assert all("power ok" in line for line in lines)


def test_log_decorator_nested_functions(capsys: pytest.CaptureFixture) -> None:
    """Test logging with nested function calls."""

    @log()
    def outer(x: int) -> int:
        @log()
        def inner(y: int) -> int:
            result: int = y * 2
            return result

        inner_result: int = inner(x)
        return inner_result + 1

    result = outer(5)
    assert result == 11

    captured = capsys.readouterr()
    assert "inner ok" in captured.out
    assert "outer ok" in captured.out


def test_log_decorator_zero_division_error(capsys: pytest.CaptureFixture) -> None:
    """Test logging of ZeroDivisionError."""

    @log()
    def divide_numbers(a: int, b: int) -> float:
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide_numbers(10, 0)

    captured = capsys.readouterr()
    assert "divide_numbers error: ZeroDivisionError" in captured.out
    assert "Inputs: (10, 0), {}" in captured.out


def test_log_decorator_index_error(capsys: pytest.CaptureFixture) -> None:
    """Test logging of IndexError."""

    @log()
    def get_element(lst: List[int], index: int) -> int:
        return lst[index]

    with pytest.raises(IndexError):
        get_element([], 0)

    captured = capsys.readouterr()
    assert "get_element error: IndexError" in captured.out
    assert "Inputs: ([], 0), {}" in captured.out


def test_log_decorator_type_error(capsys: pytest.CaptureFixture) -> None:
    """Test logging of TypeError."""

    @log()
    def add_numbers(a: int, b: int) -> int:
        result: int = a + b
        return result

    with pytest.raises(TypeError):
        add_numbers("not a number", 5)  # type: ignore

    captured = capsys.readouterr()
    assert "add_numbers error: TypeError" in captured.out
    assert "Inputs: ('not a number', 5), {}" in captured.out


def test_log_decorator_with_kwargs(capsys: pytest.CaptureFixture) -> None:
    """Test logging with keyword arguments."""

    @log()
    def greet(name: str, greeting: str = "Hello") -> str:
        result: str = f"{greeting}, {name}!"
        return result

    result = greet("World", greeting="Hi")
    assert result == "Hi, World!"

    captured = capsys.readouterr()
    assert "greet ok" in captured.out


def test_log_decorator_multiple_args(capsys: pytest.CaptureFixture) -> None:
    """Test logging with multiple arguments."""

    @log()
    def complex_function(a: int, b: str, c: List[int], d: bool = True) -> str:
        result: str = f"{a} - {b} - {len(c)} - {d}"
        return result

    result = complex_function(42, "test", [1, 2, 3], d=False)
    assert result == "42 - test - 3 - False"

    captured = capsys.readouterr()
    assert "complex_function ok" in captured.out
