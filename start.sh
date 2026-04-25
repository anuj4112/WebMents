#!/bin/bash
# WebMents Python Backend Startup Script
# Author: Anuj Singla (2210991317)

echo "============================================================"
echo "WebMents Python Backend - Quick Start"
echo "============================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo ""

# Install/Update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo ""

# Check if MongoDB is running
echo "Checking MongoDB..."
if command -v brew &> /dev/null; then
    # macOS
    brew services start mongodb-community 2>/dev/null || echo "MongoDB already running or not installed via brew"
elif command -v systemctl &> /dev/null; then
    # Linux
    sudo systemctl start mongod 2>/dev/null || echo "MongoDB already running or not installed"
fi
echo ""

# Start the server
echo "============================================================"
echo "Starting WebMents Server..."
echo "============================================================"
echo ""
python3 run.py
