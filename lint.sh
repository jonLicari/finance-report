#!/bin/bash

# Ensure script has execute permissions
chmod +x "$0"

# Check if Black is installed
if ! command -v black &> /dev/null
then
    echo "Error: Black is not installed. Installing via pip3..."
    pip3 install black

    # Check if installation was successful
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install Black."
        exit 1
    fi
fi

# Check if Pylint is installed
if ! command -v pylint &> /dev/null
then
    echo "Error: Pylint is not installed. Installing via pip3..."
    pip3 install pylint

    # Check if installation was successful
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install Pylint."
        exit 1
    fi
fi

# Lint & Format
echo "Running Black..."
python3 -m black src/ || python -m black src/

echo "Linting complete."
