

import math
from PIL import Image, ImageDraw

from .utils import mm_to_px, A4_WIDTH, A4_HEIGHT, LINE_WIDTH


RADIUS = mm_to_px(70)
CENTER_X, CENTER_Y = 400, 400
ICONS = ["joker", "qr", "qr", "evaluate", "qr", "link", "qr", "evaluate", "qr", "qr", "link", "qr"]


def draw_icon(page, icon, i):
    angle = math.pi + 2 * math.pi * i / len(ICONS)
    icon = icon.rotate(math.degrees(angle + math.pi), fillcolor=(255, 255, 255), expand=True)
    x = round(CENTER_X + math.sin(angle) * RADIUS - icon.width / 2)
    y = round(CENTER_Y + math.cos(angle) * RADIUS - icon.height / 2)
    page.paste(icon, (x, y))


def draw_line(draw, i):
    angle = math.pi + 2 * math.pi * (i + 0.5) / len(ICONS)
    x1 = round(CENTER_X + math.sin(angle) * RADIUS * 0.7)
    y1 = round(CENTER_Y + math.cos(angle) * RADIUS * 0.7)
    x2 = round(CENTER_X + math.sin(angle) * RADIUS * 1.3)
    y2 = round(CENTER_Y + math.cos(angle) * RADIUS * 1.3)
    draw.line((x1, y1, x2, y2), fill=(200, 50, 50), width=LINE_WIDTH)


def draw_spinner():
    icons = {name: Image.open(f"./images/icons/{name}.png") for name in set(ICONS)}

    page = Image.new("RGBA", (A4_WIDTH, A4_HEIGHT), (255, 255, 255, 255))
    draw = ImageDraw.Draw(page)

    for i, icon in enumerate(ICONS):
        draw_icon(page, icons[icon], i)
        draw_line(draw, i)

    page.save("./output/spinner_icons.png")


if __name__ == "__main__":
    draw_spinner()
