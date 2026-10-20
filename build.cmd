@echo off
setlocal
cd /d "%~dp0"
set PYTHONUTF8=1
py -3 -c "import sys; sys.exit(sys.version_info < (3, 8))" >nul 2>&1
if not errorlevel 1 (
    py -3 build.py
    goto result
)
python -c "import sys; sys.exit(sys.version_info < (3, 8))" >nul 2>&1
if not errorlevel 1 (
    python build.py
    goto result
)
echo Python 3.8+ is required. Install it from https://www.python.org/downloads/
echo Enable "Add python.exe to PATH", then run this script again.
set build_result=1
goto finish

:result
set build_result=%errorlevel%
:finish
if not defined CI pause
exit /b %build_result%
