@echo off

cd /d "%~dp0"

set "PYTHON=C:\Users\MANNURI ADITYA\AppData\Local\Python\pythoncore-3.14-64\python.exe"

start "IGRIS-CONVERSATION" /min "%PYTHON%" conversation_server.py

timeout /t 2 /nobreak >nul

start "IGRIS-VOICE" /min "%PYTHON%" wake_listener.py

exit