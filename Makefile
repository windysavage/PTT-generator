.PHONY: clean test

help:
	@echo "    test"
	@echo "        Run unittest with coverage report in ./htmlcov"
	@echo "    freeze"
	@echo "        Freeze required pacakges into requirements files"
	@echo "    code-analyzer"
	@echo "        static code scanning for security issues finding"

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name __pycache__ -type d | xargs rm -rf
	find . -name .pytest_cache -type d | xargs rm -rf
	rm -rf ./htmlcov

freeze:
	pip list --format=freeze > requirements.txt

test: clean
	PYTHONPATH=./src python -m pytest tests -vv --cov ./src --cov-report=term --cov-report=html:./htmlcov --capture=no --log-cli-level=info --cov-config=.coveragerc

code-analyzer:
	bandit -r src -f html -o bandit.report.html
