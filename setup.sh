#!/bin/bash

chmod +x setup.sh

# Version
PYTHON_PATH=$(command -v python3 || command -v python)

# Check if Python is installed
if [ -z "$PYTHON_PATH" ]; then
    echo "Python is not installed. Please install Python before running this script."
    exit 1
else
    echo "Python path: $PYTHON_PATH"
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
echo "$VENV_NAME created and active."

# install pip
PIP_PATH=$(command -v pip3)
if [ -z "$PIP_PATH" ] ; then
    curl https://bootstrap.pypa.io/get-pip.py | python3
fi

# Install dependencies
pip3 install -r requirements.txt &>/dev/null

echo "Environment setup complete!"
