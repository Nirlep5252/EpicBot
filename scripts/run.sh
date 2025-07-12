#!/bin/bash

# Start PostgreSQL database
echo "Starting PostgreSQL database..."
docker-compose up -d postgres

# Wait for database to be ready
echo "Waiting for database to be ready..."
sleep 3

# Run EpicBot
echo "Starting EpicBot..."
PYTHONPATH=src uv run python src/epicbot/main.py