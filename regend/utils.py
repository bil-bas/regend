import subprocess

import polib
from PIL import ImageFont, ImageDraw, ImageOps, Image

MM_TO_PX = 3.7795275591
FONT_HEIGHT_LARGE = 26
FONT_HEIGHT_SMALL = 16


def mm_to_px(mm: float) -> int:
    return round(mm * MM_TO_PX)


A4_WIDTH, A4_HEIGHT = mm_to_px(210), mm_to_px(297)
LINE_WIDTH = 2


def stickers(x: int, y: int, limit: int = None) -> (int, int, int):
    for j in range(y):
        for i in range(x):
            n = i + j * x + 1

            if limit is not None and n > limit:
                return

            yield i, j, n


def draw_circle(draw: ImageDraw, diameter: int, offset: int) -> None:
    draw.ellipse(
        (offset, offset, diameter, diameter),
        fill=None,
        outline=(0, 0, 0),
        width=LINE_WIDTH,
    )


def get_wrapped_text(text: str, font: ImageFont, line_length: int) -> [str]:
    lines = ['']
    for word in text.split():
        line = f'{lines[-1]} {word}'.strip()
        if font.getlength(line) <= line_length:
            lines[-1] = line
        else:
            lines.append(word)

    return lines


def svg_to_png(in_file: str) -> None:
    out_file = in_file.replace(".svg", "") + ".png"

    subprocess.check_call(["inkscape", f"--export-png=output/{out_file}", f"designs/{in_file}"])
