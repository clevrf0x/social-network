.DEFAULT_GOAL := help
.PHONY: help run rebuild clean migrate makemigrations createsuperuser createstaffuser

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
	@echo "  createsuperuser          : Create a superuser"
	@echo "  createstaffuser          : Create a staff user"
	@echo
	@echo "Usage:"
	@echo "  make [command]"
	@echo
	@echo "Example:"
	@echo "  make run"
	@echo "  make rebuild"
	@echo "  make migrate"
	@echo "  make makemigrations app=users"
	@echo "  make createsuperuser"
	@echo "  make createstaffuser"
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

createsuperuser:
	@echo "Creating a superuser..."
	@echo "Ensuring containers are running..."
	@if docker ps | grep -q social-network-api-1; then \
		echo "Containers are already running."; \
	else \
		echo "Starting containers..."; \
		$(call docker_compose_cmd,up -d); \
	fi; \
	docker exec -it social-network-api-1 python manage.py createsuperuser; \
	echo "Stopping containers..."; \
	$(call docker_compose_cmd,stop);

createstaffuser:
	@echo "Creating a staff user..."
	@echo "Ensuring containers are running..."
	@if docker ps | grep -q social-network-api-1; then \
		echo "Containers are already running."; \
	else \
		echo "Starting containers..."; \
		$(call docker_compose_cmd,up -d); \
	fi; \
	docker exec -it social-network-api-1 python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); email = input('Enter email for staff user: '); password = input('Enter password for staff user: '); User.objects.create_user(email=email, password=password, is_staff=True); print('Staff user created successfully.')"; \
	echo "Stopping containers..."; \
	$(call docker_compose_cmd,stop);
