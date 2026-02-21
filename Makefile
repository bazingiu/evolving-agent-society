.PHONY: help up down build test lint format fix graph

help:
	@echo "Available commands:"
	@echo "  up      : Start the containers"
	@echo "  build   : Build and start the containers"
	@echo "  down    : Stop the containers"
	@echo "  test    : Run pytest"
	@echo "  graph   : Print the langgraph"
	@echo "  run     : Run a specific python script (e.g. make run script=scripts/run_local.py)"

up:
	docker compose -f .docker/docker-compose.yml up

build:
	docker compose -f .docker/docker-compose.yml up --build

down:
	docker compose -f .docker/docker-compose.yml down

test:
	docker compose -f .docker/docker-compose.yml run --rm agent pytest

graph:
	docker compose -f .docker/docker-compose.yml run --rm agent python src/print_graph.py

run:
	docker compose -f .docker/docker-compose.yml run --rm agent python $(script)
