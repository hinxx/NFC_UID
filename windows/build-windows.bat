@echo off
setlocal

for %%I in ("%~dp0..") do set "ROOT=%%~fI"
set "PYTHON=%ROOT%\.venv\Scripts\python.exe"

if not exist "%PYTHON%" (
    echo Virtual environment not found. Create it first with: py -3.13 -m venv .venv
    exit /b 1
)

if /I "%1"=="clean" (
    if exist "%ROOT%\build" rmdir /s /q "%ROOT%\build"
    if exist "%ROOT%\dist" rmdir /s /q "%ROOT%\dist"
)

pushd "%ROOT%"
"%PYTHON%" -m PyInstaller ^
    --clean ^
    --noconfirm ^
    --onefile ^
    --name nfc-uid ^
    nfc_uid\__main__.py
set "EXITCODE=%ERRORLEVEL%"
popd

if not "%EXITCODE%"=="0" exit /b %EXITCODE%

echo.
echo Build complete:
echo   dist\nfc-uid.exe
