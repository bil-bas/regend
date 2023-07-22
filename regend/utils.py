import polib
from PIL import ImageFont, ImageDraw

MM_TO_PX = 3.7795275591
FONT_HEIGHT_QR = 26
FONT_HEIGHT_ACTION = 16


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


def draw_circle(draw: ImageDraw, i: int, j: int, diameter: int, pitch: int, margin_left: int, margin_top: int):
    draw.ellipse((
            i * pitch + margin_left, j * pitch + margin_top,
            i * pitch + diameter + margin_left, j * pitch + diameter + margin_top
        ),
        fill=None,
        outline=(0, 0, 0),
        width=LINE_WIDTH,
    )


def get_wrapped_text(text: str, font: ImageFont, line_length: int):
    lines = ['']
    for word in text.split():
        line = f'{lines[-1]} {word}'.strip()
        if font.getlength(line) <= line_length:
            lines[-1] = line
        else:
            lines.append(word)

    return lines
