#!/bin/bash

# Build React app
cd client
npm install
npm run build

# Copy to root static folder
cd ..
mkdir -p static
cp -r client/build/* static/

# Install Python deps
pip install -r requirements.txt
