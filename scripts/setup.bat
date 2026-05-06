@echo off
echo ClawVis Setup
echo =============
echo.

python -m venv venv
call venv\Scripts\activate.bat

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Creating .env file...
if not exist .env (
    copy .env.example .env
    echo Please add your API keys to .env
)

echo.
echo Setup complete!
echo Run: python main.py
pause