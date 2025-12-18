# Nvidia Clips Compressor (NVENC)

A fast and lightweight video compressor focused on gameplay clips,
built around NVIDIA NVENC for maximum speed and efficiency.

The application reduces file size while preserving visual quality,
resolution, frame rate and metadata. It is optimized for high-FPS
gameplay footage, but can also be used with any standard video file.

<img width="492" height="282" alt="image" src="https://github.com/user-attachments/assets/0dc41f27-d6bf-4877-8b48-6044285bd911" />

---

## Features

- GPU-accelerated encoding using **NVIDIA NVENC** (NVIDIA GPUs only)
- Automatic fallback to **CPU encoding** when NVENC is not available
- H.264 (default, fastest) and H.265 / HEVC (optional) support
- Batch processing (input folder → output folder)
- Optional recursive folder processing
- Skip or overwrite existing files
- Safe overwrite when input and output folders are the same
- Preserves resolution, frame rate and metadata
- Pause, resume and cancel during processing
- Dark mode Windows GUI
- Significantly faster than HandBrake on NVIDIA GPUs

---

## Target Use Case

This project is primarily intended for:

- NVIDIA gameplay clips (NVIDIA App / GeForce Experience)
- Game recordings (Fortnite, CS2, Valorant, PES, etc.)
- High FPS video footage (60–144 FPS)

It also works with any standard video file, but gameplay clips are the main focus.

## Installation

  ### As a Python Project

  - Download the project as a zip or using git clone https://github.com/VictorAp12/Nvidia-Clips-Compressor.git

  - Create a virtual environment in the project folder:
    ```bash
    python -m venv venv
    ````

  - Activate the virtual environment in the project folder:
    ```bash
    venv\Scripts\activate
    ```

  - Install the project dependencies:
    ```bash
    pip install -r requirements.txt
    ```

  - Run the main.py:
    ```bash
    python -m main
    ```
