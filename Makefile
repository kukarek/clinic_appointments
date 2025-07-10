.PHONY: up down lint test

up:
	docker compose up -d --build

down:
	docker compose down

lint:
	black app tests && isort app tests && flake8 app tests

test:
	pytest tests/
test-coverage:
	pytest --cov=app --cov-report=html tests