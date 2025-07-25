FROM python:3.10-slim

# Install unzip
RUN apt-get update && apt-get install -y \
    build-essential \
    libasound2-dev \
    libportaudio2 \
    libportaudiocpp0 \
    ffmpeg \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy requirements and install python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Download and extract vosk
RUN mkdir -p jetvoice/stt/models \
    && wget -O /tmp/vosk.zip https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip \
    && unzip /tmp/vosk.zip -d jetvoice/stt/models \
    && rm /tmp/vosk.zip

# Copy project files
COPY jetvoice ./jetvoice
COPY .env .env

# Set environment variables (override as needed)
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Entrypoint
CMD ["python", "-m", "jetvoice.main"]
