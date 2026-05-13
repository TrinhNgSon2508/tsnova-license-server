@echo off

cd /d %~dp0..

echo =====================================
echo BUILDING TSNOVA
echo =====================================

python -m PyInstaller tsnova.spec

echo.
echo =====================================
echo BUILD FINISHED
echo =====================================

pause