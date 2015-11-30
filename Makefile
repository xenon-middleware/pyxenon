.PHONY: all requirements test-requirements test-license test clean pyflakes pyflakes-exists unittest coverage fulltest install reinstall

PYTHON_FIND=find xenon scripts tests -name '*.py'
LICENSE_NAME="Apache License, Version 2.0"

all: install

requirements: requirements.txt
	@pip install -r requirements.txt

test-requirements: test_requirements.txt
	@pip install -r test_requirements.txt > /dev/null

install: requirements
	@pip install .
	
reinstall:
	@pip install --upgrade --no-deps .

test-license: LICENSE
	@echo "======= Check License ======"
	@test $(shell $(PYTHON_FIND) | xargs grep $(LICENSE_NAME) | wc -l) -eq $(shell $(PYTHON_FIND) | wc -l)

pyflakes:
	@echo "=======  PyFlakes  ========="
	@$(PYTHON_FIND) -exec pyflakes {} \;

pep8:
	@echo "=======   PEP8     ========="
	@$(PYTHON_FIND) -exec pep8 {} \;

unittest:
	@echo "======= Unit Tests ========="
	@nosetests

test: test-requirements test-license pyflakes pep8 unittest

coverage:
	@echo "======= Unit Tests ========="
	@nosetests --with-coverage --cover-package=xenon --cover-xml

fulltest: test-requirements test-license pyflakes pep8 coverage

clean: 
	rm -rf build/
	find . -name *.pyc -delete
	find . -name *.pyo -delete
	rm -rf tests/tmp
