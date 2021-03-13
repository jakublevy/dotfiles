@echo off
setlocal EnableDelayedExpansion

for /D %%d in (D: F: G:) do (
	smartctl -n standby %%d >nul
	rem !errorlevel! equ 0 ACTIVE or IDLE
	rem !errorlevel! equ 2 STANDBY
	if !errorlevel! equ 0 (
		echo %%d --^> STANDBY
		smartctl -s standby,now %%d >nul
	)
)