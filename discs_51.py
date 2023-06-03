#!/usr/bin/env python3

import math

import segno
from PIL import Image, ImageDraw, ImageFont

from regend.utils import mm_to_px, stickers, A4_HEIGHT, A4_WIDTH


DIAMETER = mm_to_px(51)
PITCH = mm_to_px(53)
MARGIN_LEFT = mm_to_px(26.5)
MARGIN_TOP = mm_to_px(17)

TOTAL = 13
PREFIX = "LL"
FONT_HEIGHT = 30


def draw_qr_code(page):
    # Draw QR tag.
    qr_code = segno.make(f"https://ishara.uk/{PREFIX}{n:02}")
    qr_code = qr_code.to_pil(scale=5)
    pos = (
        i * PITCH + MARGIN_LEFT + (DIAMETER - qr_code.width) // 2,
        j * PITCH + MARGIN_TOP + 10,
    )
    page.paste(qr_code, pos)


def draw_image(page):
    box = (
        i * PITCH + MARGIN_LEFT, j * PITCH + MARGIN_TOP,
        i * PITCH + DIAMETER + MARGIN_LEFT, j * PITCH + DIAMETER + MARGIN_TOP
    )

    image = Image.open(f"images/{PREFIX}/{PREFIX}13.png")
    min_size = min(image.width, image.height)
    crop_box = (
        (image.width - min_size) // 2,
        (image.height - min_size) // 2,
        (image.width - min_size) // 2 + min_size,
        (image.height - min_size) // 2 + min_size,
    )
    image = image.crop(crop_box).resize((DIAMETER, DIAMETER))
    page.paste(image, box)


def draw_circle(draw):
    box = (
        i * PITCH + MARGIN_LEFT, j * PITCH + MARGIN_TOP,
        i * PITCH + DIAMETER + MARGIN_LEFT, j * PITCH + DIAMETER + MARGIN_TOP
    )
    draw.ellipse(box, fill=None, outline=(0, 0, 0))


def draw_label(draw, color, background_color=None):
    label = f"{PREFIX}{n:02}"
    width = font.getlength(label)
    pos = (
        i * PITCH + MARGIN_LEFT + (DIAMETER - width) // 2,
        j * PITCH + MARGIN_TOP + (DIAMETER - 36),
    )
    if background_color is not None:
        draw.rectangle((pos[0] - 2, pos[1] - 1, pos[0] + width + 4, pos[1] + FONT_HEIGHT + 2),
                       fill=background_color, outline=None)
    draw.text(pos, label, font=font, fill=color)


if __name__ == "__main__":
    qr_page = Image.new("RGBA", (A4_WIDTH, A4_HEIGHT), (255, 255, 255, 255))
    qr_draw = ImageDraw.Draw(qr_page)
    im_page = Image.new("RGBA", (A4_WIDTH, A4_HEIGHT), (255, 255, 255, 255))
    im_draw = ImageDraw.Draw(im_page)
    font = ImageFont.truetype("./fonts/Helvetica-Bold.ttf", FONT_HEIGHT)

    for i, j, n in stickers(3, 5, TOTAL):
        draw_qr_code(qr_page)

    for i, j, n in stickers(3, 5, TOTAL):
        draw_image(im_page)

        draw_circle(qr_draw)
        draw_circle(im_draw)

        draw_label(qr_draw, color=(0, 0, 0))
        draw_label(im_draw, color=(200, 200, 200), background_color=(0, 0, 0))

    qr_page.save(f"output/{PREFIX}_qr_codes.png")
    im_page.save(f"output/{PREFIX}_images.png")
