
import pytest

from tools import run_symbolic_checks


def test_quadratic_roots():
    result = run_symbolic_checks(
        "quadratic_roots",
        "x**2 - 5*x + 6",
    )

    assert result["supported"] is True
    assert result["ok"] is True
    assert set(result["roots"]) == {"2", "3"}
    assert set(result["substitution_results"]) == {"0"}


def test_quadratic_roots_with_repeated_root():
    result = run_symbolic_checks(
        "quadratic_roots",
        "x**2 - 4*x + 4",
    )

    assert result["ok"] is True
    assert result["roots"] == ["2"]


def test_derivative():
    result = run_symbolic_checks(
        "derivative",
        "x**3 + 2*x**2 - 4*x",
    )

    assert result["supported"] is True
    assert result["ok"] is True
    assert result["derivative"] == "3*x**2 + 4*x - 4"


def test_simplify():
    result = run_symbolic_checks(
        "simplify",
        "x + x",
    )

    assert result["supported"] is True
    assert result["ok"] is True
    assert result["simplified"] == "2*x"


def test_no_check():
    result = run_symbolic_checks("none", "")

    assert result["supported"] is False
    assert result["ok"] is None


def test_unsupported_check_type():
    result = run_symbolic_checks("unknown", "x + 1")

    assert result["supported"] is False
    assert result["ok"] is None


def test_invalid_expression():
    result = run_symbolic_checks("derivative", "x + (")

    assert result["supported"] is True
    assert result["ok"] is False
    assert "Check failed" in result["message"]
