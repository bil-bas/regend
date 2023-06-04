#!/usr/bin/env python3

from PIL import Image, ImageDraw

from regend.utils import mm_to_px, stickers, draw_circle, A4_WIDTH, A4_HEIGHT


DIAMETER = mm_to_px(37)
PITCH = mm_to_px(39)
MARGIN_LEFT = mm_to_px(8.5)
MARGIN_TOP = mm_to_px(13)


def draw_icon(page, icons, i, j):
    if j in {0, 1, 2, 3}:
        icon = icons["link"]
    else:
        icon = icons["evaluate"]

    x = i * PITCH + MARGIN_LEFT + round((DIAMETER - icon.width) / 2)
    y = j * PITCH + MARGIN_TOP + round((DIAMETER - icon.height) / 2)
    page.paste(icon, (x, y))


def draw_discs():
    icons = {
        "link": Image.open("./images/link.png"),
        "evaluate": Image.open("./images/evaluate.png"),
    }

    page = Image.new("RGBA", (A4_WIDTH, A4_HEIGHT), (255, 255, 255, 255))
    draw = ImageDraw.Draw(page)

    for i, j, _ in stickers(5, 7):
        #draw_circle(draw, i, j, diameter=DIAMETER, pitch=PITCH, margin_top=MARGIN_TOP, margin_left=MARGIN_LEFT)
        draw_icon(page, icons, i, j)

    page.save("./output/37.png")


if __name__ == "__main__":
    draw_discs()
