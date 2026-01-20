@echo off
REM GoldenSeed Installation Script for Windows
REM This script installs the golden-seed package from source

echo ==================================
echo GoldenSeed Installation
echo ==================================
echo.

REM Check Python
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python not found. Please install Python 3.8 or higher.
    exit /b 1
)

REM Get Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python found: %PYTHON_VERSION%

REM Check pip
where pip >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] pip not found. Please install pip.
    exit /b 1
)
echo [OK] pip found

echo.
echo Installing golden-seed package...
echo.

REM Install package in development mode
pip install -e .
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Installation failed
    exit /b 1
)

echo [OK] Package installed successfully!
echo.

REM Verify installation
echo Verifying installation...
python -c "import gq; print(f'GoldenSeed version {gq.__version__} installed successfully')"
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Installation verification failed
    exit /b 1
)

echo [OK] Installation verified!
echo.

REM Show CLI commands
echo Available CLI commands:
echo   * gq-universal       - Universal deterministic stream generator
echo   * gq-test-vectors    - Generate test vectors
echo   * gq-coin-flip       - Golden ratio coin flip generator
echo.

echo [OK] Installation complete!
echo.
echo To get started, try:
echo   python -c "from gq import UniversalQKD; print(next(UniversalQKD()).hex())"
echo.

pause
