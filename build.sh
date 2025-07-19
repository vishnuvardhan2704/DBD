#!/usr/bin/env bash
# Build script for Render.com

set -e  # Exit on any error

echo "🚀 Starting Render.com deployment..."

# Ensure we're in the correct directory
cd "$(dirname "$0")"

# Build frontend
echo "📦 Building frontend..."
cd frontend
npm ci --only=production
npm run build

# Move built files to api/static for serving
echo "📁 Moving build files..."
cd ..
mkdir -p api/static
cp -r frontend/build/* api/static/

# Install backend dependencies
echo "🐍 Installing backend dependencies..."
cd api
pip install --no-cache-dir -r requirements.txt

echo "✅ Build complete!"
echo "📁 Static files are in api/static/"
echo "🚀 Ready to start the application!"
