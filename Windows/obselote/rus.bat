@echo off

pwsh -Command "ls C:\ProgramData\chocolatey\lib\ -Recurse -Depth 1 | ? { $_.Name -Eq ""update.ps1"" } | Where-Object { Push-Location $_.DirectoryName; &$_.FullName; Pop-Location }"
