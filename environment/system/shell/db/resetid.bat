@echo off
break on
set CWD=%~dp0
REM =============================================
REM ID���Z�b�g
REM �N���p�����[�^
REM 1:�T�[�o�[�� 2:�f�[�^�x�[�X�� 3:���[�U�[ID 4:�p�X���[�h 5:���O
REM --------------------------------
REM ����
REM 1.ID���Z�b�g
REM =============================================

REM DB�T�[�o�[��
Set ServerName=localhost\PWSP
Set Database=ad

REM Dashboard���[�U�[
Set UserID=Ad
Set Password=P@ssW0rd

REM ���O�o�͐�
Set LogPath=%CWD%

REM �N���p�����[�^�`�F�b�N
if "%1"=="" (set ServerName=%ServerName%) Else (set ServerName=%1)
if "%2"=="" (set Database=%Database%) Else (set Database=%2)
if "%3"=="" (set UserID=%UserID%) Else (set UserID=%3)
if "%4"=="" (set Password=%Password%) Else (set Password=%4)
if "%~5"=="" (set LogPath=%LogPath%) Else (set LogPath=%~5)

REM ���O�o��
Set cmdlog=%LogPath%\ResetIdBat.log
Set sqllog=%LogPath%\ResetIdSql.log

REM �N���p�����[�^
echo ID Reset start. > %cmdlog%
echo ServerName=%ServerName% >> %cmdlog%
echo Database=%Database% >> %cmdlog%
echo UserID=%UserID% >> %cmdlog%

REM ID���Z�b�g
sqlcmd -S %ServerName% -U %UserID% -P %Password% -o %sqllog% -Q "EXIT(USE [%Database%] BEGIN TRY DBCC CHECKIDENT ('ads', RESEED, 0); SELECT 0 END TRY BEGIN CATCH SELECT ERROR_NUMBER(),ERROR_MESSAGE() END CATCH)"
sqlcmd -S %ServerName% -U %UserID% -P %Password% -o %sqllog% -Q "EXIT(USE [%Database%] BEGIN TRY DBCC CHECKIDENT ('m_ad_types', RESEED, 0); SELECT 0 END TRY BEGIN CATCH SELECT ERROR_NUMBER(),ERROR_MESSAGE() END CATCH)"

REM �I��
echo ID Reset Result=%errorlevel% >> %cmdlog%
exit /b %errorlevel%
