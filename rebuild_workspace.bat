@echo off
setlocal

set "VITIS_BAT=C:\AMDDesignTools\2025.2\Vitis\bin\vitis.bat"
set "SCRIPT_DIR=%~dp0"

if not exist "%VITIS_BAT%" (
    echo ERROR: Vitis launcher not found:
    echo   %VITIS_BAT%
    echo Edit VITIS_BAT in %~nx0 if Vitis is installed elsewhere.
    exit /b 1
)

if not exist "%SCRIPT_DIR%rebuild_workspace.py" (
    echo ERROR: rebuild_workspace.py not found next to %~nx0
    exit /b 1
)

chcp 65001 > nul
pushd "%SCRIPT_DIR%"

if "%~1"=="" (
    call "%VITIS_BAT%" -s rebuild_workspace.py --force
) else (
    call "%VITIS_BAT%" -s rebuild_workspace.py %*
)

set "STATUS=%ERRORLEVEL%"
popd
exit /b %STATUS%
