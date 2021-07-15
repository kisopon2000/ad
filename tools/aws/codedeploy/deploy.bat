@echo off
break on

REM Install Internet Information Server (IIS). 
C:\Windows\Sysnative\WindowsPowerShell\v1.0\powershell.exe -Command Import-Module -Name ServerManager
C:\Windows\Sysnative\WindowsPowerShell\v1.0\powershell.exe -Command Install-WindowsFeature Web-Server

REM Defines
set errorlevel=0
set CWD=%~dp0
set LOG_FILE_DIR=C:\codedeploy
set LOG_FILE_PATH=%LOG_FILE_DIR%\codedeploy.log
set ENV_ZIP_PATH=%CWD%..\..\..\environment.zip
set INTEGRATION_DIR=C:\HOME\ad
set ENV_ZIP_DEST_PATH=%INTEGRATION_DIR%\environment.zip
set INTEGRATION_ENV_DIR=%INTEGRATION_DIR%\environment

if not exist %LOG_FILE_DIR% (
    mkdir %LOG_FILE_DIR%
)

echo Initialize > %LOG_FILE_PATH%
if not exist %INTEGRATION_DIR% (
    mkdir %INTEGRATION_DIR%
)
if exist %ENV_ZIP_DEST_PATH% (
    del %ENV_ZIP_DEST_PATH% /Q
)
if exist %INTEGRATION_ENV_DIR% (
    rmdir %INTEGRATION_ENV_DIR% /s /q
)
if %errorlevel% neq 0 (
    echo Initialize Error >> %LOG_FILE_PATH%
    goto DEPLOY_END
)

echo Copy Archive >> %LOG_FILE_PATH%
copy %ENV_ZIP_PATH% %ENV_ZIP_DEST_PATH%

echo Unzip Archive >> %LOG_FILE_PATH%
C:\Windows\Sysnative\WindowsPowerShell\v1.0\powershell.exe -noprofile -ExecutionPolicy RemoteSigned -command "Expand-Archive -Path %ENV_ZIP_DEST_PATH% -DestinationPath %INTEGRATION_DIR%"
if %errorlevel% neq 0 (
    echo Unzip Archive Error >> %LOG_FILE_PATH%
    goto DEPLOY_END
)

echo IIS Setup >> %LOG_FILE_PATH%
C:\Windows\Sysnative\WindowsPowerShell\v1.0\powershell.exe -noprofile -ExecutionPolicy RemoteSigned %INTEGRATION_ENV_DIR%\system\shell\iis-setup.ps1
if %errorlevel% neq 0 (
    echo IIS Setup Error >> %LOG_FILE_PATH%
    goto DEPLOY_END
)

echo DB drop >> %LOG_FILE_PATH%
C:\Windows\Sysnative\WindowsPowerShell\v1.0\powershell.exe -noprofile -ExecutionPolicy RemoteSigned %INTEGRATION_ENV_DIR%\system\shell\db\drop.bat
if %errorlevel% neq 0 (
    echo DB drop Error >> %LOG_FILE_PATH%
    REM goto DEPLOY_END
)

echo DB restore >> %LOG_FILE_PATH%
C:\Windows\Sysnative\WindowsPowerShell\v1.0\powershell.exe -noprofile -ExecutionPolicy RemoteSigned %INTEGRATION_ENV_DIR%\system\shell\db\restore.bat
if %errorlevel% neq 0 (
    echo DB restore Error >> %LOG_FILE_PATH%
    goto DEPLOY_END
)

echo DB predefined data restore >> %LOG_FILE_PATH%
C:\Windows\Sysnative\WindowsPowerShell\v1.0\powershell.exe -noprofile -ExecutionPolicy RemoteSigned %INTEGRATION_ENV_DIR%\system\shell\db\predefine\insert-predefines.bat
if %errorlevel% neq 0 (
    echo DB predefined data restore >> %LOG_FILE_PATH%
    goto DEPLOY_END
)

:DEPLOY_END

exit /b %errorlevel%