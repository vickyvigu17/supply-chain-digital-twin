#!/bin/bash

echo "=== Starting Supply Chain Digital Twin ==="

# Install Python dependencies with --break-system-packages if needed
echo "Installing Python dependencies..."
python3 -m pip install -r requirements.txt --break-system-packages || python3 -m pip install -r requirements.txt

# Start the FastAPI server
echo "Starting FastAPI server on port 8000..."
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

echo "Application started! Visit http://localhost:8000"