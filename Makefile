# Makefile for jetvoice

# Project config
IMAGE_NAME=jetvoice
CONTAINER_NAME=jetvoice_container

# Init: download STT model
init:
	mkdir -p jetvoice/stt/models \
	&& wget -O /tmp/vosk.zip https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip \
	&& unzip /tmp/vosk.zip -d jetvoice/stt/models \
	&& rm /tmp/vosk.zip

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
	docker run -d --name $(CONTAINER_NAME) \
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
	pytest tests || echo "No tests yet 😅"

# Down -> Build -> Up -> Logs
dbul: down build up logs

.PHONY: init build run down up clean logs format lint
