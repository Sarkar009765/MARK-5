@echo off
echo ClawVis Auto-Start Setup
echo =====================
echo.

set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

echo This will add ClawVis to Windows startup.
echo.

echo Choose:
echo 1. Add to startup (run at logon)
echo 2. Add to Task Scheduler (run as admin)
echo 3. Remove from startup
echo 4. Exit
echo.

set /p choice="Enter choice (1-4): "

if "%choice%"=="1" goto startup
if "%choice%"=="2" goto scheduler
if "%choice%"=="3" goto remove
goto exit

:startup
echo Adding to startup...
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v ClawVis /t REG_SZ /d "%SCRIPT_DIR%main.py" /f
echo Added to startup!
goto done

:scheduler
echo Adding to Task Scheduler...
schtasks /create /tn "ClawVis" /tr "python.exe \"%SCRIPT_DIR%main.py\"" /sc onlogon /rl limited /f
echo Added to Task Scheduler!
goto done

:remove
echo Removing...
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v ClawVis /f 2>nul
schtasks /delete /tn "ClawVis" /f 2>nul
echo Removed!
goto done

:done
echo.
echo Done! ClawVis will start automatically.
pause

:exit
exit