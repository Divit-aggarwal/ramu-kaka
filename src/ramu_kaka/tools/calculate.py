"""calculate: exact arithmetic. Parsed with `ast`; never eval/exec (hard rule 2)."""

import ast
import math
import operator

from pydantic import Field

from ramu_kaka.sandbox.state import PhoneState, Strict

NAME = "calculate"
DESCRIPTION = ("Work out a math expression exactly. Use only numbers, + - * / and parentheses, "
               "with no commas inside numbers, e.g. 2340/3 or (2.5*17). Never do math in your head.")
RISK = "Safe"
VERSION = "v1"

_BINARY = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}


class Args(Strict):
    expression: str = Field(min_length=1, max_length=200, description="e.g. 2340/3")


def _evaluate(node: ast.AST) -> float:
    """Walk the parsed tree, allowing only numbers, + - * /, and unary minus."""
    if isinstance(node, ast.Expression):
        return _evaluate(node.body)
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):  # bool is excluded
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _BINARY:
        return _BINARY[type(node.op)](_evaluate(node.left), _evaluate(node.right))
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -_evaluate(node.operand)
    raise ValueError(type(node).__name__)


def run(state: PhoneState, args: Args) -> dict:
    expression = args.expression.replace("×", "*").replace("÷", "/").replace("−", "-")
    try:
        value = _evaluate(ast.parse(expression, mode="eval"))
    except ZeroDivisionError:
        return {"error": "Division by zero."}
    except (SyntaxError, ValueError):
        return {"error": "Use only numbers, + - * / and parentheses, e.g. 2340/3. No commas in numbers."}
    if not math.isfinite(value):  # inf, or nan from inf - inf
        return {"error": "The result is infinite or not a number."}
    value = round(value, 10)
    return {"result": int(value) if float(value).is_integer() else value}
