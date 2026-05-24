@echo off
cd /d "%~dp0.."
echo [%date% %time%] Starting weekly pipeline...
call python run_apt_weekly.py >> output\apt_weekly.log 2>&1
echo [%date% %time%] Weekly pipeline complete. >> output\apt_weekly.log
