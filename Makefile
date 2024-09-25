.DEFAULT_GOAL := help
.PHONY: help run rebuild clean migrate makemigrations

define docker_compose_cmd
	if command -v docker compose >/dev/null 2>&1; then \
		docker compose $(1); \
	elif command -v docker-compose >/dev/null 2>&1; then \
		docker-compose $(1); \
	else \
		echo "Error: Neither 'docker compose' nor 'docker-compose' command found."; \
		exit 1; \
	fi
endef

help:
	@echo "Makefile Help:"
	@echo
	@echo "This Makefile provides various commands for building, running, and managing a Django server with Docker and database migrations."
	@echo
	@echo "Available commands:"
	@echo
	@echo "  help                     : Display this help message"
	@echo "  run                      : Run the Django server"
	@echo "  rebuild                  : Rebuild Images and Run the Django server"
	@echo "  clean                    : Clean docker compose images and volumes for a fresh start"
	@echo "  migrate                  : Apply all pending migrations for db"
	@echo "  makemigrations           : Create new migrations (Optionally accept app name)"
	@echo
	@echo "Usage:"
	@echo "  make [command]"
	@echo
	@echo "Example:"
	@echo "  make run"
	@echo "  make rebuild"
	@echo "  make migrate"
	@echo "  make makemigrations app=users"
	@echo

run:
	@$(call docker_compose_cmd,up)

rebuild:
	@$(call docker_compose_cmd,up --build)

clean:
	@echo "Warning: This will remove all Docker containers, images, and volumes associated with this project."
	@echo "You will lose all database data. Are you sure you want to continue? (y/N)"
	@read -p "" response; \
	if [ "$$response" = "y" ] || [ "$$response" = "Y" ]; then \
		$(call docker_compose_cmd,down -v); \
		echo "Clean completed."; \
	else \
		echo "Clean aborted."; \
	fi

migrate:
	@echo "Ensuring containers are running..."
	@if docker ps | grep -q social-network-api-1; then \
		echo "Containers are already running."; \
	else \
		echo "Starting containers..."; \
		$(call docker_compose_cmd,up -d); \
	fi; \
	docker exec -it social-network-api-1 python manage.py migrate; \
	echo "Stopping containers..."; \
	$(call docker_compose_cmd,stop);

makemigrations:
	@echo "Ensuring containers are running..."
	@if docker ps | grep -q social-network-api-1; then \
		echo "Containers are already running."; \
	else \
		echo "Starting containers..."; \
		$(call docker_compose_cmd,up -d); \
	fi; \
	if [ -n "$(app)" ]; then \
		docker exec -it social-network-api-1 python manage.py makemigrations $(app); \
	else \
		docker exec -it social-network-api-1 python manage.py makemigrations; \
	fi; \
	echo "Stopping containers..."; \
	$(call docker_compose_cmd,stop);
