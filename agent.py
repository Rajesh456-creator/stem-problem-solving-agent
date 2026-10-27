
import json
import re

import requests

from schemas import SolutionDraft
from tools import run_symbolic_checks, verify_quadratic_answer

DEFAULT_ENDPOINT = "https://router.huggingface.co/v1/chat/completions"
TIMEOUT = 90


def _extract_json(text: str) -> dict:
    cleaned = re.sub(
        r"^```(?:json)?\s*",
        "",
        text.strip(),
        flags=re.I,
    )
    cleaned = re.sub(r"\s*```$", "", cleaned)

    start = cleaned.find("{")
    end = cleaned.rfind("}")

    if start < 0 or end <= start:
        raise ValueError(
            "The model did not return valid JSON. "
            "Try again or choose another model."
        )

    return json.loads(cleaned[start:end + 1])


def _call_model(question: str, token: str, model: str) -> str:
    prompt = f"""Solve this STEM question carefully. Return ONLY valid JSON with keys:
topic (string), assumptions (array of strings), steps (array of strings),
final_answer (string), verification_expression (string),
verification_type (one of quadratic_roots, derivative, simplify, none).

For quadratic_roots, verification_expression should be a polynomial in x,
e.g. x**2 - 5*x + 6. Report the roots clearly, e.g. "x = 2 and x = 3".

For derivative, verification_expression should be an expression in x,
e.g. x**3 + 2*x**2 - 4*x.

Do not claim a tool verified something. If no supported symbolic check
applies, use verification_type "none".

Question: {question}"""

    response = requests.post(
        DEFAULT_ENDPOINT,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a careful STEM tutor. "
                        "Return only valid JSON."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.1,
            "max_tokens": 1200,
        },
        timeout=TIMEOUT,
    )

    if response.status_code >= 400:
        raise RuntimeError(
            f"Hosted inference returned HTTP {response.status_code}: "
            f"{response.text[:400]}"
        )

    payload = response.json()

    try:
        return payload["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError(
            f"Unexpected response format: {str(payload)[:300]}"
        ) from exc


def solve_problem(question: str, token: str, model: str) -> dict:
    try:
        raw = _call_model(question, token, model)

        structured = SolutionDraft.model_validate(
            _extract_json(raw)
        ).model_dump()

        check_type = structured["verification_type"]
        expression = structured["verification_expression"]
        final_answer = structured["final_answer"]

        # Keep the original symbolic check for transparency.
        checks = run_symbolic_checks(check_type, expression)

        answer_verification = None

        if check_type == "quadratic_roots":
            # Compare the model's reported roots with SymPy's roots.
            answer_verification = verify_quadratic_answer(
                expression,
                final_answer,
            )

            verification_status = (
                "Quadratic answer verification: "
                f"{answer_verification['status']}. "
                f"{answer_verification['message']}"
            )

        elif checks.get("supported") and checks.get("ok") is True:
            verification_status = (
                "The symbolic calculation completed successfully. "
                "The AI final answer has not been independently compared "
                "for this check type."
            )

        elif checks.get("supported"):
            verification_status = (
                "The symbolic check did not pass. "
                "Review the result carefully."
            )

        else:
            verification_status = (
                "No supported automatic symbolic check applied. "
                "Human review is needed."
            )

        assumptions = (
            structured.get("assumptions") or ["No assumptions stated."]
        )

        steps = "\n".join(
            f"{i}. {step}"
            for i, step in enumerate(structured["steps"], 1)
        )

        final = (
            f"**Topic:** {structured['topic']}\n\n"
            f"**Steps**\n{steps}\n\n"
            f"**Final answer:** {final_answer}\n\n"
            f"**Assumptions**\n"
            + "\n".join(f"- {item}" for item in assumptions)
            + f"\n\n**Automatic check:** {verification_status}"
        )

        return {
            "structured": structured,
            "checks": checks,
            "answer_verification": answer_verification,
            "verification_status": verification_status,
            "final_answer": final,
        }

    except requests.exceptions.Timeout:
        return {
            "error": (
                "The hosted model timed out. "
                "Try again or select a different model."
            )
        }

    except requests.exceptions.ConnectionError:
        return {
            "error": (
                "Could not connect to the hosted inference endpoint. "
                "Check your connection and try again."
            )
        }

    except Exception as exc:
        return {"error": f"{type(exc).__name__}: {exc}"}
