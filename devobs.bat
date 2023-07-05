@echo off

REM Set the name of your virtual environment
set VENV_NAME=myenv

REM Set the path where the virtual environment will be created
set VENV_PATH=%~dp0\%VENV_NAME%

REM Set the name and path of the dummy file
set DUMMY_FILE=%VENV_PATH%\requirements_installed.txt

REM Check if the dummy file exists
if not exist "%DUMMY_FILE%" (
    echo For first time use, creating virtual environment and installing dependencies..
    REM Create the virtual environment
    python -m venv %VENV_PATH%

    REM Activate the virtual environment
    call %VENV_PATH%\Scripts\activate.bat

    REM Install required packages using pip
    pip install -r requirements.txt

    REM Create the dummy file to indicate that requirements have been installed
    echo. > "%DUMMY_FILE%"

    echo Virtual environment "%VENV_NAME%" has been created and activated.
    echo.
) else (
    REM Activate the virtual environment
    call %VENV_PATH%\Scripts\activate.bat
)

REM Check if the verbose flag is provided as a command-line argument
set VERBOSE=false
if "%~1"=="-v" set VERBOSE=true

REM Run the main.py module within the virtual environment, passing the verbose flag
if "%VERBOSE%"=="true" (
    python app.py -v
) else (
    python app.py
)

REM Deactivate the virtual environment when finished
deactivate
