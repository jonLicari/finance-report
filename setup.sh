#!/bin/bash

chmod +x setup.sh

# Version
PYTHON_PATH=$(command -v python3 || command -v python)

# Check if Python is installed
if [ -z "$PYTHON_PATH" ]; then
    echo "Python is not installed. Please install Python before running this script."
    exit 1
else
    echo "PYTHON_PATH is set to: $PYTHON_PATH"
fi

# Create a virtual environment
VENV_NAME="finance-script-env"

# Are we already in a virtual environment?
if [ -n "$VIRTUAL_ENV" ]; then
    deactivate

    # Remove the existing virtual environment directory
    rm -rf $VIRTUAL_ENV
fi

# Create & activate new virtual environment
$PYTHON_PATH -m venv $VENV_NAME --without-pip
source $VENV_NAME/bin/activate

# install pip
curl https://bootstrap.pypa.io/get-pip.py | python3
echo "$VENV_NAME created and active."

# Install dependencies from requirements.txt
pip3 install -r requirements.txt &>/dev/null

# Display a message indicating successful setup
echo "Virtual environment created and dependencies installed successfully."
