# Makefile for jetvoice

# Load environment variables from .env
include .env
export

# Project config
IMAGE_NAME=jetvoice
CONTAINER_NAME=jetvoice_container
ENV_FILE=.env

# Init: download STT model
init:
	@if [ ! -d "jetvoice/stt/models/$(VOSK_MODEL)" ]; then \
		echo "Model '$(VOSK_MODEL)' not found. Downloading..."; \
		mkdir -p jetvoice/stt/models; \
		wget -O /tmp/vosk.zip https://alphacephei.com/vosk/models/$(VOSK_MODEL).zip; \
		unzip /tmp/vosk.zip -d jetvoice/stt/models; \
		rm /tmp/vosk.zip; \
	else \
		echo "Model '$(VOSK_MODEL)' already exists. Skipping download."; \
	fi

# Build Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run the container interactively (for debugging/development)
run:
	docker run --rm -it --name $(CONTAINER_NAME) $(IMAGE_NAME) bash

# Stop and remove container (if running in background mode)
down:
	-docker stop $(CONTAINER_NAME) && docker rm $(CONTAINER_NAME)

# Run container in background with volume mount (edit code live)
up:
	docker run -d \
		--env-file $(ENV_FILE) \
		--device /dev/snd \
		--privileged \
		--name $(CONTAINER_NAME) \
		-v $$(pwd):/app \
		$(IMAGE_NAME)

# Clean Docker stuff
clean:
	-docker rm -f $(CONTAINER_NAME)
	-docker rmi -f $(IMAGE_NAME)

# Check container logs
logs:
	docker logs -f $(CONTAINER_NAME)

# Format Python code
format:
	black jetvoice

# Run linters
lint:
	pylint jetvoice

test:
	pytest tests

# Down -> Build -> Up -> Logs
dbul: down build up logs

# Restart: Down -> Up -> Logs
restart: down up logs

.PHONY: init build run down up clean logs format lint
