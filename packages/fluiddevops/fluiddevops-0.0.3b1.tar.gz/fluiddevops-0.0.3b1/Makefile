
help:
	@echo "targets: develop and install"

develop:
	python setup.py develop

install:
	python setup.py install

clean_pyc:
	find fluiddevops -name "*.pyc" -delete
	find fluiddevops -name "__pycache__" -type d | xargs rm -rf

clean: clean_pyc
	rm -rf build dist

deploy: clean
	python setup.py sdist
	python setup.py bdist_wheel
	twine upload dist/*

tests:
	python -m unittest discover -v

_tests_coverage:
	mkdir -p .coverage
	coverage run -m unittest discover

_report_coverage:
	coverage report
	coverage html
	coverage xml
	@echo "Code coverage analysis complete. View detailed report:"
	@echo "file://${PWD}/.coverage/index.html"

coverage: _tests_coverage _report_coverage
