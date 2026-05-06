@echo off
echo =============================================
echo   ClawVis - Voice Model Downloader
echo =============================================
echo.

set MODELS_DIR=%~dp0..\models
set VOSK_DIR=%MODELS_DIR%\vosk-model

if not exist "%MODELS_DIR%" mkdir "%MODELS_DIR%"

echo Checking for Vosk speech model...
if exist "%VOSK_DIR%\README" (
    echo [OK] Vosk model already installed!
    goto done
)

echo.
echo Downloading Vosk small English model (~40MB)...
echo This is needed for voice recognition and wake word detection.
echo.

where curl >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] curl not found. Please install curl or download manually:
    echo   https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
    echo   Extract to: %VOSK_DIR%
    goto done
)

set VOSK_URL=https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
set VOSK_ZIP=%MODELS_DIR%\vosk-model.zip

echo Downloading from %VOSK_URL%
curl -L -o "%VOSK_ZIP%" "%VOSK_URL%"

if %errorlevel% neq 0 (
    echo [ERROR] Download failed! Check your internet connection.
    goto done
)

echo.
echo Extracting model...

where tar >nul 2>&1
if %errorlevel% equ 0 (
    tar -xf "%VOSK_ZIP%" -C "%MODELS_DIR%"
) else (
    powershell -command "Expand-Archive -Path '%VOSK_ZIP%' -DestinationPath '%MODELS_DIR%' -Force"
)

:: Rename extracted folder to expected name
if exist "%MODELS_DIR%\vosk-model-small-en-us-0.15" (
    ren "%MODELS_DIR%\vosk-model-small-en-us-0.15" "vosk-model"
)

:: Cleanup zip
del "%VOSK_ZIP%" 2>nul

echo.
if exist "%VOSK_DIR%" (
    echo [SUCCESS] Vosk model installed to %VOSK_DIR%
) else (
    echo [ERROR] Something went wrong. Please download manually:
    echo   https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
    echo   Extract contents to: %VOSK_DIR%
)

:done
echo.
pause
