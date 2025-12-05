@echo off
REM Ultra-optimized PyInstaller build with UPX compression

echo ========================================
echo Building CSV Pro Tools (Optimized)
echo ========================================
echo.

REM Clean previous builds
if exist build_csv rmdir /s /q build_csv
if exist dist_csv rmdir /s /q dist_csv

echo Installing dependencies...
pip install pyinstaller --quiet

echo.
echo Downloading UPX for compression...
echo.

REM Download UPX if not exists
if not exist upx.exe (
    echo Downloading UPX compressor...
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/upx/upx/releases/download/v4.2.2/upx-4.2.2-win64.zip' -OutFile 'upx.zip'"
    powershell -Command "Expand-Archive -Path 'upx.zip' -DestinationPath '.' -Force"
    move upx-4.2.2-win64\upx.exe .
    rmdir /s /q upx-4.2.2-win64
    del upx.zip
)

echo.
echo Building with maximum compression...
echo.

pyinstaller ^
    --onefile ^
    --windowed ^
    --name "CSV_Pro_Tools" ^
    --distpath dist_csv ^
    --workpath build_csv ^
    --clean ^
    --strip ^
    --optimize 2 ^
    --upx-dir=. ^
    --exclude-module matplotlib ^
    --exclude-module scipy ^
    --exclude-module numpy.distutils ^
    --exclude-module numpy.f2py ^
    --exclude-module tests ^
    --exclude-module test ^
    --exclude-module unittest ^
    --exclude-module email ^
    --exclude-module http.server ^
    --exclude-module xml.etree ^
    --exclude-module pydoc ^
    --exclude-module setuptools ^
    --exclude-module pip ^
    --exclude-module wheel ^
    --exclude-module distutils ^
    --exclude-module IPython ^
    --exclude-module notebook ^
    --exclude-module jupyter ^
    csv_converter_unified.py

echo.
echo Compressing with UPX...
upx --best --lzma dist_csv\CSV_Pro_Tools.exe

echo.
echo ========================================
echo Build Complete!
echo ========================================
echo.

REM Show file size
powershell -Command "Get-ChildItem -Path 'dist_csv\CSV_Pro_Tools.exe' | Select-Object Name, @{Name='Size (MB)';Expression={[math]::Round($_.Length/1MB, 2)}}"

echo.
echo Executable: dist_csv\CSV_Pro_Tools.exe
echo.
pause
