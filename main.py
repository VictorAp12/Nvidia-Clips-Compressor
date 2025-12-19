from pathlib import Path
import os
import threading
import time
from gui import AppGUI
from ffmpeg_utils import (
    VIDEO_EXTS,
    get_video_info,
    cq_by_resolution,
    run_ffmpeg,
    get_ffmpeg_path,
)
from tkinter import messagebox


def collect_videos(folder, recursive):
    if recursive:
        return [p for p in folder.rglob("*") if p.suffix.lower() in VIDEO_EXTS]
    return [p for p in folder.iterdir() if p.suffix.lower() in VIDEO_EXTS]


def worker(input_dir, output_dir, recursive, overwrite, gui):
    videos = collect_videos(input_dir, recursive)
    total = len(videos)

    same_folder = input_dir.resolve() == output_dir.resolve()

    for i, video in enumerate(videos, 1):
        if gui.cancel_requested:
            break

        rel = video.relative_to(input_dir)
        out = output_dir / rel
        out.parent.mkdir(parents=True, exist_ok=True)

        if out.exists() and not overwrite and not same_folder:
            continue

        if same_folder:
            temp_out = out.with_suffix(".tmp.mp4")
            final_out = out
        else:
            temp_out = out
            final_out = out

        try:
            height, duration = get_video_info(video)
        except Exception:
            height, duration = 1080, 0

        cq = cq_by_resolution(height)
        label = f"[{i}/{total}] {video.name}"

        codec = gui.video_codec.get()  # "h264" or "h265"

        if codec == "h265":
            nvenc = [
                get_ffmpeg_path("ffmpeg"),
                "-y",
                "-hwaccel",
                "cuda",
                "-hwaccel_output_format",
                "cuda",
                "-i",
                str(video),
                "-map_metadata",
                "0",
                "-c:v",
                "hevc_nvenc",
                "-preset",
                "p5",
                "-rc",
                "vbr_hq",
                "-cq:v",
                str(cq),
                "-profile:v",
                "main",
                "-pix_fmt",
                "yuv420p",
                "-c:a",
                "aac",
                "-b:a",
                "160k",
                "-progress",
                "pipe:1",
                "-nostats",
                str(temp_out),
            ]
        else:
            # H.264 (Default, faster)
            nvenc = [
                get_ffmpeg_path("ffmpeg"),
                "-y",
                "-hwaccel",
                "cuda",
                "-hwaccel_output_format",
                "cuda",
                "-i",
                str(video),
                "-map_metadata",
                "0",
                "-c:v",
                "h264_nvenc",
                "-preset",
                "p5",
                "-rc",
                "vbr",
                "-cq:v",
                str(cq),
                "-profile:v",
                "high",
                "-pix_fmt",
                "yuv420p",
                "-c:a",
                "aac",
                "-b:a",
                "160k",
                "-progress",
                "pipe:1",
                "-nostats",
                str(temp_out),
            ]

        # try GPU
        if run_ffmpeg(nvenc, duration, label, gui, i, total) != 0:
            # fallback CPU (security)
            cpu = [
                get_ffmpeg_path("ffmpeg"),
                "-y",
                "-i",
                str(video),
                "-map_metadata",
                "0",
                "-c:v",
                "libx264",
                "-preset",
                "medium",
                "-crf",
                str(cq + 2),
                "-profile:v",
                "high",
                "-pix_fmt",
                "yuv420p",
                "-c:a",
                "aac",
                "-b:a",
                "160k",
                "-progress",
                "pipe:1",
                "-nostats",
                str(temp_out),
            ]
            run_ffmpeg(cpu, duration, label, gui, i, total)

        if same_folder and temp_out.exists():
            for _ in range(10):
                try:
                    if final_out.exists():
                        final_out.unlink()
                    temp_out.replace(final_out)
                    break
                except PermissionError:
                    time.sleep(0.2)


    gui.start_btn["state"] = "normal"
    gui.pause_btn["state"] = "disabled"
    gui.cancel_btn["state"] = "disabled"

    gui.file_progress.set(0)
    gui.total_progress.set(0)
    gui.current_file.set("Finished. Select another folder and click Start.")

    if not gui.cancel_requested:
        os.startfile(output_dir)


if __name__ == "__main__":
    gui = AppGUI()

    def start_processing():
        # RESET obrigatório
        gui.cancel_requested = False
        gui.paused = False

        inp = Path(gui.input_dir.get())
        out = Path(gui.output_dir.get())
        rec = gui.recursive.get()
        over = gui.overwrite.get()

        # -------- VALIDATIONS --------

        if not inp.exists() or not inp.is_dir():
            messagebox.showerror(
                "Invalid input folder", "The selected input folder does not exist."
            )
            gui.start_btn["state"] = "normal"
            return

        if not out.exists() or not out.is_dir():
            messagebox.showerror(
                "Invalid output folder", "The selected output folder does not exist."
            )
            gui.start_btn["state"] = "normal"
            return

        videos = collect_videos(inp, rec)
        if not videos:
            messagebox.showinfo(
                "No videos found",
                "No supported video files were found in the selected input folder.",
            )
            gui.start_btn["state"] = "normal"
            return

        # -------- START THREAD --------
        t = threading.Thread(
            target=worker,
            args=(inp, out, rec, over, gui),
            daemon=True,
        )
        t.start()

    gui.start_callback = start_processing
    gui.root.mainloop()
