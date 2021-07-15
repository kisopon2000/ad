@echo off
break on
set CWD=%~dp0
set SysRootPath=%CWD%..\..\..\
REM =============================================
REM ���O�C�����[�U�[�쐬
REM �N���p�����[�^
REM 1:�T�[�o�[�� 2:���[�U�[ID 3:�p�X���[�h 4:���O
REM --------------------------------
REM ����
REM 1.���[�U�[���쐬
REM =============================================

REM DB�T�[�o�[��
Set ServerName=localhost\PWSP

REM DB���[�U�[
Set UserID=Ad
Set Password=P@ssW0rd

REM ���O�o�͐�
Set LogPath=%CWD%

REM �N���p�����[�^�`�F�b�N
if "%1"=="" (set ServerName=%ServerName%) Else (set ServerName=%1)
if "%2"=="" (set UserID=%UserID%) Else (set UserID=%2)
if "%3"=="" (set Password=%Password%) Else (set Password=%3)
if "%~4"=="" (set LogPath=%LogPath%) Else (set LogPath=%~4)

REM ���O�o��
Set cmdlog=%LogPath%\CreateUserBat.log
Set sqllog=%LogPath%\CreateUserSql.log

REM �N���p�����[�^
echo User Create start. > %cmdlog%
echo ServerName=%ServerName% >> %cmdlog%
echo UserID=%UserID% >> %cmdlog%

REM �f�[�^�x�[�X-�Z�L�����e�B-���O�C��-�쐬
sqlcmd -S %ServerName% -o %sqllog% -Q "EXIT(USE [Master] BEGIN TRY IF NOT EXISTS (SELECT * FROM sys.syslogins where name = N'%UserID%') CREATE LOGIN [%UserID%] WITH PASSWORD=N'%Password%',  DEFAULT_DATABASE=[master] , DEFAULT_LANGUAGE=[���{��], CHECK_EXPIRATION=OFF, CHECK_POLICY=ON ; ALTER SERVER ROLE [sysadmin] ADD MEMBER [%UserID%] ; SELECT 0 END TRY BEGIN CATCH SELECT ERROR_NUMBER(),ERROR_MESSAGE() END CATCH)"

REM VIEW SERVER STATE�����t�^
If %errorlevel%==0 (
   sqlcmd -S %ServerName% -o %sqllog% -Q "EXIT(USE [master] BEGIN TRY GRANT VIEW SERVER STATE TO [%UserID%] ; SELECT 0 END TRY BEGIN CATCH SELECT ERROR_NUMBER(),ERROR_MESSAGE() END CATCH)"
)

REM �I��
echo User Create Result=%errorlevel% >> %cmdlog%
exit /b %errorlevel%
