FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    curl \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://ollama.ai/install.sh | bash


WORKDIR /app


COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

RUN echo '#!/bin/bash' > /app/start.sh \
    && echo 'ollama serve &' >> /app/start.sh \
    && echo 'sleep 10' >> /app/start.sh \
    && echo 'python3 policy_error.py' >> /app/start.sh \
    && chmod +x /app/start.sh

EXPOSE 8000

CMD ["/app/start.sh"]
