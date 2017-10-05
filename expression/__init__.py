"""
Expression parser.

Copyright 2017 Leon Helwerda

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

# pylint: disable=invalid-name

# Use Python 3 division
from __future__ import division
import ast

__all__ = ['Expression_Parser']
__version__ = '0.0.2'

class Expression_Parser(ast.NodeVisitor):
    """
    Transformer that safely parses an expression, disallowing any complicated
    functions or control structures (inline if..else is allowed though).
    """

    # Boolean operators
    # The AST nodes may have multiple ops and right comparators, but we
    # evaluate each op individually.
    _boolean_ops = {
        ast.And: lambda left, right: left and right,
        ast.Or: lambda left, right: left or right
    }

    # Binary operators
    _binary_ops = {
        ast.Add: lambda left, right: left + right,
        ast.Sub: lambda left, right: left - right,
        ast.Mult: lambda left, right: left * right,
        ast.Div: lambda left, right: left / right,
        ast.Mod: lambda left, right: left % right,
        ast.Pow: lambda left, right: left ** right,
        ast.LShift: lambda left, right: left << right,
        ast.RShift: lambda left, right: left >> right,
        ast.BitOr: lambda left, right: left | right,
        ast.BitXor: lambda left, right: left ^ right,
        ast.BitAnd: lambda left, right: left & right,
        ast.FloorDiv: lambda left, right: left // right
    }

    # Unary operators
    _unary_ops = {
        ast.Invert: lambda operand: ~operand,
        ast.Not: lambda operand: not operand,
        ast.UAdd: lambda operand: +operand,
        ast.USub: lambda operand: -operand
    }

    # Comparison operators
    # The AST nodes may have multiple ops and right comparators, but we
    # evaluate each op individually.
    _compare_ops = {
        ast.Eq: lambda left, right: left == right,
        ast.NotEq: lambda left, right: left != right,
        ast.Lt: lambda left, right: left < right,
        ast.LtE: lambda left, right: left <= right,
        ast.Gt: lambda left, right: left > right,
        ast.GtE: lambda left, right: left >= right,
        ast.Is: lambda left, right: left is right,
        ast.IsNot: lambda left, right: left is not right,
        ast.In: lambda left, right: left in right,
        ast.NotIn: lambda left, right: left not in right
    }

    # Predefined variable names
    _variable_names = {
        'True': True,
        'False': False,
        'None': None
    }

    # Predefined functions
    _function_names = {
        'int': int,
        'float': float,
        'bool': bool
    }

    def __init__(self, variables=None, functions=None):
        if variables is None:
            self._variables = {}
        else:
            self._variables = variables

        variable_names = set(self._variables.keys())
        constant_names = set(self._variable_names.keys())
        forbidden_variables = variable_names.intersection(constant_names)
        if forbidden_variables:
            keyword = 'keyword' if len(forbidden_variables) == 1 else 'keywords'
            forbidden = ', '.join(forbidden_variables)
            raise NameError('Cannot override {} {}'.format(keyword, forbidden))

        if functions is None:
            self._functions = {}
        else:
            self._functions = functions

    def parse(self, expression, filename='<expression>'):
        """
        Parse a string `expression` and return its result.
        """

        try:
            return self.visit(ast.parse(expression))
        except SyntaxError as error:
            error.filename = filename
            error.text = expression
            raise error
        except Exception as error:
            error_type = error.__class__.__name__
            if len(error.args) > 2:
                line_col = error.args[1:]
            else:
                line_col = (1, 0)

            error = SyntaxError('{}: {}'.format(error_type, error.args[0]),
                                (filename,) + line_col + (expression,))
            raise error

    def generic_visit(self, node):
        """
        Visitor for nodes that do not have a custom visitor.

        This visitor denies any nodes that may not be part of the expression.
        """

        raise SyntaxError('Node {} not allowed'.format(ast.dump(node)),
                          ('', node.lineno, node.col_offset, ''))

    def visit_Module(self, node):
        """
        Visit the root module node.
        """

        if len(node.body) != 1:
            if len(node.body) > 1:
                lineno = node.body[1].lineno
                col_offset = node.body[1].col_offset
            else:
                lineno = 1
                col_offset = 0

            raise SyntaxError('Exactly one expression must be provided',
                              ('', lineno, col_offset, ''))

        return self.visit(node.body[0])

    def visit_Expr(self, node):
        """
        Visit an expression node.
        """

        return self.visit(node.value)

    def visit_BoolOp(self, node):
        """
        Visit a boolean expression node.
        """

        op = type(node.op)
        func = self._boolean_ops[op]
        result = func(self.visit(node.values[0]), self.visit(node.values[1]))
        for value in node.values[2:]:
            result = func(result, self.visit(value))

        return result

    def visit_BinOp(self, node):
        """
        Visit a binary expression node.
        """

        op = type(node.op)
        func = self._binary_ops[op]
        return func(self.visit(node.left), self.visit(node.right))

    def visit_UnaryOp(self, node):
        """
        Visit a unary expression node.
        """

        op = type(node.op)
        func = self._unary_ops[op]
        return func(self.visit(node.operand))

    def visit_IfExp(self, node):
        """
        Visit an inline if..else expression node.
        """

        return self.visit(node.body) if self.visit(node.test) else self.visit(node.orelse)

    def visit_Compare(self, node):
        """
        Visit a comparison expression node.
        """

        result = self.visit(node.left)
        for operator, comparator in zip(node.ops, node.comparators):
            op = type(operator)
            func = self._compare_ops[op]
            result = func(result, self.visit(comparator))

        return result

    def visit_Call(self, node):
        """
        Visit a function call node.
        """

        name = node.func.id
        if name in self._functions:
            func = self._functions[name]
        elif name in self._function_names:
            func = self._function_names[name]
        else:
            raise NameError("Function '{}' is not defined".format(name),
                            node.lineno, node.col_offset)

        args = [self.visit(arg) for arg in node.args]
        keywords = dict([self.visit(keyword) for keyword in node.keywords])

        if node.starargs is not None or node.kwargs is not None:
            raise SyntaxError('Star arguments are not supported',
                              ('', node.lineno, node.col_offset, ''))

        return func(*args, **keywords)

    def visit_keyword(self, node):
        """
        Visit a function keyword argument node.
        """

        return (node.arg, self.visit(node.value))

    def visit_Num(self, node):
        """
        Visit a literal number node.
        """

        # pylint: disable=no-self-use
        return node.n

    def visit_Name(self, node):
        """
        Visit a named variable node.
        """

        if node.id in self._variables:
            return self._variables[node.id]

        if node.id in self._variable_names:
            return self._variable_names[node.id]

        raise NameError("Name '{}' is not defined".format(node.id),
                        node.lineno, node.col_offset)

    def visit_NameConstant(self, node):
        """
        Visit a named constant singleton node (Python 3).
        """

        # pylint: disable=no-self-use
        return node.value
