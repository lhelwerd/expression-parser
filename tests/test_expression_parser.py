"""
Tests for the expression parser.

Copyright 2017-2018 Leon Helwerda

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

import unittest

import expression


class Expression_Parser_Test(unittest.TestCase):
    """Tests for the expression parser."""

    # pylint: disable=too-many-public-methods

    def setUp(self):
        super(Expression_Parser_Test, self).setUp()
        variables = {"data": [1, 2, 3]}
        functions = {"square": lambda x, y=2: x**y}
        self.parser = expression.Expression_Parser(
            variables=variables, functions=functions
        )

    def assertRaisesError(self, regex=None, exception=SyntaxError):
        if regex is None:
            return self.assertRaises(exception)
        if hasattr(self, "assertRaisesRegex"):
            return self.assertRaisesRegex(exception, regex)
        return self.assertRaisesRegexp(exception, regex)  # Python 2.7 fallback

    def test_and(self):
        self.assertFalse(self.parser.parse("True and False"))
        self.assertEqual(self.parser.parse("1 and 2 and 3"), 3)

    def test_or(self):
        self.assertTrue(self.parser.parse("True or False"))
        self.assertEqual(self.parser.parse("1 or 2 or 3"), 1)

    def test_add(self):
        self.assertEqual(self.parser.parse("1+2"), 3)

    def test_sub(self):
        self.assertEqual(self.parser.parse("2-1"), 1)

    def test_mult(self):
        self.assertEqual(self.parser.parse("2*2.5"), 5)

    def test_div(self):
        self.assertIsInstance(self.parser.parse("1/2"), float)
        self.assertEqual(self.parser.parse("4/2"), 2.0)

    def test_mod(self):
        self.assertEqual(self.parser.parse("3%2"), 1)

    def test_pow(self):
        self.assertEqual(self.parser.parse("3**2"), 9)

    def test_lshift(self):
        self.assertEqual(self.parser.parse("1<<2"), 0b100)

    def test_rshift(self):
        self.assertEqual(self.parser.parse("0b100>>2"), 0b001)

    def test_bitor(self):
        self.assertEqual(self.parser.parse("0b100 | 0b101"), 0b101)

    def test_bitxor(self):
        self.assertEqual(self.parser.parse("0b011 ^ 0b111"), 0b100)

    def test_bitand(self):
        self.assertEqual(self.parser.parse("0b110 & 0b011"), 0b010)

    def test_floordiv(self):
        self.assertIsInstance(self.parser.parse("1//2.0"), float)
        self.assertEqual(self.parser.parse("3//2.0"), 1)

    def test_invert(self):
        self.assertEqual(self.parser.parse("~0b011"), -0b100)

    def test_not(self):
        self.assertFalse(self.parser.parse("not True"))

    def test_uadd(self):
        self.assertEqual(self.parser.parse("+1"), 1)

    def test_usub(self):
        self.assertEqual(self.parser.parse("-1"), -1)

    def test_eq(self):
        self.assertFalse(self.parser.parse("0 == 1"))

    def test_noteq(self):
        self.assertTrue(self.parser.parse("2 != 3"))

    def test_chained_comparisons(self):
        self.assertTrue(self.parser.parse("1 < 2 < 3"))
        self.assertFalse(self.parser.parse("1 < 2 > 3"))
        self.assertTrue(self.parser.parse("1 == 1 < 2"))

    def test_lt(self):
        self.assertFalse(self.parser.parse("3 < 3"))

    def test_boolean_short_circuit(self):
        self.assertEqual(self.parser.parse("0 and unknown"), 0)
        self.assertEqual(self.parser.parse("1 or unknown"), 1)

    def test_lte(self):
        self.assertTrue(self.parser.parse("3 <= 3"))

    def test_gt(self):
        self.assertFalse(self.parser.parse("3 > 3"))

    def test_gte(self):
        self.assertTrue(self.parser.parse("3 >= 3"))

    def test_is(self):
        self.assertFalse(self.parser.parse("0 is False"))

    def test_isnot(self):
        self.assertTrue(self.parser.parse("False is not True"))

    def test_in(self):
        self.assertFalse(self.parser.parse("0 in data"))

    def test_notin(self):
        self.assertTrue(self.parser.parse("0 not in data"))

    def test_ifelse(self):
        self.assertEqual(self.parser.parse("0 if True else 1"), 0)
        self.assertEqual(self.parser.parse("0.5 if 1 > 2 else 1.5"), 1.5)

    def test_known_variables(self):
        with self.assertRaisesError(
            "Cannot override keyword True", exception=NameError
        ):
            expression.Expression_Parser(variables={"True": 42})
        parser = expression.Expression_Parser()
        self.assertIsNone(parser.parse("None"))
        with self.assertRaisesError("NameError: Name 'test' is not defined"):
            parser.parse("test")

    def test_functions(self):
        self.assertEqual(self.parser.parse("int(4.2)"), 4)
        self.assertEqual(self.parser.parse("square(4)"), 16)
        self.assertEqual(self.parser.parse("square(3, 3)"), 27)
        self.assertEqual(self.parser.parse("square(2, y=3)"), 8)
        parser = expression.Expression_Parser(functions={"x2": lambda: 2})
        with self.assertRaisesError("NameError: Function 'x1' is not defined"):
            parser.parse("x1()")
        with self.assertRaisesError(r"TypeError: .* takes (no|0.*) arguments"):
            parser.parse("x2(1,2,3)")
        with self.assertRaisesError("Star arguments are not supported"):
            parser.parse("x2(1, *data)")

    def test_starstar_kwargs_not_supported(self):
        with self.assertRaisesError("Star arguments are not supported"):
            self.parser.parse("int(**{'x': 1})")

    def test_attribute_access_disallowed(self):
        with self.assertRaisesError(r"Node .* not allowed"):
            self.parser.parse("data.append")

    def test_parenthesized_function_call_allowed(self):
        self.assertEqual(self.parser.parse("(int)(4.2)"), 4)

    def test_call_requires_direct_function_name(self):
        with self.assertRaisesError("Only direct function names are allowed"):
            self.parser.parse("(lambda x: x)(3)")
        with self.assertRaisesError("Only direct function names are allowed"):
            self.parser.parse("int.__call__(5)")

    def test_disallowed(self):
        with self.assertRaisesError(r"Node .* not allowed"):
            self.parser.parse("while True: pass")
        with self.assertRaisesError("Exactly one expression must be provided"):
            self.parser.parse("")
        with self.assertRaisesError("Exactly one expression must be provided"):
            self.parser.parse("1;2")

    def test_variables(self):
        self.assertEqual(self.parser.variables, {"data": [1, 2, 3]})
        self.parser.variables = {"x": 42, "y": 1.3}
        self.assertEqual(self.parser.variables, {"x": 42, "y": 1.3})

    def test_assignment(self):
        self.assertFalse(self.parser.assignment)
        with self.assertRaisesError("Assignments are not allowed"):
            self.parser.parse("a = 1")
        with self.assertRaisesError("Assignments are not allowed"):
            self.parser.parse("foo += 1")
        self.parser.assignment = True
        with self.assertRaisesError(r"Multiple-target .* not supported"):
            self.parser.parse("a = b = 3")
        with self.assertRaisesError(r"Assignment target must be a variable .*"):
            self.parser.parse("a,b = 2")
        with self.assertRaisesError(r"Assignment target must be a variable .*"):
            self.parser.parse("data[1] *= 2")
        with self.assertRaisesError(r"Assignment name .* is not defined"):
            self.parser.parse("test /= 123")
        self.parser.parse("a = 1")
        self.assertEqual(self.parser.modified_variables, {"a": 1})
        self.assertEqual(self.parser.used_variables, set())
        self.parser.variables = {"b": 1}
        self.parser.parse("b += 5")
        self.assertEqual(self.parser.modified_variables, {"b": 6})
        self.assertEqual(self.parser.used_variables, set())

    def test_used_variables(self):
        self.assertEqual(self.parser.used_variables, set())
        self.parser.parse("1")
        self.assertEqual(self.parser.used_variables, set())
        self.parser.parse("data")
        self.assertEqual(self.parser.used_variables, set(["data"]))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
