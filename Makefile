init: update install pre-commit

install:
	poetry install

update:
	poetry update

build:
	poetry build

pre-commit:
	poetry run pre-commit install

mypy:
	poetry run mypy macos_tags

test:
	poetry run pytest --exitfirst tests/
	poetry run pytest --cov --cov-fail-under=100

format:
	poetry run black macos_tags tests
	poetry run isort -y

clean:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	rm -f .coverage
	rm -fr .pytest_cache
	rm -fr .mypy_cache

ci:
	poetry run black --check macos_tags tests/
	poetry run mypy macos_tags
	poetry run pytest --exitfirst tests/
	poetry run pytest --cov --cov-fail-under=100
