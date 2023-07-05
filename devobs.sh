#!/bin/bash

# Set the name of your virtual environment
VENV_NAME="myenv"

# Set the path where the virtual environment will be created
VENV_PATH="$(dirname "$0")/$VENV_NAME"

# Set the name and path of the dummy file
DUMMY_FILE="$VENV_PATH/requirements_installed.txt"

# Check if the dummy file exists
if [ ! -f "$DUMMY_FILE" ]; then
    echo "For first time use, creating virtual environment and installing dependencies."
    # Create the virtual environment
    python -m venv "$VENV_PATH"

    # Activate the virtual environment
    source "$VENV_PATH/bin/activate"

    # Install required packages using pip
    pip install -r requirements.txt

    # Create the dummy file to indicate that requirements have been installed
    echo "" > "$DUMMY_FILE"

    echo "Virtual environment \"$VENV_NAME\" has been created and activated."
    echo
else
    # Activate the virtual environment
    source "$VENV_PATH/bin/activate"
fi

# Check if verbose mode is enabled
if [[ "$1" == "-v" ]]; then
    # Run the main.py module within the virtual environment in verbose mode
    python app.py -v
else
    # Run the main.py module within the virtual environment
    python app.py
fi

# Deactivate the virtual environment when finished
deactivate

echo "Virtual environment has been deactivated."
