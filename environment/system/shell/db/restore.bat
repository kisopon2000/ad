@echo off
break on
set CWD=%~dp0
set SysRootPath=%CWD%..\..\..\
REM =============================================
REM �f�[�^�x�[�X�̕���
REM �N���p�����[�^
REM 1:�T�[�o�[�� 2:�����t�@�C���p�X 3:���O�t�@�C���t�H���_ 4:���[�U�[ID 5:�p�X���[�h 6:mdf/ldf�̃t�@�C���t�H���_ 7:�f�[�^�x�[�X��
REM --------------------------------
REM ����
REM 1.Dashboard_Admin���[�U�[�Ń��O�C��
REM 2.�u�f�[�^�x�[�X���v�̃f�[�^�x�[�X�쐬(����)
REM 3.���[�U�[�č쐬 ��� �uDashboard_Admin�v�����݂���΁A��x���[�U�[���폜
REM 4.���[�U�[�}�b�s���O�����s (dbo) 
REM 5.�uDashboard_Admin�v�Őڑ��m�F
REM =============================================

REM DB�T�[�o�[��
Set ServerName=localhost\PWSP

REM DB���[�U�[
Set Database=ad
Set UserID=Ad
Set Password=P@ssW0rd

REM ���̓t�@�C���p�X
Set inFilePath=%CWD%..\..\db\ad.bak

REM ���O�o�͐�
Set LogPath=%CWD%

REM mdf/ldf�̃t�@�C��
Set sqlserverDataPath=C:\HOME\ad\db
if not exist %sqlserverDataPath% (
    mkdir %sqlserverDataPath%
)

REM �N���p�����[�^�`�F�b�N
if "%1"=="" (set ServerName=%ServerName%) Else (set ServerName=%1)
if "%~2"=="" (set inFilePath=%inFilePath%) Else (set inFilePath=%~2)
if "%~3"=="" (set LogPath=%LogPath%) Else (set LogPath=%~3)
if "%4"=="" (set UserID=%UserID%) Else (set UserID=%4)
if "%5"=="" (set Password=%Password%) Else (set Password=%5)
if "%~6"=="" (set sqlserverDataPath=%sqlserverDataPath%) Else (set sqlserverDataPath=%~6)
if "%7"=="" (set Database=%Database%) Else (set Database=%7)

REM ���O�o��
Set sqllog="%LogPath%\RestoreSql.log"
Set cmdlog="%LogPath%\RestoreBat.log"

REM �N���p�����[�^
echo DB setup start. > %cmdlog%
echo ServerName=%ServerName% >> %cmdlog%
echo inFilePath=%inFilePath% >> %cmdlog%
echo UserID=%UserID% >> %cmdlog%
echo sqlserverDataPath=%sqlserverDataPath% >> %cmdlog%
echo Database=%Database% >> %cmdlog%

REM �����J�n
sqlcmd -S %ServerName% -U %UserID% -P %Password% -d "master" -o %sqllog% -Q "EXIT(USE [master] BEGIN TRY RESTORE DATABASE [%Database%] FROM DISK = N'%inFilePath%' WITH FILE = 1,  MOVE N'ad' TO N'%sqlserverDataPath%\%Database%.mdf',  MOVE N'ad_log' TO N'%sqlserverDataPath%\%Database%_log.ldf',  NOUNLOAD,  STATS = 5 SELECT 0 END TRY BEGIN CATCH SELECT ERROR_NUMBER(),ERROR_MESSAGE() END CATCH)"

REM PWSP-�Z�L�����e�B-���[�U�[-�폜
If %errorlevel%==0 (
   sqlcmd -S %ServerName% -U %UserID% -P %Password% -d "master" -o %sqllog% -Q "EXIT(USE [%Database%] BEGIN TRY DROP USER IF EXISTS [%UserID%] SELECT 0 END TRY BEGIN CATCH SELECT ERROR_NUMBER(),ERROR_MESSAGE() END CATCH)"
)

REM �f�[�^�x�[�X-�Z�L�����e�B-���O�C���X�V�E�}�b�s���O
If %errorlevel%==0 (
   sqlcmd -S %ServerName% -U %UserID% -P %Password% -d "master" -o %sqllog% -Q "EXIT(USE [Master] BEGIN TRY ALTER LOGIN [%UserID%] WITH PASSWORD=N'%Password%' , DEFAULT_DATABASE=[%Database%] ; USE [%Database%] CREATE USER [%UserID%] FOR LOGIN [%UserID%] ALTER USER [%UserID%] WITH DEFAULT_SCHEMA=[dbo] ALTER ROLE [db_owner] ADD MEMBER [%UserID%] ;  SELECT 0 END TRY BEGIN CATCH SELECT ERROR_NUMBER(),ERROR_MESSAGE() END CATCH)"
)

REM �ڑ��m�F
If %errorlevel%==0 (
   sqlcmd -S %ServerName% -U %UserID% -P %Password% -o %sqllog% -Q "EXIT(BEGIN TRY SELECT Getdate() SELECT 0 END TRY BEGIN CATCH SELECT ERROR_NUMBER(),ERROR_MESSAGE() END CATCH)"
)

REM �I��
echo DB setup Result=%errorlevel% >> %cmdlog%
exit /b %errorlevel%
