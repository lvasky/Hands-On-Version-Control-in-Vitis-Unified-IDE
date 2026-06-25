@echo off
setlocal

@REM Use the system environment variable VITIS_BAT to locate the Vitis launcher.
@REM Example in Windows system environment variables:
@REM   VITIS_BAT=C:\AMDDesignTools\2025.2\Vitis\bin\vitis.bat
@REM Or set it temporarily in the current CMD session:
@REM   set "VITIS_BAT=C:\AMDDesignTools\2025.2\Vitis\bin\vitis.bat"
set "SCRIPT_DIR=%~dp0"

if "%VITIS_BAT%"=="" (
    echo ERROR: VITIS_BAT environment variable is not defined.
    echo Set VITIS_BAT to your Vitis launcher path and rerun this script.
    exit /b 1
)

if not exist "%VITIS_BAT%" (
    echo ERROR: Vitis launcher not found:
    echo   %VITIS_BAT%
    echo Check the VITIS_BAT environment variable.
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
