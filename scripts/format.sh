#!/bin/bash

echo "Formatting code..."

# Format with ruff
echo "🎨 Running ruff format..."
uv run ruff format src/ tests/

# Sort imports with ruff
echo "🎨 Sorting imports with ruff..."
uv run ruff check --select I --fix src/ tests/

echo "✅ Formatting complete!"