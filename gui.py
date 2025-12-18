import sys
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, ttk
from config import load_config, save_config


class AppGUI:
    def __init__(self):
        self.cfg = load_config()

        self.root = tk.Tk()
        self.root.title("Nvidia Clips Compressor (NVENC)")
        self.root.resizable(False, False)

        if getattr(sys, "frozen", False):
            icon_path = Path(sys._MEIPASS) / "app.ico"
        else:
            icon_path = Path("app.ico")

        if icon_path.exists():
            self.root.iconbitmap(icon_path)

        self.cancel_requested = False
        self.paused = False

        self.start_callback = None

        # Settings
        self.input_dir = tk.StringVar(value=self.cfg.get("last_input", ""))
        self.output_dir = tk.StringVar(value=self.cfg.get("last_output", ""))
        self.recursive = tk.BooleanVar(value=self.cfg.get("recursive", False))
        self.overwrite = tk.BooleanVar(value=self.cfg.get("overwrite", False))
        self.video_codec = tk.StringVar(value="h264")

        # Status
        self.current_file = tk.StringVar(value="Waiting…")
        self.file_progress = tk.DoubleVar(value=0)
        self.total_progress = tk.DoubleVar(value=0)
        self.eta_text = tk.StringVar(value="ETA: --")

        self.setup_theme()
        self.build()

    def setup_theme(self):
        self.root.configure(bg="#1e1e1e")
        style = ttk.Style(self.root)
        style.theme_use("default")

        style.configure(".", background="#1e1e1e", foreground="white")
        style.configure("TProgressbar", troughcolor="#333333", background="#4caf50")

        style.configure(
            "TEntry",
            foreground="black",
            fieldbackground="white",
            background="white",
        )
        style.map(
            "TEntry",
            fieldbackground=[("readonly", "white")],
            foreground=[("disabled", "#a0a0a0")],
        )

        style.map(
            "TButton",
            background=[("active", "#2a72d4"), ("!active", "#2d2d2d")],
            foreground=[("active", "white"), ("!active", "white")],
        )
        style.map(
            "TCheckbutton",
            foreground=[("active", "#8ab4f8"), ("!active", "white")],
        )

        style.configure(
            "TCombobox",
            foreground="black",
            fieldbackground="white",
            background="white",
        )

        style.map(
            "TCombobox",
            fieldbackground=[("readonly", "white")],
            foreground=[("readonly", "black")],
        )

    def build(self):
        pad = {"padx": 10, "pady": 5}

        ttk.Label(self.root, text="Input folder").grid(row=0, column=0, **pad)
        ttk.Entry(self.root, textvariable=self.input_dir, width=45).grid(
            row=0, column=1
        )
        ttk.Button(self.root, text="Browse", command=self.select_input).grid(
            row=0, column=2
        )

        ttk.Label(self.root, text="Output folder").grid(row=1, column=0, **pad)
        ttk.Entry(self.root, textvariable=self.output_dir, width=45).grid(
            row=1, column=1
        )
        ttk.Button(self.root, text="Browse", command=self.select_output).grid(
            row=1, column=2
        )

        ttk.Checkbutton(
            self.root, text="Process subfolders", variable=self.recursive
        ).grid(row=2, column=1, sticky="w")

        ttk.Checkbutton(
            self.root, text="Overwrite existing files", variable=self.overwrite
        ).grid(row=3, column=1, sticky="w")

        ttk.Label(self.root, text="Video codec").grid(row=4, column=0, padx=10, pady=5)

        ttk.Combobox(
            self.root,
            textvariable=self.video_codec,
            values=["h264", "h265"],
            state="readonly",
            width=10,
        ).grid(row=4, column=1, sticky="w")

        self.start_btn = ttk.Button(self.root, text="Start", command=self.start)
        self.start_btn.grid(row=5, column=1)

        self.pause_btn = ttk.Button(
            self.root, text="Pause", command=self.toggle_pause, state="disabled"
        )
        self.pause_btn.grid(row=5, column=2)

        self.cancel_btn = ttk.Button(
            self.root, text="Cancel", command=self.cancel, state="disabled"
        )
        self.cancel_btn.grid(row=5, column=3)

        ttk.Label(self.root, textvariable=self.current_file).grid(
            row=6, column=0, columnspan=4, sticky="w", **pad
        )
        ttk.Progressbar(self.root, length=420, variable=self.file_progress).grid(
            row=7, column=0, columnspan=4, **pad
        )
        ttk.Progressbar(self.root, length=420, variable=self.total_progress).grid(
            row=8, column=0, columnspan=4, **pad
        )
        ttk.Label(self.root, textvariable=self.eta_text).grid(
            row=9, column=0, columnspan=4, sticky="w", **pad
        )

    def start(self):
        self.cfg.update(
            {
                "recursive": self.recursive.get(),
                "overwrite": self.overwrite.get(),
                "last_input": self.input_dir.get(),
                "last_output": self.output_dir.get(),
            }
        )
        save_config(self.cfg)

        self.cancel_requested = False
        self.paused = False

        self.start_btn["state"] = "disabled"
        self.pause_btn["state"] = "normal"
        self.cancel_btn["state"] = "normal"

        if callable(self.start_callback):
            self.start_callback()

    def toggle_pause(self):
        self.paused = not self.paused
        self.pause_btn.config(text="Resume" if self.paused else "Pause")

    def cancel(self):
        self.cancel_requested = True

    def select_input(self):
        path = filedialog.askdirectory()
        if path:
            self.input_dir.set(path)

    def select_output(self):
        path = filedialog.askdirectory()
        if path:
            self.output_dir.set(path)
