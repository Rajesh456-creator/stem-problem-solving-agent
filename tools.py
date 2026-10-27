import sympy as sp


def run_symbolic_checks(check_type: str, expression: str) -> dict:
    if check_type == "none" or not expression.strip():
        return {"supported": False, "ok": None, "message": "No supported symbolic expression supplied."}
    try:
        x = sp.Symbol("x")
        expr = sp.sympify(expression, locals={"x": x})
        if check_type == "quadratic_roots":
            roots = sp.solve(expr, x)
            results = [sp.simplify(expr.subs(x, root)) for root in roots]
            ok = all(v == 0 for v in results)
            return {"supported": True, "ok": bool(ok), "expression": str(expr),
                    "roots": [str(r) for r in roots],
                    "substitution_results": [str(v) for v in results]}
        if check_type == "derivative":
            return {"supported": True, "ok": True, "expression": str(expr),
                    "derivative": str(sp.diff(expr, x))}
        if check_type == "simplify":
            return {"supported": True, "ok": True, "expression": str(expr),
                    "simplified": str(sp.simplify(expr))}
        return {"supported": False, "ok": None, "message": f"Unsupported check: {check_type}"}
    except Exception as exc:
        return {"supported": True, "ok": False, "message": f"Check failed: {type(exc).__name__}: {exc}"}
