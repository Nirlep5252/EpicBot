#!/bin/bash

echo "Running linting checks..."

# Run ruff linting
echo "🔍 Running ruff check..."
uv run ruff check src/ tests/

echo "✅ Linting complete!"