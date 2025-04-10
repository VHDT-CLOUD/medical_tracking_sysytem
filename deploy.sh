#!/bin/bash

# Exit on error
set -e

echo "🚀 Starting deployment process..."

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Run tests
echo "🧪 Running tests..."
npm test

# Security audit
echo "🔒 Running security audit..."
npm audit

# Lint check
echo "📝 Running lint check..."
npm run lint

# Build frontend (if applicable)
echo "🏗️ Building frontend..."
# Add frontend build commands here if needed

# Set up environment
echo "🌍 Setting up environment..."
if [ "$1" == "production" ]; then
    export NODE_ENV=production
    echo "Production environment set"
else
    export NODE_ENV=development
    echo "Development environment set"
fi

# Start the application
echo "🚀 Starting application..."
if [ "$NODE_ENV" == "production" ]; then
    npm start
else
    npm run dev
fi 