#!/bin/bash
# Build script that avoids Rust compilation issues

echo "Starting build with Rust avoidance..."

# Set environment variables to avoid Rust compilation
export CARGO_HOME=/tmp/cargo
export RUSTUP_HOME=/tmp/rustup
export PIP_NO_BUILD_ISOLATION=1
export PIP_NO_CACHE_DIR=1

# Upgrade pip first
pip install --upgrade pip

# Install with specific flags to avoid compilation
pip install --only-binary=all --no-deps -r requirements-ultra-minimal.txt

# If that fails, try with individual packages
if [ $? -ne 0 ]; then
    echo "Trying individual package installation..."
    pip install --only-binary=all fastapi==0.104.1
    pip install --only-binary=all uvicorn==0.24.0
    pip install --only-binary=all openai==1.3.7
    pip install --only-binary=all pydantic==2.5.0
    pip install --only-binary=all python-dotenv==1.0.0
    pip install --only-binary=all python-multipart==0.0.6
fi

echo "Build completed!"
