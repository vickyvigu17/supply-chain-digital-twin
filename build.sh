#!/bin/bash

echo "=== Starting build process ==="

# Build React app
echo "Building React app..."
cd client
npm install
npm run build

# Show what was built
echo "React build contents:"
ls -la build/

# Copy build files to backend static folder
echo "Copying build files..."
cd ..
rm -rf backend/static
mkdir -p backend/static
cp -r client/build/* backend/static/

# Show what was copied
echo "Static folder contents:"
ls -la backend/static/

# Install Python dependencies
echo "Installing Python dependencies..."
cd backend
pip install -r requirements.txt

echo "=== Build complete ==="
