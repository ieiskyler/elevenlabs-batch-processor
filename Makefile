.PHONY: help install test lint format clean dev-install

help:
	@echo "Available commands:"
	@echo "  install     - Install package dependencies"
	@echo "  dev-install - Install package with development dependencies"
	@echo "  test        - Run tests with coverage"
	@echo "  lint        - Run linting checks"
	@echo "  format      - Format code with black"
	@echo "  clean       - Clean up temporary files"
	@echo "  setup       - Set up development environment"

install:
	pip install -r requirements.txt

dev-install:
	pip install -e ".[dev]"

test:
	pytest

lint:
	flake8 src tests
	mypy src

format:
	black src tests

clean:
	rm -rf __pycache__ .pytest_cache .coverage htmlcov
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

setup: dev-install
	cp .env.example .env
	@echo "Setup complete! Please edit .env with your API key."
