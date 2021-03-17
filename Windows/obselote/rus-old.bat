@echo off
setlocal EnableDelayedExpansion

set "olddir=%cd%"

cd C:\ProgramData\chocolatey\lib

for /f "skip=2 tokens=* USEBACKQ" %%a in (`robocopy . . /l /s /njs /njh /ns /lev:2`) do (
	cd /d %%a
	dir | findstr /C:update.ps1
	if !errorlevel! equ 0 (
		:: rem update.ps1 found
		pwsh -File update.ps1
	)
)

cd %olddir%


