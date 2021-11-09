PIPENV := $(shell command -v pipenv 2> /dev/null)

ifndef PIPENV
    $(error "Pipenv is not installed! See README.md")
endif


.PHONY: init play test pipeline-dev

export PIPENV_IGNORE_VIRTUALENVS=1
export PYTHONPATH=./src

init:
	pipenv install --dev

play:
	pipenv run python ./src/main.py

test:
	pipenv run pytest tests

pipeline-dev:
	@echo Running What A Pipeline Would Run
	@echo Delete all old test files
	rm -f .coverage
	rm -rf ./test-reports
	mkdir -p test-reports/{bandit,flake8,coverage,coverage/html,coverage/xml,pylint,pytest}

	@echo Running Flake8
	pipenv run flake8 ./src --exit-zero --format=html --htmldir=test-reports/flake8/

	@echo "Running pylint"
	pipenv run pylint --output-format=json ./src > test-reports/pylint/pylint.json || exit 0
	pipenv run pylint-json2html -o test-reports/pylint/pylint.html test-reports/pylint/pylint.json

	# @echo "Running bandit security check"
	# pipenv run bandit -r --exclude='venv,./src/z_*,./src/mock*' --format=html --output=./test-reports/bandit/index.html ./src

	@echo "Running tests"
	pipenv run coverage run -m pytest --html=test-reports/pytest/index.html --self-contained-html --junitxml=test-reports/pytest/junit.xml
	# # coverage report

	@echo "Creating HTML coverage report"
	pipenv run coverage html || exit 0

	@echo "Creating XML coverage report"
	pipenv run coverage xml