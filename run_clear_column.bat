@echo off
set /p TARGET_DATE=Enter the target date (YYYY-MM-DD), or press Enter for yesterday: 

if "%TARGET_DATE%"=="" (
    for /f %%i in ('powershell -Command "(Get-Date).AddDays(-1).ToString(\"yyyy-MM-dd\")"') do set TARGET_DATE=%%i
    echo No input. Using yesterday's date: %TARGET_DATE%
)

python .\app.py %TARGET_DATE%
