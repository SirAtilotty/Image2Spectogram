
"""
spectrogram_text.py

Encodes a grayscale image into a WAV file such that opening the result
in a spectrogram viewer (e.g. Audacity) visually reconstructs the image.

Usage:
    python spectrogram_text.py message.png
    python spectrogram_text.py message.png -o output.wav --width 64 --height 16
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.io.wavfile import write as write_wav

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def load_image(path: Path, width: int, height: int) -> np.ndarray:
    """Load an image, convert to grayscale, resize, and normalize to [0, 1]."""
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")


    img = Image.open(path).convert("L").resize((width, height), Image.Resampling.LANCZOS)
    arr = np.array(img, dtype=np.float64)


    normalized = 1.0 - arr / 255.0
    return np.flipud(normalized)


def image_to_signal(
    img_norm: np.ndarray,
    sample_rate: int,
    duration_per_column: float,
    freq_start: float,
    freq_end: float,
    intensity_threshold: float,
) -> np.ndarray:
    """Convert a normalized image array into an audio signal.

    Each column becomes a short audio segment; each row within a column
    becomes a sine wave at a frequency proportional to its vertical
    position, added only if the pixel's intensity exceeds the threshold.
    A Hann window is applied per column to avoid audible clicks/pops at
    column boundaries (a common artifact in the naive version).
    """
    num_rows, num_cols = img_norm.shape
    samples_per_col = int(sample_rate * duration_per_column)
    t = np.linspace(0, duration_per_column, samples_per_col, endpoint=False)
    window = np.hanning(samples_per_col)

    signal = np.zeros(samples_per_col * num_cols)

    for col in range(num_cols):
        column_signal = np.zeros(samples_per_col)
        active_rows = np.where(img_norm[:, col] > intensity_threshold)[0]

        for row in active_rows:
            freq = freq_start + (freq_end - freq_start) * (row / (num_rows - 1))
            column_signal += np.sin(2 * np.pi * freq * t)

        column_signal *= window  
        start = col * samples_per_col
        signal[start:start + samples_per_col] = column_signal

    return signal


def normalize_and_save(signal: np.ndarray, sample_rate: int, output_path: Path) -> None:
    """Normalize a signal to [-1, 1] and write it out as a 16-bit PCM WAV."""
    peak = np.max(np.abs(signal))
    if peak == 0:
        raise ValueError("Signal is silent (image produced no audio content).")

    signal = signal / peak
    write_wav(output_path, sample_rate, (signal * 32767).astype(np.int16))


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path, help="Path to the source image.")
    parser.add_argument("-o", "--output", type=Path, default=Path("output.wav"),
                         help="Path to write the output WAV file (default: output.wav).")
    parser.add_argument("--width", type=int, default=128,
                         help="Resize width in pixels (default: 128). More width = longer audio.")
    parser.add_argument("--height", type=int, default=64,
                         help="Resize height in pixels (default: 64). More height = finer detail, "
                              "no effect on duration -- but see --fft-size.")
    parser.add_argument("--sample-rate", type=int, default=44100, help="Audio sample rate in Hz.")
    parser.add_argument("--duration-per-column", type=float, default=0.05,
                         help="Seconds of audio per image column.")
    parser.add_argument("--freq-start", type=float, default=300.0, help="Lowest frequency in Hz.")
    parser.add_argument("--freq-end", type=float, default=8000.0, help="Highest frequency in Hz.")
    parser.add_argument("--threshold", type=float, default=0.5,
                         help="Minimum pixel intensity (0-1) to trigger a tone.")
    parser.add_argument("--fft-size", type=int, default=2048,
                         help="FFT window size your spectrogram viewer uses (Audacity default: 2048). "
                              "Used only to warn you if --height is set higher than the viewer can "
                              "actually resolve, given --sample-rate and the frequency range.")
    return parser.parse_args(argv)


def warn_if_height_too_fine(height: int, freq_start: float, freq_end: float,
                             sample_rate: int, fft_size: int) -> None:
    """Log a warning if the chosen height packs rows closer together than the
    viewer's FFT bin width can distinguish -- those extra rows would just
    blur together in the spectrogram instead of adding real detail."""
    bin_width = sample_rate / fft_size
    row_spacing = (freq_end - freq_start) / max(height - 1, 1)
    if row_spacing < bin_width:
        max_height = int((freq_end - freq_start) / bin_width) + 1
        logger.warning(
            "height=%d packs rows %.1f Hz apart, finer than your viewer's ~%.1f Hz "
            "resolution at fft-size=%d. Rows will blur together; ~%d is the practical max.",
            height, row_spacing, bin_width, fft_size, max_height,
        )


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    try:
        warn_if_height_too_fine(args.height, args.freq_start, args.freq_end,
                                 args.sample_rate, args.fft_size)

        logger.info("Loading image: %s", args.image)
        img_norm = load_image(args.image, args.width, args.height)

        logger.info("Synthesizing audio (%d columns, %.0f Hz - %.0f Hz)...",
                    img_norm.shape[1], args.freq_start, args.freq_end)
        signal = image_to_signal(
            img_norm,
            args.sample_rate,
            args.duration_per_column,
            args.freq_start,
            args.freq_end,
            args.threshold,
        )

        normalize_and_save(signal, args.sample_rate, args.output)
        logger.info("Done -> %s (open it in a spectrogram viewer, e.g. Audacity)", args.output)
        return 0

    except (FileNotFoundError, ValueError) as exc:
        logger.error(str(exc))
        return 1


if __name__ == "__main__":
    sys.exit(main())
