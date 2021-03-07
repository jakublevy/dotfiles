@echo off

reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v "ProxyServer" /t REG_SZ /d "socks=localhost:9050" /f > nul

reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v "ProxyEnable" /t REG_DWORD /d 1 /f > nul

reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v "ProxyOverride" /t REG_SZ /d "<local>" /f > nul

SET curpath=%~dp0
powershell -Command "& { . %curpath:~0,-1%\..\libs\ps\registry-changed.ps1; refresh-system | Out-Null }"
sc start tor > nul


