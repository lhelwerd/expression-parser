# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and we adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Implement true short-circuit for 'and'/'or' returning deciding operand
- Make chained comparisons evaluate pairwise with short-circuit
- Restrict function calls to direct names only (reject attribute/lambda)

### Fixed

- Add `visit_Constant` for Python 3.8+ unified literals support

## [0.0.5] - 2018-01-29

### Added

- Support simple (augmented) assignment operations like `variable = expression` 
  and `variable += expression` via the `assignment` parameter and property, 
  with a `modified_variables` property
- Variable scope can be replaced
- Add interactive interpreter script entry point

### Changed

- Interpreter keeps context of variable scope
- Install script as `expression` instead of `expr` to avoid conflict
- Show only the expression line in the traceback

## [0.0.4] - 2017-10-05

### Added

- Track which variables are used in expression with a `used_variables` property

## [0.0.3] - 2017-10-05

### Fixed

- Correct Python 3.6+ starred arguments detection
- Disallow overriding predefined names `True`, `False` and `None`
- Always use float division for `/`

## [0.0.1] - 2017-10-05

### Added

- Initial version of expression parser

[Unreleased]: https://github.com/lhelwerd/expression-parser/compare/v0.0.5...HEAD
[0.0.5]: https://github.com/lhelwerd/expression-parser/releases/tag/v0.0.5
[0.0.4]: https://github.com/lhelwerd/expression-parser/releases/tag/v0.0.4
[0.0.3]: https://github.com/lhelwerd/expression-parser/releases/tag/v0.0.3
[0.0.1]: https://github.com/lhelwerd/expression-parser/releases/tag/v0.0.1
