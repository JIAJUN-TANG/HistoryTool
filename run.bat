@echo off
SET "SCRIPT_PATH=%~dp0"
cd /d "%SCRIPT_PATH%"
conda activate myenv
if errorlevel 1 (
    echo Could not activate conda environment. Please check if 'myenv' is the correct environment name and you have conda initialized properly.
    exit /b
)
streamlit run Homepage.py