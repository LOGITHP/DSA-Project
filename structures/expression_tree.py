"""
structures/expression_tree.py
Expression Tree for Supply Chain Logistics Cost & Tariff Evaluation.
Reads postfix expressions (e.g. "dist rate * toll + 2 /"), builds an expression tree,
evaluates numerical values, and prints minimal-parentheses infix expressions.

Handles:
- Operand shortage errors
- Unused operand errors
- Division by zero errors
- Minimal parentheses generation based on operator precedence and associativity
"""

from typing import Optional, Dict, Any, Tuple
from structures.common_utils import Stack


class ExpressionNode:
    def __init__(self, value: str, left: Optional['ExpressionNode'] = None, right: Optional['ExpressionNode'] = None):
        self.value: str = value
        self.left: Optional['ExpressionNode'] = left
        self.right: Optional['ExpressionNode'] = right

    def is_operator(self) -> bool:
        return self.value in {'+', '-', '*', '/', '^'}

    def is_leaf(self) -> bool:
        return self.left is None and self.right is None


class ExpressionTree:
    """
    Expression Tree for parsing, evaluating, and converting postfix formulas.
    """
    OPERATORS = {
        '+': {'prec': 1, 'assoc': 'L'},
        '-': {'prec': 1, 'assoc': 'L'},
        '*': {'prec': 2, 'assoc': 'L'},
        '/': {'prec': 2, 'assoc': 'L'},
        '^': {'prec': 3, 'assoc': 'R'},
    }

    def __init__(self, postfix_str: Optional[str] = None):
        self.root: Optional[ExpressionNode] = None
        self.postfix_expr: str = postfix_str or ""
        if postfix_str:
            self.build_from_postfix(postfix_str)

    def build_from_postfix(self, postfix: str) -> None:
        """
        Builds expression tree from a whitespace-separated postfix string.
        Raises ValueError on invalid expressions (shortage of operands, malformed tokens).
        """
        tokens = postfix.strip().split()
        if not tokens:
            raise ValueError("Expression cannot be empty")

        stack = Stack()
        for token in tokens:
            if token in self.OPERATORS:
                if stack.size() < 2:
                    raise ValueError(f"Invalid postfix expression: operand shortage for operator '{token}'")
                right = stack.pop()
                left = stack.pop()
                node = ExpressionNode(token, left, right)
                stack.push(node)
            else:
                # Operand (numeric or variable)
                stack.push(ExpressionNode(token))

        if stack.size() != 1:
            raise ValueError(f"Invalid postfix expression: {stack.size()} disconnected operands remaining (missing operators)")

        self.root = stack.pop()
        self.postfix_expr = postfix

    def evaluate(self, variable_map: Optional[Dict[str, float]] = None) -> float:
        """
        Evaluates the expression tree given a dictionary of variable values.
        Raises ZeroDivisionError on division by zero.
        Raises KeyError / ValueError if variable cannot be resolved.
        """
        if not self.root:
            raise ValueError("Tree is empty")

        variables = variable_map or {}

        def _eval_rec(node: ExpressionNode) -> float:
            if node.is_leaf():
                # Check if it's a direct float literal
                try:
                    return float(node.value)
                except ValueError:
                    if node.value in variables:
                        return float(variables[node.value])
                    raise KeyError(f"Undefined variable in formula: '{node.value}'")

            left_val = _eval_rec(node.left)
            right_val = _eval_rec(node.right)

            op = node.value
            if op == '+':
                return left_val + right_val
            elif op == '-':
                return left_val - right_val
            elif op == '*':
                return left_val * right_val
            elif op == '/':
                if abs(right_val) < 1e-12:
                    raise ZeroDivisionError(f"Division by zero encountered: {left_val} / {right_val}")
                return left_val / right_val
            elif op == '^':
                return left_val ** right_val
            else:
                raise ValueError(f"Unknown operator: '{op}'")

        return _eval_rec(self.root)

    def to_infix_minimal_parentheses(self) -> str:
        """
        Generates infix representation adding parentheses ONLY where mathematically necessary
        according to operator precedence and associativity rules.
        """
        if not self.root:
            return ""

        def _format(node: ExpressionNode) -> str:
            if node.is_leaf():
                return node.value

            parent_info = self.OPERATORS[node.value]
            parent_prec = parent_info['prec']

            # Left child
            left_str = _format(node.left)
            need_left_paren = False
            if node.left.is_operator():
                left_prec = self.OPERATORS[node.left.value]['prec']
                if left_prec < parent_prec:
                    need_left_paren = True
                elif left_prec == parent_prec and parent_info['assoc'] == 'R':
                    need_left_paren = True
            if need_left_paren:
                left_str = f"({left_str})"

            # Right child
            right_str = _format(node.right)
            need_right_paren = False
            if node.right.is_operator():
                right_prec = self.OPERATORS[node.right.value]['prec']
                if right_prec < parent_prec:
                    need_right_paren = True
                elif right_prec == parent_prec:
                    # Non-associative or sensitive cases
                    if parent_info['assoc'] == 'L':
                        if node.value in {'-', '/'}:
                            need_right_paren = True
            if need_right_paren:
                right_str = f"({right_str})"

            return f"{left_str} {node.value} {right_str}"

        return _format(self.root)

