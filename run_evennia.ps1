# Define variables
$VENV_DIR = ".venv"
$DB_FILE = "server/evennia.db3"
$REQ_FILE = "requirements.txt"

# Check if virtual environment exists
if (-not (Test-Path -Path $VENV_DIR)) {
    Write-Host "Virtual environment not found. Creating one..."
    python -m venv $VENV_DIR

    # Activate and install dependencies
    # Note: In a script, activating the venv affects the current session scope.
    # However, since we might be running this from a fresh shell, we invoke pip via the venv path directly
    # OR we activate it. Activating in PS scripts can be tricky due to execution policies.
    # A safer bet is to use the direct path to the python executable in the venv for pip operations.

    $PYTHON_EXEC = "$VENV_DIR\Scripts\python.exe"
    $PIP_EXEC = "$VENV_DIR\Scripts\pip.exe"

    Write-Host "Upgrading pip..."
    & $PYTHON_EXEC -m pip install --upgrade pip

    if (Test-Path -Path $REQ_FILE) {
        Write-Host "Installing dependencies from $REQ_FILE..."
        & $PIP_EXEC install -r $REQ_FILE
    } else {
        Write-Host "Warning: $REQ_FILE not found. Installing evennia directly..."
        & $PIP_EXEC install evennia
    }
}

# We need to ensure 'evennia' command is available.
# In PowerShell, simply running the activate script works if the policy allows.
# Alternatively, we can use the 'evennia.exe' inside Scripts directly.
$EVENNIA_EXEC = "$VENV_DIR\Scripts\evennia.exe"

# Check if database exists
if (-not (Test-Path -Path $DB_FILE)) {
    Write-Host "Database not found. Initializing..."
    & $EVENNIA_EXEC migrate
}

# Run the command passed to the script
Write-Host "Running evennia command..."
& $EVENNIA_EXEC @args
