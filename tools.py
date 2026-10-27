
import re

import sympy as sp


def run_symbolic_checks(check_type: str, expression: str) -> dict:
    """Run supported symbolic mathematics checks with SymPy."""

    if check_type == "none" or not expression.strip():
        return {
            "supported": False,
            "ok": None,
            "message": "No supported symbolic expression supplied.",
        }

    try:
        x = sp.Symbol("x")
        expr = sp.sympify(expression, locals={"x": x})

        if check_type == "quadratic_roots":
            poly = sp.Poly(expr, x)

            if poly.degree() != 2:
                return {
                    "supported": True,
                    "ok": False,
                    "message": "Expected a quadratic polynomial in x.",
                }

            roots = sp.solve(expr, x)
            results = [
                sp.simplify(expr.subs(x, root))
                for root in roots
            ]

            # Accept repeated roots as well as two distinct roots.
            ok = poly.degree() == 2 and all(
                value == 0 for value in results
            )

            return {
                "supported": True,
                "ok": bool(ok),
                "expression": str(expr),
                "roots": [str(root) for root in roots],
                "substitution_results": [
                    str(value) for value in results
                ],
            }

        if check_type == "derivative":
            return {
                "supported": True,
                "ok": True,
                "expression": str(expr),
                "derivative": str(sp.diff(expr, x)),
            }

        if check_type == "simplify":
            return {
                "supported": True,
                "ok": True,
                "expression": str(expr),
                "simplified": str(sp.simplify(expr)),
            }

        return {
            "supported": False,
            "ok": None,
            "message": f"Unsupported check: {check_type}",
        }

    except Exception as exc:
        return {
            "supported": True,
            "ok": False,
            "message": (
                f"Check failed: {type(exc).__name__}: {exc}"
            ),
        }


def verify_quadratic_answer(
    expression: str,
    final_answer: str,
) -> dict:
    """Compare clearly formatted reported roots with SymPy roots."""

    check = run_symbolic_checks(
        "quadratic_roots",
        expression,
    )

    if not check.get("supported") or check.get("ok") is not True:
        return {
            "supported": False,
            "ok": None,
            "status": "REVIEW",
            "message": (
                "Could not independently verify the quadratic expression."
            ),
        }

    number = r"-?\d+(?:\.\d+)?(?:/\d+)?"

    patterns = [
        rf"x\s*=\s*({number})\s*(?:,|and|or)\s*x\s*=\s*({number})",
        rf"(?:roots|solutions)\s*(?:are|:|=)\s*({number})\s*(?:,|and|or)\s*({number})",
    ]

    reported = None

    for pattern in patterns:
        match = re.search(
            pattern,
            final_answer,
            flags=re.IGNORECASE,
        )
        if match:
            reported = list(match.groups())
            break

    if reported is None:
        return {
            "supported": True,
            "ok": None,
            "status": "REVIEW",
            "expected_roots": check["roots"],
            "message": (
                "Could not reliably extract two roots from the final answer. "
                "Human review is needed."
            ),
        }

    try:
        x = sp.Symbol("x")
        poly = sp.Poly(sp.sympify(expression, locals={"x": x}), x)

        # all_roots() preserves multiplicity, e.g. [2, 2].
        expected_roots = poly.all_roots()
        reported_roots = [
            sp.sympify(value, rational=True)
            for value in reported
        ]

        matches = (
            len(reported_roots) == len(expected_roots)
            and all(
                sp.simplify(a - b) == 0
                for a, b in zip(
                    sorted(reported_roots, key=sp.default_sort_key),
                    sorted(expected_roots, key=sp.default_sort_key),
                )
            )
        )

        return {
            "supported": True,
            "ok": bool(matches),
            "status": "PASS" if matches else "FAIL",
            "expected_roots": [str(root) for root in expected_roots],
            "reported_roots": [str(root) for root in reported_roots],
            "message": (
                "Reported roots match the symbolic result."
                if matches
                else "Reported roots do not match the symbolic result."
            ),
        }

    except Exception:
        return {
            "supported": True,
            "ok": False,
            "status": "FAIL",
            "expected_roots": check["roots"],
            "message": "Could not parse or compare the reported roots.",
        }
