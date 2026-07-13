FROM python:3.11-slim

# Install Node.js (needed to run supergateway) and uv (needed to run the Python server)
RUN apt-get update && apt-get install -y curl ca-certificates && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app
COPY . .

# Install the Python project's dependencies
RUN uv sync

# Railway provides the PORT env var at runtime; supergateway must listen on it
CMD sh -c "npx -y supergateway --stdio 'uv run python main.py' --port ${PORT:-8000} --outputTransport streamableHttp --healthEndpoint /health"
