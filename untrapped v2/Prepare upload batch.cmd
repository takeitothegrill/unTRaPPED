@echo off
setlocal
cd /d "%~dp0"
python tools\prepare_upload_batch.py
set "result=%ERRORLEVEL%"
echo.
if "%result%"=="0" (
  echo Preparation finished. Review the RESULTS.txt file in the new batches folder.
) else (
  echo Preparation finished with items needing attention. Review RESULTS.txt in the new batches folder.
)
pause
exit /b %result%
