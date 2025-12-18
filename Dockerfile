FROM python:3.11-slim

# Create a non-root user and group
RUN groupadd -r app && useradd -r -g app -m -d /home/app app

WORKDIR /app

# Install minimal build deps only when needed; keep image small
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first for better layer caching
COPY --chown=app:app requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application files
COPY --chown=app:app fitgraph_complete_integration.py /app/fitgraph_complete_integration.py
COPY --chown=app:app README.md /app/README.md

# Switch to non-root user
USER app

# Default run: non-interactive demo
ENTRYPOINT ["python3", "/app/fitgraph_complete_integration.py"]
CMD ["--auto"]
