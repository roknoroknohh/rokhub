# Makefile for ROKhub

.PHONY: help install run dev test clean docker-build docker-run

help:
	@echo "ROKhub - منصة الألعاب الرقمية"
	@echo ""
	@echo "Available commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make run          - Run production server"
	@echo "  make dev          - Run development server"
	@echo "  make test         - Run tests"
	@echo "  make clean        - Clean cache and temp files"
	@echo "  make init-db      - Initialize database"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run with Docker Compose"

install:
	pip install -r requirements.txt

run:
	gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app

dev:
	python app.py

test:
	python -m pytest tests/ -v

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.log" -delete
	rm -rf .pytest_cache

init-db:
	python -c "from app import app; from utils import init_database; app.app_context().push(); init_database()"

docker-build:
	docker build -t rokhub:latest .

docker-run:
	docker-compose up -d

docker-stop:
	docker-compose down
