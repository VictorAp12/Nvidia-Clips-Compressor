import subprocess
import json
import time
import os
import signal
from pathlib import Path
import sys


VIDEO_EXTS = (".mp4", ".mkv", ".mov")
AUDIO_BITRATE = "192k"
NVENC_PRESET = "p5"
CPU_PRESET = "medium"


def get_ffmpeg_path(name: str) -> str:
    if getattr(sys, "frozen", False):
        return str(Path(sys._MEIPASS) / "ffmpeg" / name)
    return str(Path("ffmpeg") / name)


def get_video_info(video_path):
    cmd = [
        get_ffmpeg_path("ffprobe.exe"),
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=height,duration",
        "-of",
        "json",
        str(video_path),
    ]

    r = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
    )

    if r.returncode != 0:
        raise RuntimeError(f"ffprobe failed for: {video_path}")

    data = json.loads(r.stdout)
    stream = data["streams"][0]

    height = int(stream.get("height", 1080))
    duration = float(stream.get("duration", 0))

    return height, duration


def cq_by_resolution(height):
    if height <= 720:
        return 23
    elif height <= 768:
        return 22
    else:
        return 21


def run_ffmpeg(cmd, duration, label, gui, index, total):
    start = time.time()

    startupinfo = None
    creationflags = 0

    if sys.platform == "win32":
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        creationflags = subprocess.CREATE_NO_WINDOW

    p = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        startupinfo=startupinfo,
        creationflags=creationflags,
    )

    gui.pause_btn["state"] = "normal"
    gui.cancel_btn["state"] = "normal"
    gui.current_file.set(label)

    for line in p.stdout:
        if gui.cancel_requested:
            p.terminate()
            return -1

        if gui.paused:
            os.kill(p.pid, signal.SIGSTOP)
            while gui.paused and not gui.cancel_requested:
                time.sleep(0.2)
            os.kill(p.pid, signal.SIGCONT)

        if line.startswith("out_time_ms"):
            v = line.split("=")[1].strip()
            if v == "N/A":
                continue

            t = int(v)
            percent = min(t / (duration * 1_000_000) * 100, 100)
            elapsed = time.time() - start
            eta = (elapsed / percent * (100 - percent)) if percent > 0 else None

            gui.file_progress.set(percent)
            gui.total_progress.set(((index - 1) / total * 100) + (percent / total))
            gui.eta_text.set(f"ETA: {eta:5.1f}s" if eta else "ETA: --")
            gui.root.update_idletasks()

    p.wait()
    gui.file_progress.set(100)
    return p.returncode
