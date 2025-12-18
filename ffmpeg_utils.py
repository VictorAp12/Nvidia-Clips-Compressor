import subprocess
import json
import time
import os
import signal

VIDEO_EXTS = (".mp4", ".mkv", ".mov")
AUDIO_BITRATE = "192k"
NVENC_PRESET = "p5"
CPU_PRESET = "medium"


def get_video_info(video):
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=height,duration",
        "-of",
        "json",
        str(video),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, check=True)
    s = json.loads(r.stdout)["streams"][0]
    return int(s["height"]), float(s["duration"])


def cq_by_resolution(height):
    if height <= 720:
        return 23
    elif height <= 768:
        return 22
    else:
        return 21


def run_ffmpeg(cmd, duration, label, gui, index, total):
    start = time.time()
    p = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True
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
