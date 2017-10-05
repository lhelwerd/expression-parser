"""
Package module for the expression parser tests.

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

__all__ = ['Expression_Parser_Test']

import unittest
import expression

class Expression_Parser_Test(unittest.TestCase):
    """
    Tests for the expression parser.
    """

    # pylint: disable=too-many-public-methods

    def setUp(self):
        super(Expression_Parser_Test, self).setUp()
        variables = {
            'data': [1, 2, 3]
        }
        functions = {
            'square': lambda x, y=2: x ** y
        }
        self.parser = expression.Expression_Parser(variables=variables,
                                                   functions=functions)

    def assertRaisesError(self, regex=None, exception=SyntaxError):
        """
        Check that an exception is raised from a context manager body.

        If `regex` is `None`, then only the exception type is tested, otherwise
        the this also tests if `regex` matches the exception message.
        The `exception` type by default is `SyntaxError`.
        """

        # pylint: disable=invalid-name,no-member

        if regex is None:
            return self.assertRaises(exception)

        if hasattr(self, 'assertRaisesRegex'):
            return self.assertRaisesRegex(exception, regex)

        # Python 2.7
        return self.assertRaisesRegexp(exception, regex)

    def test_and(self):
        """
        Test the 'and' boolean operator.
        """

        self.assertFalse(self.parser.parse('True and False'))
        self.assertEqual(self.parser.parse('1 and 2 and 3'), 3)

    def test_or(self):
        """
        Test the 'or' boolean operator.
        """

        self.assertTrue(self.parser.parse('True or False'))
        self.assertEqual(self.parser.parse('1 or 2 or 3'), 1)

    def test_add(self):
        """
        Test the '+' addition binary operator.
        """

        self.assertEqual(self.parser.parse('1+2'), 3)

    def test_sub(self):
        """
        Test the '-' subtraction binary operator.
        """

        self.assertEqual(self.parser.parse('2-1'), 1)

    def test_mult(self):
        """
        Test the '*' multiplication binary operator.
        """

        self.assertEqual(self.parser.parse('2*2.5'), 5)

    def test_div(self):
        """
        Test the '/' division binary operator.
        """

        self.assertIsInstance(self.parser.parse('1/2'), float)
        self.assertEqual(self.parser.parse('4/2'), 2.0)

    def test_mod(self):
        """
        Test the '%' modulo binary operator.
        """

        self.assertEqual(self.parser.parse('3%2'), 1)

    def test_pow(self):
        """
        Test the '**' power binary operator.
        """

        self.assertEqual(self.parser.parse('3**2'), 9)

    def test_lshift(self):
        """
        Test the '<<' left shift binary operator.
        """

        self.assertEqual(self.parser.parse('1<<2'), 0b100)

    def test_rshift(self):
        """
        Test the '>>' right shift binary operator.
        """

        self.assertEqual(self.parser.parse('0b100>>2'), 0b001)

    def test_bitor(self):
        """
        Test the '|' bitwise OR binary operator.
        """

        self.assertEqual(self.parser.parse('0b100 | 0b101'), 0b101)

    def test_bitxor(self):
        """
        Test the '^' bitwise XOR binary operator.
        """

        self.assertEqual(self.parser.parse('0b011 ^ 0b111'), 0b100)

    def test_bitand(self):
        """
        Test the '&' bitwise AND binary operator.
        """

        self.assertEqual(self.parser.parse('0b110 & 0b011'), 0b010)

    def test_floordiv(self):
        """
        Test the '//' floored division binary operator.
        """

        # Floored division respects the input types.
        self.assertIsInstance(self.parser.parse('1//2.0'), float)
        self.assertEqual(self.parser.parse('3//2.0'), 1)

    def test_invert(self):
        """
        Test the '~' bitwise inversion unary operator.
        """

        self.assertEqual(self.parser.parse('~0b011'), -0b100)

    def test_not(self):
        """
        Test the 'not' logical unary operator.
        """

        self.assertFalse(self.parser.parse('not True'))

    def test_uadd(self):
        """
        Test the '+' positive unary operator.
        """

        self.assertEqual(self.parser.parse('+1'), 1)

    def test_usub(self):
        """
        Test the '+' positive unary operator.
        """

        self.assertEqual(self.parser.parse('-1'), -1)

    def test_eq(self):
        """
        Test the '==' equality comparison operator.
        """

        self.assertFalse(self.parser.parse('0 == 1'))

    def test_noteq(self):
        """
        Test the '!=' inequality comparison operator.
        """

        self.assertTrue(self.parser.parse('2 != 3'))

    def test_lt(self):
        """
        Test the '<' less than comparison operator.
        """

        self.assertFalse(self.parser.parse('3 < 3'))

    def test_lte(self):
        """
        Test the '<=' less than or equals comparison operator.
        """

        self.assertTrue(self.parser.parse('3 <= 3'))

    def test_gt(self):
        """
        Test the '>' greater than comparison operator.
        """

        self.assertFalse(self.parser.parse('3 > 3'))

    def test_gte(self):
        """
        Test the '>=' greater than or equals comparison operator.
        """

        self.assertTrue(self.parser.parse('3 >= 3'))

    def test_is(self):
        """
        Test the 'is' equivalence comparison operator.
        """

        self.assertFalse(self.parser.parse('0 is False'))

    def test_isnot(self):
        """
        Test the 'is not' inequivalence comparison operator.
        """

        self.assertTrue(self.parser.parse('False is not True'))

    def test_in(self):
        """
        Test the 'in' set containment comparison operator.
        """

        self.assertFalse(self.parser.parse('0 in data'))

    def test_notin(self):
        """
        Test the 'not in' set exclusion comparison operator.
        """

        self.assertTrue(self.parser.parse('0 not in data'))

    def test_ifelse(self):
        """
        Test the 'if..else' inline conditional expression.
        """

        self.assertEqual(self.parser.parse('0 if True else 1'), 0)
        self.assertEqual(self.parser.parse('0.5 if 1 > 2 else 1.5'), 1.5)

    def test_variables(self):
        """
        Test whether known variables work and whether undefined variables raise
        exceptions.
        """

        with self.assertRaisesError('Cannot override keyword True',
                                    exception=NameError):
            parser = expression.Expression_Parser(variables={'True': 42})

        parser = expression.Expression_Parser()
        self.assertIsNone(parser.parse('None'))
        with self.assertRaisesError("NameError: Name 'test' is not defined"):
            parser.parse('test')

    def test_functions(self):
        """
        Test whether known functions work and whether undefined functions raise
        exceptions.
        """

        self.assertEqual(self.parser.parse('int(4.2)'), 4)
        self.assertEqual(self.parser.parse('square(4)'), 16)
        self.assertEqual(self.parser.parse('square(3, 3)'), 27)
        self.assertEqual(self.parser.parse('square(2, y=3)'), 8)

        parser = expression.Expression_Parser(functions={'x2': lambda: 2})
        with self.assertRaisesError("NameError: Function 'x1' is not defined"):
            parser.parse('x1()')

        with self.assertRaisesError(r"TypeError: .* takes (no|0.*) arguments"):
            parser.parse('x2(1,2,3)')

        with self.assertRaisesError("Star arguments are not supported"):
            parser.parse('x2(1, *data)')

    def test_disallowed(self):
        """
        Test whether disallowed syntax, such as control structures, raise
        exceptions.
        """

        with self.assertRaisesError("Node .* not allowed"):
            self.parser.parse('while True: pass')

        with self.assertRaisesError("Exactly one expression must be provided"):
            self.parser.parse('')

        with self.assertRaisesError("Exactly one expression must be provided"):
            self.parser.parse('1;2')
