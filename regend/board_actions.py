import math

from PIL import Image, ImageDraw

from .utils import mm_to_px, A4_WIDTH, A4_HEIGHT

DIAMETER = mm_to_px(37)
LINE_WIDTH = 6


def draw_circles() -> None:
    page = Image.new("RGBA", (A4_WIDTH, A4_HEIGHT), (255, 255, 255, 255))
    draw = ImageDraw.Draw(page)

    for n in range(7):
        x, y = ((A4_WIDTH / 2 + math.cos(math.pi * n / 3.5) * A4_WIDTH / 3,
                 A4_HEIGHT / 2 + math.sin(math.pi * n / 3.5) * A4_WIDTH / 3))
        box = (x - DIAMETER / 2, y - DIAMETER / 2, x + DIAMETER / 2, y + DIAMETER / 2)
        draw.ellipse(box, fill=None, outline=(0, 0, 0), width=LINE_WIDTH)

    page.save(f"./output/board_actions.png")
