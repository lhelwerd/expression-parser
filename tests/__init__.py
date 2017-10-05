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

    def setUp(self):
        super(Expression_Parser_Test, self).setUp()
        self.parser = expression.Expression_Parser()

    def test_add(self):
        """
        Test the 'add' operator.
        """

        self.assertEqual(self.parser.parse('1+2'), 3)
