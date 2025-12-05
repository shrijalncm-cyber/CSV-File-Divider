@echo off
REM Ultra-minimal build script using PyInstaller with maximum compression

echo Creating ultra-minimal executable...
echo.

REM Clean previous builds
if exist build rmdir /s /q build
if exist dist_minimal rmdir /s /q dist_minimal

pyinstaller ^
    --onefile ^
    --windowed ^
    --name CSV_Breaker ^
    --distpath dist_minimal ^
    --workpath build_minimal ^
    --specpath . ^
    --clean ^
    --strip ^
    --noupx ^
    --optimize 2 ^
    --exclude-module matplotlib ^
    --exclude-module scipy ^
    --exclude-module numpy.distutils ^
    --exclude-module tests ^
    --exclude-module test ^
    --exclude-module unittest ^
    --exclude-module email ^
    --exclude-module http ^
    --exclude-module xml ^
    --exclude-module pydoc ^
    --exclude-module setuptools ^
    --exclude-module pip ^
    --exclude-module wheel ^
    --exclude-module pygments ^
    --exclude-module jedi ^
    csv_breaker.py

echo.
echo Build complete!
echo.

REM Show file size
powershell -Command "Get-ChildItem -Path 'dist_minimal\CSV_Breaker.exe' | Select-Object Name, @{Name='Size (MB)';Expression={[math]::Round($_.Length/1MB, 2)}}"

echo.
echo Executable location: dist_minimal\CSV_Breaker.exe
