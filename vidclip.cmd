@echo off
setlocal
set "INSTALLED=%LOCALAPPDATA%\vidclip\venv\Scripts\vidclip.exe"
set "DEV=%~dp0.venv\Scripts\vidclip.exe"

if exist "%INSTALLED%" (
  "%INSTALLED%" %*
  exit /b %ERRORLEVEL%
)
if exist "%DEV%" (
  "%DEV%" %*
  exit /b %ERRORLEVEL%
)

echo vidclip is not installed yet.
echo Open this folder and double-click install.bat, then try again.
exit /b 1
