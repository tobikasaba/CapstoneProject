#!/bin/bash
echo "****************************************"
echo " Setting up Capstone Environment"
echo "****************************************"

echo "Checking the Python version..."
python3 --version

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
