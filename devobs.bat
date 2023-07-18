@echo off

REM Set the name of your virtual environment
set VENV_NAME=myenv

REM Set the path where the virtual environment will be created
set VENV_PATH=%~dp0\%VENV_NAME%

REM Check if the virtual env folder exists
if not exist "%VENV_PATH%" (
    echo For first time use, creating virtual environment and installing dependencies. This will take some while.
    REM Create the virtual environment
    python -m venv %VENV_PATH%

    REM Activate the virtual environment
    call %VENV_PATH%\Scripts\activate.bat

    REM Install required packages using pip
    pip install -r requirements.txt

    echo Virtual environment "%VENV_NAME%" has been created and activated.
    echo.
) else (
    REM Activate the virtual environment
    call %VENV_PATH%\Scripts\activate.bat
)

python app.py %*

REM Deactivate the virtual environment when finished
deactivate
