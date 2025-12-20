@echo off
REM Batch script to build Python script into .exe with PyInstaller

REM Get the name of the Python script in this folder
SET SCRIPT_NAME=EZM_Updater.py
SET ICON_NAME=EZM_Updater_Icon.ico
SET MP3_FILE=a3.wav 

REM Run PyInstaller 
REM use --windowed for no cmd window
REM --add-data "%MP3_FILE%;%MP3_FILE%"
pyinstaller --onefile --icon=%ICON_NAME% %SCRIPT_NAME%

REM Pause so you can see any errors
pause
