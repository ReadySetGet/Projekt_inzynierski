# Projekt_inzynierski

Edytor graficzny systemów rozmytych dla języka Python

## Setup

### Prerequisites

- Python 3.x
- PowerShell (Windows)

### Initial Setup

If Chocolatey and `make` are not installed on your machine, run the setup script **as Administrator**:

```powershell
# Run PowerShell as Administrator, then:
.\commands\setup_windows.ps1
```

This script will:

- Install Chocolatey (if not present)
- Install `make` (if not present)
- Create a virtual environment (`.venv`)
- Install project dependencies
- Set up pre-commit hooks

### Manual Setup (Alternative)

If you prefer to set up manually:

```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Install pre-commit hooks
pre-commit install --hook-type commit-msg
pre-commit install --hook-type pre-push
```

## Running the Application

### Using Make (Recommended)

```bash
make start
```

### Using Python Directly

```bash
# Activate virtual environment first
.\.venv\Scripts\Activate.ps1

# Run the application
python main.py
```

Or directly:

```bash
.\.venv\Scripts\python.exe main.py
```

## Available Make Commands

- `make start` - Run the application
- `make debug` - Run with debugger attached
- `make lint` - Run linter
- `make lint-fix` - Fix linting issues
- `make format` - Format code
- `make format-check` - Check code formatting
- `make test` - Run tests
- `make test-watch` - Run tests in watch mode
- `make test-coverage` - Run tests with coverage report
- `make type-check` - Run type checker
