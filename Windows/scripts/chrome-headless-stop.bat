@echo off

wmic path win32_process Where "Caption Like '%%chrome.exe%%' AND CommandLine Like '%%--headless%%'" Call Terminate > nul