#!/bin/bash
set -e

echo "Setting up MCP Client project environment..."

# Check if UV is installed
if ! command -v uv &> /dev/null
then
    echo "Installing UV package manager..."
    pip install uv
fi

# Create virtual environment
echo "Creating virtual environment..."
uv venv

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
uv pip install -r requirements.txt

echo "Setup complete! To activate the environment, run:"
echo "source .venv/bin/activate"
echo
echo "To run the API server:"
echo "python app.py"
echo
echo "To run the CLI client:"
echo "python cli.py <MCP_SERVER_URL>"