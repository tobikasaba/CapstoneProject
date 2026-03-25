#!/bin/bash
echo "****************************************"
echo " Setting up Capstone Environment"
echo "****************************************"

echo "Checking the Python version..."
python3 --version

# Verify Python 3.10+
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if [[ "$(printf '%s\n' "3.10" "$PYTHON_VERSION" | sort -V | head -n1)" != "3.10" ]]; then
    echo "Error: Python 3.10 or higher is required. Found: $PYTHON_VERSION"
    exit 1
fi
echo "Python $PYTHON_VERSION detected - OK"

echo "Installing Python dependencies..."
pip install --upgrade pip wheel
pip install -r requirements.txt

echo "Checking Docker status..."
if command -v docker &> /dev/null; then
    docker ps
else
    echo "Docker not installed or not running"
fi

echo "****************************************"
echo " Capstone Environment Setup Complete"
echo "****************************************"