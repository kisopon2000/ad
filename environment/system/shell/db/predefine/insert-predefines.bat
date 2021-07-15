@echo off
rem Reuiqred PowerShell v4.0 or higher

cd "%~dp0"
cmd /k powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0\insert-predefines.ps1" ^
 -S "localhost" ^
 -I "PWSP" ^
 -port 0 ^
 -D "ad" ^
 -U "Ad" ^
 -P "P@ssW0rd" ^
 -dataDir "data"
 
@echo on