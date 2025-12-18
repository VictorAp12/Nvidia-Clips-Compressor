@echo off
pyinstaller ^
  --onefile ^
  --noconsole ^
  --name "Nvidia Clips Compressor (NVENC)" ^
  --icon app.ico ^
  --add-data "app.ico;." ^
  --add-binary "ffmpeg\ffmpeg.exe;ffmpeg" ^
  --add-binary "ffmpeg\ffprobe.exe;ffmpeg" ^
  main.py
pause
