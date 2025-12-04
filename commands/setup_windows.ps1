# Get the project root (parent directory of this script)
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectRoot = Split-Path -Parent $ProjectRoot

# Change to project root
Set-Location $ProjectRoot

# Check for Chocolatey and install if missing
if (!(Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Host "Chocolatey not found. Installing Chocolatey..."
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
} else {
    Write-Host "Chocolatey is already installed."
}

# Refresh environment variables
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Install make if not present
if (!(Get-Command make -ErrorAction SilentlyContinue)) {
    Write-Host "Installing make..."
    choco install make -y
} else {
    Write-Host "make is already installed."
}

# Create virtual environment if not present
if (!(Test-Path ".venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv .venv
} else {
    Write-Host ".venv already exists."
}

# Activate virtual environment and install requirements
Write-Host "Activating virtual environment and installing requirements..."
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# Install pre-commit hooks
Write-Host "Installing pre-commit hooks..."
.\.venv\Scripts\python.exe -m pre_commit install --hook-type commit-msg
.\.venv\Scripts\python.exe -m pre_commit install --hook-type pre-push

Write-Host "Setup complete! You can now use 'make start' or 'python main.py' to run the project." 