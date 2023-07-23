import math

from PIL import Image, ImageDraw

from .utils import mm_to_px, A4_WIDTH, A4_HEIGHT, stickers

DIAMETER = mm_to_px(51)
PITCH = mm_to_px(56)
MARGIN_TOP = mm_to_px(6)
MARGIN_LEFT = mm_to_px(20)
LINE_WIDTH = 6


def draw_circles(prefix: str, num_tasks: int) -> None:
    page = Image.new("RGBA", (A4_WIDTH, A4_HEIGHT), (255, 255, 255, 255))
    draw = ImageDraw.Draw(page)

    for i, j, _ in stickers(3, 5, num_tasks + 2):
        x, y = MARGIN_LEFT + (i + 0.5) * PITCH, MARGIN_TOP + (j + 0.5) * PITCH
        box = (x - DIAMETER / 2, y - DIAMETER / 2, x + DIAMETER / 2, y + DIAMETER / 2)
        draw.ellipse(box, fill=None, outline=(0, 0, 0), width=LINE_WIDTH)

    page.save(f"./output/{prefix}_board_tasks.png")
