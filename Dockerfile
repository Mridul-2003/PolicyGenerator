FROM ubuntu:22.04

# system dependencies install karo
RUN apt-get update && apt-get install -y \
    curl \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# install ollama
RUN curl -fsSL https://ollama.ai/install.sh | sh

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy your application code
COPY . .

# Create a script to start both Ollama and Flask
RUN echo '#!/bin/bash\nollama serve &\nsleep 10\npython3 policy_error.py' > start.sh
RUN chmod +x start.sh

# Expose the port your Flask app runs on
EXPOSE 8000

# Start both Ollama and Flask
CMD ["./start.sh"]