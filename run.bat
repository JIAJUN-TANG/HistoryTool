@echo off
SET "SCRIPT_PATH=%~dp0"
cd /d "%SCRIPT_PATH%"

REM 尝试激活conda环境，如果失败则直接运行streamlit
call conda activate myenv >nul 2>&1
if errorlevel 1 (
    echo Conda environment 'myenv' not found. Running streamlit directly.
    streamlit run Homepage.py
) else (
    streamlit run Homepage.py
)