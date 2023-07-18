#!/bin/bash

# Exit immediately if any command exits with a non-zero status
set -e

# Check the Python version
if ! python3 --version 2>&1 | grep -q "Python 3"; then
    echo "Error: Python 3 is required to run this application."
    exit 1
fi

# Set the name of your virtual environment
VENV_NAME="myenv"

# Set the path where the virtual environment will be created
VENV_PATH="$(dirname "$0")/$VENV_NAME"

# Check if the dummy file exists
if [ ! -d "$VENV_PATH" ]; then
    echo "For first time use, creating virtual environment and installing dependencies. This will take some while."
    # Create the virtual environment
    python3 -m venv "$VENV_PATH"

    # Activate the virtual environment
    source "$VENV_PATH/bin/activate"

    # Install required packages using pip
    pip install -r requirements.txt

    echo "Virtual environment \"$VENV_NAME\" has been created and activated."
    echo
else
    # Activate the virtual environment
    source "$VENV_PATH/bin/activate"
fi

python3 app.py "$@"

# Deactivate the virtual environment when finished
deactivate

echo "Virtual environment has been deactivated."
