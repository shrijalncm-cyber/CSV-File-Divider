@echo off
REM Build with Nuitka for smaller executable size

echo ========================================
echo Building CSV Pro Tools with Nuitka
echo (Much smaller than PyInstaller)
echo ========================================
echo.

echo Installing Nuitka...
pip install nuitka ordered-set zstandard --quiet

echo.
echo Building optimized executable...
echo This will take 5-10 minutes (compiling Python to C)...
echo.

python -m nuitka ^
    --onefile ^
    --windows-disable-console ^
    --enable-plugin=tk-inter ^
    --remove-output ^
    --assume-yes-for-downloads ^
    --output-dir=dist_nuitka_csv ^
    --output-filename=CSV_Pro_Tools.exe ^
    --nofollow-import-to=pytest ^
    --nofollow-import-to=unittest ^
    --nofollow-import-to=test ^
    --nofollow-import-to=setuptools ^
    --nofollow-import-to=pip ^
    csv_converter_unified.py

echo.
echo ========================================
echo Build Complete!
echo ========================================
echo.

REM Show file size
powershell -Command "Get-ChildItem -Path 'dist_nuitka_csv\CSV_Pro_Tools.exe' | Select-Object Name, @{Name='Size (MB)';Expression={[math]::Round($_.Length/1MB, 2)}}"

echo.
echo Executable: dist_nuitka_csv\CSV_Pro_Tools.exe
echo.
pause
