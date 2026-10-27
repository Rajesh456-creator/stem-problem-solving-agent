from tools import run_symbolic_checks


def test_quadratic_roots():
    result = run_symbolic_checks("quadratic_roots", "x**2 - 5*x + 6")
    assert result["ok"] is True
    assert set(result["roots"]) == {"2", "3"}


def test_derivative():
    result = run_symbolic_checks("derivative", "x**3 + 2*x**2 - 4*x")
    assert result["derivative"] == "3*x**2 + 4*x - 4"


def test_no_check():
    assert run_symbolic_checks("none", "")["supported"] is False
