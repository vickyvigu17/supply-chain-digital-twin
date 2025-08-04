#!/bin/bash

# Build React app
cd client
npm install
npm run build

# Copy build files to backend static folder
cd ..
mkdir -p backend/static
cp -r client/build/* backend/static/

# Install Python dependencies
cd backend
pip install -r requirements.txt
