import re
import ast
import operator
from typing import Optional, Dict, Any

class SafeCalculator:
    """
    Safe mathematical expression evaluator for arithmetic tool calling.
    Supports addition, subtraction, multiplication, division, modulo, and exponentiation.
    """
    
    ALLOWED_OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    @classmethod
    def evaluate(cls, expression: str) -> Dict[str, Any]:
        """Safely evaluates an arithmetic expression."""
        clean_expr = expression.strip().replace("$", "").replace(",", "")
        try:
            tree = ast.parse(clean_expr, mode='eval')
            result = cls._eval_node(tree.body)
            return {
                "success": True,
                "expression": expression,
                "result": result,
                "formatted": f"{result:,.4f}".rstrip("0").rstrip(".") if isinstance(result, float) else str(result)
            }
        except Exception as e:
            return {
                "success": False,
                "expression": expression,
                "error": f"Failed to compute arithmetic expression: {str(e)}"
            }

    @classmethod
    def _eval_node(cls, node):
        if isinstance(node, ast.Constant): # Numbers
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Unsupported constant: {node.value}")
        elif isinstance(node, ast.BinOp):
            left = cls._eval_node(node.left)
            right = cls._eval_node(node.right)
            op_type = type(node.op)
            if op_type in cls.ALLOWED_OPERATORS:
                return cls.ALLOWED_OPERATORS[op_type](left, right)
            raise ValueError(f"Unsupported operator: {op_type}")
        elif isinstance(node, ast.UnaryOp):
            operand = cls._eval_node(node.operand)
            op_type = type(node.op)
            if op_type in cls.ALLOWED_OPERATORS:
                return cls.ALLOWED_OPERATORS[op_type](operand)
            raise ValueError(f"Unsupported operator: {op_type}")
        else:
            raise ValueError(f"Unsupported syntax expression")
