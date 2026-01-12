# Define variables
$VENV_DIR = ".venv"
$DB_FILE = "server/evennia.db3"
$REQ_FILE = "requirements.txt"
$SUPERUSER_SCRIPT = "server/ensure_superuser.py"

# Function to check/create venv and install deps
function Ensure-Venv {
    if (-not (Test-Path -Path $VENV_DIR)) {
        Write-Host "Virtual environment not found. Creating one..."
        python -m venv $VENV_DIR

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

        Write-Host "Installing pytest..."
        & $PIP_EXEC install pytest
    }
}

# Ensure Venv exists
Ensure-Venv

# Set executables
$PYTHON_EXEC = "$VENV_DIR\Scripts\python.exe"
$EVENNIA_EXEC = "$VENV_DIR\Scripts\evennia.exe"

# Parse arguments
$RESET = $false
$TEST = $false
$PASSTHROUGH_ARGS = @()

foreach ($arg in $args) {
    if ($arg -eq "--reset") {
        $RESET = $true
    } elseif ($arg -eq "--test") {
        $TEST = $true
    } else {
        $PASSTHROUGH_ARGS += $arg
    }
}

# Handle Reset
if ($RESET) {
    Write-Host "Resetting database..."
    if (Test-Path -Path $DB_FILE) {
        Remove-Item -Path $DB_FILE -Force
        Write-Host "Database deleted."
    }
}

# Check if database exists or needs migration
if (-not (Test-Path -Path $DB_FILE)) {
    Write-Host "Database not found or reset. Initializing..."
    & $EVENNIA_EXEC migrate
    Write-Host "Creating default superuser..."
    & $PYTHON_EXEC $SUPERUSER_SCRIPT
}

# Handle Test
if ($TEST) {
    Write-Host "Running tests..."
    & $EVENNIA_EXEC test .
    exit $LASTEXITCODE
}

# Run the command passed to the script
if ($PASSTHROUGH_ARGS.Count -eq 0) {
    Write-Host "No command provided. Starting Evennia..."
    & $EVENNIA_EXEC start -l
} else {
    Write-Host "Running evennia command: $PASSTHROUGH_ARGS"
    & $EVENNIA_EXEC @PASSTHROUGH_ARGS
}
