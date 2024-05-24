import subprocess
from contextlib import contextmanager
import re
from tempfile import TemporaryDirectory
import platform
import os

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
            with TemporaryDirectory() as folder:
                svg_file = os.path.join(folder, "tmp.svg")
                page.save_svg(svg_file)
                args = [
                    inkscape_path(),
                    svg_file,
                    f"--export-filename=./output/{name}.pdf",
                ]
                subprocess.check_call(args)

        elif fmt == "png":
            # Assume this doesn't have exotic fonts.
            page.save_png(f"./output/{name}.png")
        elif fmt == "svg":
            # This will be fine regardless of whether it includes exotic fonts.
            page.save_svg(f"./output/{name}.svg")
        else:
            raise ValueError(f"Bad format: {fmt}")


def icon(name):
    return f"./images/icons/{name}.png"


def inkscape_path():
    if platform.system() == "Windows":
        return "C:\\Program Files\\Inkscape\\bin\\inkscape.exe"
    elif platform.system() == "Linux":
        return "/usr/bin/inkscape"
    else:
        raise


def font_from_language(language_code):
    if language_code == "or":
        return "Noto Sans Oriya"
    else:
        return "Arimo"
