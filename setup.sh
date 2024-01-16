#!/bin/bash

chmod +x setup.sh

# Version
PYTHON_VERSION="3.11"

# Check if Python is installed
if ! command -v "python$PYTHON_VERSION" &> /dev/null; then
    echo "Python$PYTHON_VERSION is not installed. Please install Python$PYTHON_VERSION before running this script."
    exit 1
fi

# Create a virtual environment
python$PYTHON_VERSION -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Display a message indicating successful setup
echo "Virtual environment created and dependencies installed successfully."
echo "Activate the virtual environment using: source venv/bin/activate"
