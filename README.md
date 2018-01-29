# Python sandboxed expression parser

[![PyPI](https://img.shields.io/pypi/v/expression-parser.svg)](https://pypi.python.org/pypi/expression-parser)
[![Build 
Status](https://travis-ci.org/lhelwerd/expression-parser.svg?branch=master)](https://travis-ci.org/lhelwerd/expression-parser)
[![Coverage 
Status](https://coveralls.io/repos/github/lhelwerd/expression-parser/badge.svg?branch=master)](https://coveralls.io/github/lhelwerd/expression-parser?branch=master)

This parser can calculate the results of a single simple expression,
disallowing any complicated functions or control structures, with support for
custom variable and function environment contexts.

## Features

- Support for all boolean, binary, unary, and comparative operators as in 
  Python itself.
- Support for inline `if..else` expressions.
- Support for assignments and augmented assignments like `+=`, only if enabled 
  explicitly.
- All other control structures and multiple expressions are disallowed.
- Isolation from execution context using a restricted scope.
- Separate scope for variables and functions to avoid abusing one or the other.
- Function calls may use specific keyword arguments.
- Errors from parsing or evaluating the expression are raised as `SyntaxError` 
  with appropriate context parameters to make error display easier (works with 
  default traceback output).
- A successful parse yields the result of the evaluated expression. Successful
  assignments of variables are stored in a property `modified_variables`.
  A separate property `used_variables` provides a set of variable names used in 
  the evaluation of the expression excluding the assignment targets.
- Supports both Python 2.7 and 3.6 AST syntax trees.
- Python 3+ conventions are used whenever possible: Specifically, the division 
  operator `/` always returns floats instead of integers, and `True`, `False` 
  and `None` are reserved named constants and cannot be overridden through the 
  variable scope in any version.

Not supported (often by design):

- Functions or lambdas defined within the expression.
- Control structures and other Python statements (`return`, `pass`, etc.).
- Comprehensions and generators.
- Multiple expressions or assignment targets in the same input string.
- Function calls that have variable positional or keyword (starred) arguments.
- Literals which are not integers, floats, or the named constants, nor any
  subscripting or indexing. You can still inject other types of variables using 
  the context, and add specialized functions to interact with them.

## Requirements

The expression parser has been tested to work on Python 2.7 and 3.6. This 
package has no other dependencies and works with only core Python modules.

## Installation

Install the latest version from PyPI using:

```
pip install expression-parser
```

## Functionality

First, import the library:

```python
import expression
```

Next, determine a variable and function scope. If you do not need any custom
variables and functions in your environment, you can skip this step. Otherwise,
create two dictionaries, each containing string identifier names as keys and
either variables or functions as values. For example, to create a scope with
a few mathematical constants and functions:

```python
import math
variables = {
    'pi': math.pi,
    'e': math.e
}
functions = {
    'log': math.log,
    'log10': math.log10,
    'exp': math.exp,
    'pow': math.pow,
    'sqrt': math.sqrt
}
```

Then create the parser, either by simply calling it with no additional 
arguments, such as `parser = expression.Expression_Parser()`, or by passing the 
scope along to it in dictionaries of values and functions, respectively:

```python
parser = expression.Expression_Parser(variables=variables, functions=functions,
                                      assignment=bool(assignment))
```

You can also set a new dictionary for `variables`, and enable or disable 
parsing of assignments in the expression using `assignment`, after construction 
via the properties of the created object.

Now you can use this parser to evaluate any valid expression:

```python
print(parser.parse('1+2'))
3
print(parser.parse('pi > 3'))
True
print(parser.parse('int(log(e))'))
1
```

## Development

- [Travis](https://travis-ci.org/lhelwerd/expression-parser) is used to run 
  unit tests and report on coverage.
- [Coveralls](https://coveralls.io/github/lhelwerd/expression-parser) receives 
  coverage reports and tracks them.
- You can perform local lint checks, tests and coverage during development 
  using `make pylint`, `make test` and `make coverage`, respectively.
- We publish releases to [PyPI](https://pypi.python.org/pypi/expression-parser) 
  using `make release` which performs lint and unit test checks.

## License

The expression parser library is licensed under the Apache 2.0 License.
