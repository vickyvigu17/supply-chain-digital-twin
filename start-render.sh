#!/bin/bash
echo "=== Starting Supply Chain Digital Twin on Render ==="

# Install Python dependencies
pip install -r requirements.txt

# Build React frontend
cd client
npm install
npm run build
cd ..

# Copy React build to static
rm -rf static
mkdir -p static
cp -r client/build/* static/

# Start FastAPI server
python -m uvicorn main:app --host 0.0.0.0 --port $PORT
