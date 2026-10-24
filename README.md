<div align="center">

# Image2Spectrogram 🎵🖼️

**Hide an image inside an audio file. Open it in a spectrogram viewer and the picture appears.**

![License](https://img.shields.io/github/license/siratilotty/image2spectogram?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.9+-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

</div>

---

> 🎉 **After one years in beta, Image2Spectrogram has finally graduated and shipped its first stable release.**

## Overview

Image2Spectrogram is a small command-line tool that converts an image into a `.wav` file. The audio is synthesized so that its **spectrogram** (frequency over time) draws the original image.

Each image column becomes a short slice of audio, and each row becomes a sine wave at a specific frequency. Dark pixels switch their frequency on, light pixels leave it silent. Played back, it sounds like a burst of tones; viewed in a spectrogram, it reads as a picture.

```
image (pixels)  ──►  columns = time  ──►  rows = frequency  ──►  output.wav
```

## Features

- **Simple CLI:** pass an image, get a WAV. Every parameter is configurable.
- **Clean audio:** a Hann window is applied to every column to prevent clicks and pops at column boundaries.
- **High-quality resizing:** images are downscaled with Lanczos resampling to preserve detail.
- **Resolution guard:** warns you when the chosen height is finer than a spectrogram viewer can resolve.
- **Standard output:** 16-bit PCM WAV, 44.1 kHz by default.

## Requirements

- Python 3.9 or newer
- [NumPy](https://numpy.org/), [SciPy](https://scipy.org/) and [Pillow](https://python-pillow.org/)
- A spectrogram viewer, such as [Audacity](https://www.audacityteam.org/)

## Installation

```bash
git clone https://github.com/SirAtilotty/Image2Spectogram.git
cd Image2Spectogram/Image2Spectrogram
```

Create a virtual environment and install the dependencies:

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

> **Arch Linux and other distros with a managed Python:** `pip install` outside a virtual environment fails with `externally-managed-environment` (PEP 668). Use the venv above, or install the system packages with `sudo pacman -S python-numpy python-scipy python-pillow`.

## Usage

```bash
python spectrogram_text.py message.png
```

This writes `output.wav` to the current folder. Open it in Audacity, click the track name, choose **Spectrogram**, and your image shows up.

### Examples

```bash
# Custom output file
python spectrogram_text.py logo.png -o logo.wav

# Higher resolution (longer audio, finer detail)
python spectrogram_text.py logo.png --width 256 --height 96

# Wider frequency range and a lower tone threshold
python spectrogram_text.py logo.png --freq-start 200 --freq-end 10000 --threshold 0.4
```

### Options

| Option | Default | Description |
|---|---|---|
| `image` | required | Path to the source image. |
| `-o`, `--output` | `output.wav` | Output WAV file path. |
| `--width` | `128` | Image width in pixels after resizing. More width means longer audio. |
| `--height` | `64` | Image height in pixels after resizing. More height means finer detail and does not change the duration. |
| `--sample-rate` | `44100` | Audio sample rate in Hz. |
| `--duration-per-column` | `0.05` | Seconds of audio per image column. |
| `--freq-start` | `300` | Lowest frequency in Hz (bottom row of the image). |
| `--freq-end` | `8000` | Highest frequency in Hz (top row of the image). |
| `--threshold` | `0.5` | Minimum pixel intensity (0 to 1) that triggers a tone. |
| `--fft-size` | `2048` | FFT window of your spectrogram viewer. Only used for the resolution warning. |

Run `python spectrogram_text.py -h` for the full help text.

## Preparing your image

- **Dark on light.** Dark pixels produce tones and appear bright in the spectrogram, so use a dark subject on a white background.
- **High contrast.** Thick shapes, silhouettes and bold text survive downscaling. Thin lines and fine gradients get lost.
- **Match the aspect ratio.** The image is resized to `--width` x `--height`, so use the same ratio (the default 128x64 is 2:1) to avoid stretching. The source file can be any size at least as large as the target.
- **Keep the height reasonable.** Rows closer together than the viewer's frequency resolution blur into each other. With the defaults, about 358 rows is the practical ceiling, and the tool warns you if you go past it.

## How it works

1. The image is converted to grayscale, resized with Lanczos resampling, and inverted so dark pixels carry high intensity.
2. Columns map to time: each one lasts `--duration-per-column` seconds.
3. Rows map linearly to frequency between `--freq-start` and `--freq-end`.
4. For every column, a sine wave is added for each row whose intensity exceeds `--threshold`.
5. Each column is multiplied by a Hann window, concatenated, normalized and written as 16-bit PCM.

Total duration is `width x duration-per-column`, so the default 128 columns produce about 6.4 seconds of audio.

## Troubleshooting

| Problem | Fix |
|---|---|
| `error: the following arguments are required: image` | Pass the image path: `python spectrogram_text.py message.png`. |
| `externally-managed-environment` | Use a virtual environment (see Installation). |
| `Signal is silent` | The image produced no tones. Check that the subject is dark on a light background, or lower `--threshold`. |
| Image looks blurry or smeared in Audacity | Lower `--height`, or raise the window size in Audacity under *Spectrogram Settings*. |
| Image looks squashed | Make the source image match the aspect ratio of `--width` x `--height`. |

## Roadmap

- [ ] Optional logarithmic frequency scaling
- [ ] Preview of the resized image before synthesis
- [ ] Unit tests and CI

## License

Released under the **MIT License**. See [LICENSE](LICENSE) for details.

Copyright (c) 2026 Atilla İlhan.
