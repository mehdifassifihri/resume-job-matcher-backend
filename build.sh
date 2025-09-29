#!/bin/bash
# Build script for Render deployment
# This script handles potential Rust compilation issues

echo "Starting build process..."

# Set environment variables to help with compilation
export CARGO_HOME=/tmp/cargo
export RUSTUP_HOME=/tmp/rustup

# Install dependencies with specific flags to avoid Rust issues
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt

echo "Build completed successfully!"
