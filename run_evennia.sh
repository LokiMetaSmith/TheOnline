#!/bin/bash

# Define variables
VENV_DIR=".venv"
DB_FILE="server/evennia.db3"
REQ_FILE="requirements.txt"

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv "$VENV_DIR"

    # Activate and install dependencies
    source "$VENV_DIR/bin/activate"
    echo "Upgrading pip..."
    pip install --upgrade pip

    if [ -f "$REQ_FILE" ]; then
        echo "Installing dependencies from $REQ_FILE..."
        pip install -r "$REQ_FILE"
    else
        echo "Warning: $REQ_FILE not found. Installing evennia directly..."
        pip install evennia
    fi
else
    source "$VENV_DIR/bin/activate"
fi

# Check if database exists
if [ ! -f "$DB_FILE" ]; then
    echo "Database not found. Initializing..."
    evennia migrate
fi

# Run the command passed to the script
echo "Running evennia command..."
evennia "$@"
