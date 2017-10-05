COVERAGE=coverage
TEST=-m unittest discover -s tests -p '*.py'

.PHONY: all
all: release

.PHONY: release
release: pylint test clean tag build push upload

.PHONY: setup
setup:
	pip install setuptools wheel

.PHONY: get_version
get_version:
	$(eval VERSION=v$(shell python setup.py --version))
	python setup.py --version

.PHONY: pylint
pylint:
	pylint *.py expression/*.py tests/*.py

.PHONY: tag
tag: get_version
	git tag $(VERSION)

.PHONY: build
build:
	python setup.py sdist
	python setup.py bdist_wheel --universal

.PHONY: push
push: get_version
	git push origin $(VERSION)

.PHONY: upload
upload:
	twine upload dist/*

.PHONY: test
test:
	python $(TEST)

.PHONY: coverage
coverage:
	$(COVERAGE) run $(TEST)
	$(COVERAGE) report -m

.PHONY: clean
clean:
	rm -rf build/ dist/ expression.egg-info .coverage
