import subprocess
from contextlib import contextmanager
import base64

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
def create_page(name, format: str, language_code: str = None, width: int = A4_WIDTH, height: int = A4_HEIGHT):
    assert format in ("svg", "png", "pdf")

    font_family = font_from_language(language_code) if language_code else None

    page = svg.Drawing(width, height, font_family=font_family)
    if font_family is not None:
        page.embed_google_font(font_family)

    yield page

    if format == "pdf":
        cairosvg.svg2pdf(page.as_svg(), write_to=f"./output/{name}.pdf")
    elif format == "png":
        cairosvg.svg2png(page.as_svg(), write_to=f"./output/{name}.png")
    else:
        page.save_svg(f"./output/{name}.svg")


def icon(name):
    return f"./images/icons/{name}.png"


def font_from_language(language_code):
    if language_code == "or":
        return "Noto Sans Oriya"
    else:
        return "Arimo"
