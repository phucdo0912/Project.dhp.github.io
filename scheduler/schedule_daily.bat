@echo off
cd /d "%~dp0.."
echo [%date% %time%] Starting daily crawl...
call python crawl_daily.py >> output\crawl_daily.log 2>&1
echo [%date% %time%] Daily crawl complete. >> output\crawl_daily.log
