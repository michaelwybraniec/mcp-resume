#!/bin/bash

# Build script for MCP Resume Server on Streamlit Cloud
echo "🔨 Building MCP Resume Server..."

# Check if we're in the right directory
if [ ! -f "../package.json" ]; then
    echo "❌ Parent package.json not found. Make sure you're in the streamlit-client directory."
    exit 1
fi

# Go to parent directory (where the main TypeScript project is)
cd ..

# Install dependencies
echo "📦 Installing Node.js dependencies..."
npm install

# Build TypeScript
echo "🔧 Building TypeScript..."
npm run build

# Check if build was successful
if [ -f "build/index.js" ]; then
    echo "✅ MCP Server built successfully!"
    echo "📁 Server available at: build/index.js"
else
    echo "❌ Build failed!"
    exit 1
fi

echo "🎉 Build complete! You can now start the Streamlit app." 