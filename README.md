<div align="center">
  
  ![](https://img.shields.io/github/license/siratilotty/image2spectogram?style=for-the-badge)
  ![](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=white)
</div>

# Image2Spectrogram 🎵🖼️

**Image2Spectrogram** is a lightweight Python tool that encodes images into audio files. When the generated `.wav` file is viewed through a spectrogram analyzer, the original image is visually reconstructed within the frequencies.

> **Status:** This project is currently in **Beta** and under active development.

---

## ✨ Features

* **Visual Encoding:** Converts 2D pixel data into frequency-domain audio.
* **High-Quality Output:** Generates standard 16-bit PCM WAV files at a 44.1 kHz sample rate.
* **Frequency Mapping:** Encodes visual data within the human-audible range (300Hz - 8000Hz).

## 🛠️ Requirements

To run this project, you will need:

1. **Python 3.x**
2. **External Libraries:** `numpy`, `scipy`, and `Pillow` (PIL).
3. **Spectrogram Viewer:** An application like **Audacity** to visualize the output.

## 🚀 Installation & Usage

1. **Clone the repository:**
```bash
git clone https://github.com/SirAtilotty/Image2Spectogram.git
cd Image2Spectogram

```


2. **Install dependencies:**
```bash
pip install numpy scipy pillow

```


3. **Prepare your image:**
* The image must be named `message.png`.
* It must be placed in the same folder as the script.
* For best results, use a high-contrast black and white image (white subject on a black background).
* **Note:** The current version automatically resizes input images to **64x16** pixels.


4. **Run the script:**
```bash
python spectrogram_text.py

```


5. **View the result:**
Open `output.wav` in Audacity, click on the track name, and select **Spectrogram** view to see your image.

## ⚙️ Technical Specs

* **Sample Rate:** 44100 Hz
* **Duration per Pixel Column:** 0.05s
* **Frequency Range:** 300 Hz to 8000 Hz
* **Intensity Threshold:** > 0.5 (for pixel-to-frequency triggering)

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.
Copyright (c) 2026 Atilla İlhan.
