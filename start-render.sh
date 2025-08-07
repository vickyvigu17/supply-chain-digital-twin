#!/bin/bash
set -e

echo "🚀 RENDER DEPLOYMENT STARTING..."
echo "====================================="

# Install Python dependencies
echo "📦 Installing Python dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

# Install Node.js and build React app
echo "📦 Installing Node.js dependencies..."
cd client
npm install
echo "🔨 Building React app..."
npm run build
cd ..

# Copy built files to static directory
echo "📁 Copying static files..."
rm -rf static
mkdir -p static
cp -r client/build/* static/

# Verify our key fixes are in place
echo "✅ VERIFICATION:"
echo "  - Shipments with destinations array: $(grep -c 'destinations: List' main.py || echo 0)"
echo "  - 45 shipments generated: $(grep -c 'range(45)' main.py || echo 0)"
echo "  - React app built: $(ls -la static/index.html | wc -l)"

echo "====================================="
echo "🎉 RENDER BUILD COMPLETE!"
echo "====================================="