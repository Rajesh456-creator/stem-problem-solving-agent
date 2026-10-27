from pydantic import BaseModel, Field
from typing import Literal


class SolutionDraft(BaseModel):
    topic: str
    assumptions: list[str] = Field(default_factory=list)
    steps: list[str] = Field(min_length=1)
    final_answer: str
    verification_expression: str = ""
    verification_type: Literal["quadratic_roots", "derivative", "simplify", "none"] = "none"
