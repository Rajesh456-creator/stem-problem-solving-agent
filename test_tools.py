
from tools import run_symbolic_checks, verify_quadratic_answer


def test_quadratic_roots():
    result = run_symbolic_checks(
        "quadratic_roots",
        "x**2 - 5*x + 6",
    )

    assert result["supported"] is True
    assert result["ok"] is True
    assert set(result["roots"]) == {"2", "3"}
    assert set(result["substitution_results"]) == {"0"}


def test_reject_non_quadratic_expression():
    result = run_symbolic_checks(
        "quadratic_roots",
        "x**3 - 1",
    )

    assert result["supported"] is True
    assert result["ok"] is False


def test_derivative():
    result = run_symbolic_checks(
        "derivative",
        "x**3 + 2*x**2 - 4*x",
    )

    assert result["derivative"] == "3*x**2 + 4*x - 4"


def test_simplify():
    result = run_symbolic_checks("simplify", "x + x")

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


def test_answer_verification_pass():
    result = verify_quadratic_answer(
        "x**2 - 5*x + 6",
        "The roots are x = 2 and x = 3.",
    )

    assert result["status"] == "PASS"
    assert result["ok"] is True


def test_answer_verification_fail():
    result = verify_quadratic_answer(
        "x**2 - 5*x + 6",
        "The roots are x = 2 and x = 4.",
    )

    assert result["status"] == "FAIL"
    assert result["ok"] is False


def test_answer_verification_review():
    result = verify_quadratic_answer(
        "x**2 - 5*x + 6",
        "The answer is probably two and three.",
    )

    assert result["status"] == "REVIEW"
    assert result["ok"] is None
