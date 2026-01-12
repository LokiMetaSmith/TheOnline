#!/bin/bash

# Define variables
VENV_DIR=".venv"
DB_FILE="server/evennia.db3"
REQ_FILE="requirements.txt"
SUPERUSER_SCRIPT="server/ensure_superuser.py"

# Function to activate virtual environment
activate_venv() {
    if [ ! -d "$VENV_DIR" ]; then
        echo "Virtual environment not found. Creating one..."
        python3 -m venv "$VENV_DIR"
        source "$VENV_DIR/bin/activate"
        echo "Upgrading pip..."
        pip install --upgrade pip

        # Install dependencies
        if [ -f "$REQ_FILE" ]; then
            echo "Installing dependencies from $REQ_FILE..."
            pip install -r "$REQ_FILE"
        else
            echo "Warning: $REQ_FILE not found. Installing evennia directly..."
            pip install evennia
        fi
        # Ensure pytest is installed for testing
        pip install pytest
    else
        source "$VENV_DIR/bin/activate"
    fi
}

# Parse arguments
RESET=false
TEST=false

for arg in "$@"; do
    case $arg in
        --reset)
            RESET=true
            shift
            ;;
        --test)
            TEST=true
            shift
            ;;
    esac
done

# Main Execution
activate_venv

if [ "$RESET" = true ]; then
    echo "Resetting database..."
    if [ -f "$DB_FILE" ]; then
        rm "$DB_FILE"
        echo "Database deleted."
    fi
    # Also clear migrations if necessary? No, usually not for dev unless strict reset.
    # Just running migrate is enough for fresh DB.
fi

# Check if database exists or needs migration
if [ ! -f "$DB_FILE" ]; then
    echo "Database not found or reset. Initializing..."
    evennia migrate
    echo "Creating default superuser..."
    python3 "$SUPERUSER_SCRIPT"
fi

if [ "$TEST" = true ]; then
    echo "Running tests..."
    evennia test .
    exit $?
fi

# Run the command passed to the script, or default to start
if [ $# -eq 0 ]; then
    echo "No command provided. Starting Evennia..."
    evennia start -l
else
    echo "Running evennia command: $@"
    evennia "$@"
fi
