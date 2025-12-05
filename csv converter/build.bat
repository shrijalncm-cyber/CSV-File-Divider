@echo off
echo ========================================
echo Building CSV Pro Tools
echo ========================================
echo.

REM Clean previous builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo Building executable...
echo.

pyinstaller --onefile --windowed --name "CSV_Pro_Tools" csv_converter.py

echo.
echo ========================================
echo Build Complete!
echo ========================================
echo.

REM Show file size
powershell -Command "if (Test-Path 'dist\CSV_Pro_Tools.exe') { Get-ChildItem -Path 'dist\CSV_Pro_Tools.exe' | Select-Object Name, @{Name='Size (MB)';Expression={[math]::Round($_.Length/1MB, 2)}} } else { Write-Host 'Build failed - no exe created' }"

echo.
if exist dist\CSV_Pro_Tools.exe (
    echo Executable: dist\CSV_Pro_Tools.exe
) else (
    echo Build failed! Check error messages above.
)
echo.
pause
