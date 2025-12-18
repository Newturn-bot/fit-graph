#!/usr/bin/env bash
# Small helper to build and run the Docker container on the server.
# Usage: copy files to server (Dockerfile, docker-compose.yml, requirements.txt,
# fitgraph_complete_integratio.py, .env) then run this script on the server.

set -eu

echo "Building and starting fitgraph container..."
# Build and start the service in detached mode
docker-compose up -d --build

echo "Done. To view logs: docker-compose logs -f"
