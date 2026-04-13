@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

if not exist input mkdir input
if not exist frames mkdir frames
if not exist bimg mkdir bimg
if not exist output mkdir output

echo.
set /p URL=Paste YouTube URL: 
if "%URL%"=="" (
    echo No URL entered.
    pause
    exit /b 1
)

echo.
echo Cleaning old files...
del /q input\* 2>nul
del /q frames\* 2>nul
del /q bimg\* 2>nul
del /q output\* 2>nul

echo.
echo Downloading video...
yt-dlp -f "bv*+ba/b" -o "input\video.%%(ext)s" "%URL%"
if errorlevel 1 (
    echo yt-dlp failed.
    pause
    exit /b 1
)

set "VIDEOFILE="
for %%F in (input\video.*) do (
    set "VIDEOFILE=%%F"
)

if not defined VIDEOFILE (
    echo Downloaded video file not found.
    pause
    exit /b 1
)

echo.
echo Converting audio to DFPWM...
ffmpeg -y -i "%VIDEOFILE%" -ac 1 -ar 48000 -f dfpwm "output\audio.dfpwm"
if errorlevel 1 (
    echo Audio conversion failed.
    pause
    exit /b 1
)

echo.
echo Exporting frames...
ffmpeg -y -i "%VIDEOFILE%" -vf "fps=4,scale=164:81:flags=neighbor" "frames\%%04d.png"
if errorlevel 1 (
    echo Frame export failed.
    pause
    exit /b 1
)

echo.
echo Converting PNG frames to BIMG...
python png_to_bimg.py
if errorlevel 1 (
    echo PNG to BIMG conversion failed.
    pause
    exit /b 1
)

echo.
echo Copying BIMG frames to output...
copy /y bimg\*.bimg output\ >nul

echo.
echo Done.
echo.
echo Files are in:
echo %cd%\output
echo.
echo Upload audio.dfpwm and all .bimg files from output to your GitHub/server.
pause