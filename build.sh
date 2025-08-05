#!/bin/bash

echo "=== Starting build process ==="

# Install Python deps first
echo "Installing Python dependencies..."
python3 -m pip install -r requirements.txt

# Build React app
cd client
npm install
npm run build

# Show what was built
echo "React build contents:"
ls -la build/

# Copy to root static folder
cd ..
rm -rf static
mkdir -p static
cp -r client/build/* static/

# Show what was copied
echo "Static folder contents:"
ls -la static/

echo "=== Build complete ==="
