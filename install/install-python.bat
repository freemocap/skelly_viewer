@echo off
setlocal

if "%~1"=="" (
    echo Usage: %~nx0 pythonRequirementsFullPath, targetBinaryName pythonMainFilePath binaryDestinationFolder
    exit /b 1
)

set pyProjectTomlFullPath=%~1
set targetBinaryName=%~2
set pythonMainFilePath=%~3
set binaryDestinationFolder=%~4

echo Executing .bat file from working directory:
cd

echo Creating virtual environment...
CALL python -m venv venv

echo Activating virtual environment...
CALL venv\Scripts\activate.bat

echo Upgrading pip...
CALL python -m pip install --upgrade pip

echo Installing Python requirements...
CALL pip install -e %pythonRequirementsFullPath%

echo Building with PyInstaller...
CALL pyinstaller --onefile %pythonMainFilePath% --distpath %binaryDestinationFolder% --name %targetBinaryName%

endlocal
