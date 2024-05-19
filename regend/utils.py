import subprocess
from contextlib import contextmanager
import re
from tempfile import NamedTemporaryFile
import os

import cairosvg
import drawsvg as svg

MM_TO_PX = 3.7795275591
FONT_HEIGHT_LARGE = 26
FONT_HEIGHT_SMALL = 16


class Color:
    CUT = "darkblue"
    ENGRAVE = "black"
    SCORE = "magenta"
    BACKGROUND = "white"

    DRAW = "black"


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


def svg_to_png(in_file: str) -> None:
    out_file = in_file.replace(".svg", "") + ".png"

    subprocess.check_call(["inkscape", f"--export-png=output/{out_file}", f"designs/{in_file}"])


@contextmanager
def create_page(name, format_: str, language_code: str = None, width: int = A4_WIDTH, height: int = A4_HEIGHT):
    font_family = font_from_language(language_code) if language_code else None

    page = svg.Drawing(width, height, font_family=font_family)
    if font_family is not None:
        page.append_css(f"@import url('https://fonts.googleapis.com/css2?family={font_family}:ital,wght@0,400..700;1,400..700&display=swap');")

    yield page

    for fmt in re.split(r"\s*,\s*", format_.lower()):
        if fmt == "pdf":
            # Assume this MIGHT have exotic fonts.
            with NamedTemporaryFile(suffix=".svg") as f:
                page.save_svg(f.name)
                subprocess.check_call([
                    inkscape_path(),
                    f"--file={f.name}",
                    f"--export-pdf=./output/{name}.pdf",
                ])
        elif fmt == "png":
            # Assume this doesn't have exotic fonts.
            cairosvg.svg2png(page.as_svg(), write_to=f"./output/{name}.png")
        elif fmt == "svg":
            # This will be fine regardless of whether it includes exotic fonts.
            page.save_svg(f"./output/{name}.svg")
        else:
            raise ValueError(f"Bad format: {fmt}")


def icon(name):
    return f"./images/icons/{name}.png"


def inkscape_path():
    return "/usr/bin/inkscape"


def font_from_language(language_code):
    if language_code == "or":
        return "Noto Sans Oriya"
    else:
        return "Arimo"
