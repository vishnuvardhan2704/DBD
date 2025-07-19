#!/usr/bin/env bash
# Build script for Render.com

set -e  # Exit on any error

echo "🚀 Starting Render.com deployment..."

# Build frontend
echo "📦 Building frontend..."
cd frontend

# Install frontend dependencies
echo "� Installing frontend dependencies..."
npm ci

# Build the React app
echo "🏗️ Building React app..."
npm run build

# Move built files to api/static for serving
echo "📁 Moving build files to api/static..."
cd ..
mkdir -p api/static
cp -r frontend/build/* api/static/

# Verify files were copied
echo "📋 Verifying static files..."
ls -la api/static/

# Install backend dependencies
echo "🐍 Installing backend dependencies..."
pip install --no-cache-dir -r requirements.txt

echo "✅ Build complete!"
echo "📁 Static files are in api/static/"
echo "🚀 Ready to start the application!"
