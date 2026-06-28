#!/usr/bin/env python3
"""Convert a P5 (binary grayscale) PGM image to PNG."""

from __future__ import annotations

import argparse
import struct
from pathlib import Path

from PIL import Image


def read_p5(path: Path) -> Image.Image:
    with path.open("rb") as f:
        magic = f.readline().strip()
        if magic != b"P5":
            raise ValueError(f"{path}: expected P5 PGM, got {magic!r}")

        # Skip comment lines.
        line = f.readline()
        while line.startswith(b"#"):
            line = f.readline()

        width, height = map(int, line.split())
        maxval = int(f.readline().strip())

        if maxval <= 255:
            data = f.read(width * height)
            if len(data) != width * height:
                raise ValueError(f"{path}: expected {width * height} bytes, got {len(data)}")
            return Image.frombytes("L", (width, height), data)

        # 16-bit PGM from mandelbrot (little-endian short, native layout).
        count = width * height
        raw = f.read(count * 2)
        if len(raw) != count * 2:
            raise ValueError(f"{path}: expected {count * 2} bytes, got {len(raw)}")
        pixels = struct.unpack(f"<{count}H", raw)
        scale = 255.0 / maxval
        bytes8 = bytes(min(255, int(v * scale)) for v in pixels)
        return Image.frombytes("L", (width, height), bytes8)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Convert PGM (P5) to PNG")
    parser.add_argument(
        "input",
        nargs="?",
        default=root / "plots" / "mandelbrot_set.pgm",
        type=Path,
        help="Input .pgm file (default: plots/mandelbrot_set.pgm)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output .png file (default: same name as input, .png extension)",
    )
    args = parser.parse_args()

    input_path = args.input.resolve()
    output_path = (args.output or input_path.with_suffix(".png")).resolve()

    image = read_p5(input_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()