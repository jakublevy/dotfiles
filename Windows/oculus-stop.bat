@echo off

taskkill /IM "OculusClient.exe" /F
sc stop "OVRService"