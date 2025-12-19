# Nvidia Clips Compressor (NVENC)

A fast and lightweight video compressor focused on gameplay clips,
built around NVIDIA NVENC for maximum speed and efficiency.

The application reduces file size while preserving visual quality,
resolution, frame rate and metadata. It is optimized for high-FPS
gameplay footage, but can also be used with any standard video file.

<img width="492" height="282" alt="image" src="https://github.com/user-attachments/assets/0dc41f27-d6bf-4877-8b48-6044285bd911" />


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

## Target Use Case

This project is primarily intended for:

- NVIDIA gameplay clips (NVIDIA App / GeForce Experience)
- Game recordings (Fortnite, CS2, Valorant, PES, etc.)
- High FPS video footage (60–144 FPS)

It also works with any standard video file, but gameplay clips are the main focus.

## Video Encoding Strategy

### Default codec
- **H.264 NVENC** (fastest, maximum compatibility)

### Optional codec
- **H.265 / HEVC NVENC** (smaller files, slightly slower)

The codec can be selected directly in the GUI.

If an NVIDIA GPU with NVENC support is not detected, the application
automatically switches to CPU-based encoding.

## Quality Control (CQ)

Instead of fixed bitrates, the application uses **Constant Quality (CQ)**,
similar in concept to CRF in HandBrake:

- Complex scenes receive more bits
- Simple scenes receive fewer bits
- Better size-to-quality ratio than fixed bitrates

CQ values are automatically selected based on video resolution.

This approach avoids wasting bitrate on lower resolutions while maintaining
good visual quality for high-resolution gameplay footage.

## Performance Notes

- **NVIDIA GPU required for NVENC acceleration**
- On NVIDIA GPUs:
- Encoding is GPU-based
- CPU usage is minimal
- Much faster than HandBrake
- On non-NVIDIA systems:
- CPU encoding is used
- Performance will be slower

The application prioritizes speed and practicality over heavy filtering.

## Requirements

- Windows
- **NVIDIA GPU with NVENC support for GPU acceleration**
- Works on non-NVIDIA systems using CPU encoding
- No external FFmpeg installation required (FFmpeg is embedded)


## Installation

  ### Windows Installer

  The easiest way to install the application is by using the **Windows installer**.

  1. Go to the **Releases** page on GitHub
  2. Download the latest installer:
  3. Run the installer
  4. Follow the setup wizard

  The installer will:
  - Install the application in a folder selected by the user
  - Create Start Menu shortcuts
  - Optionally create a Desktop shortcut
  - Include all required dependencies (FFmpeg is embedded)

  No Python or external tools are required.

  ### Build executable

  These steps are only required if you want to build the application yourself.

  ```bash
  pip install pyinstaller
  build_exe.bat
  ```

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
