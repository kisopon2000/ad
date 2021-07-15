@echo off
rem Reuiqred PowerShell v4.0 or higher

if "%1" == "" (
	set CMD_PARAM="/k"
) else (
	set CMD_PARAM=%1
)
cd "%~dp0"
cmd %CMD_PARAM% powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0\Insert-PredefineRecords.ps1" ^
 -S "localhost" ^
 -port 3306 ^
 -D "ad" ^
 -U "root" ^
 -P "Rencho2000" ^
 -dataDir "data" ^
 -dataList "%~dp0\list.ini"
 
@echo on
