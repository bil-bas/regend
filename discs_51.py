#!/usr/bin/env python3

import math

import segno
from PIL import Image, ImageDraw, ImageFont

MM_TO_PX = 3.7795275591

def mm_to_px(mm):
    return round(mm * MM_TO_PX)

A4_WIDTH, A4_HEIGHT = mm_to_px(210), mm_to_px(297)
DIAMETER = mm_to_px(51)
MARGIN_LEFT = mm_to_px(26.5)
MARGIN_TOP = mm_to_px(17)
SPACING = mm_to_px(2)

TOTAL = 13
PREFIX = "LL"
FONT_HEIGHT = 30

qr_page = Image.new("RGBA", (A4_WIDTH, A4_HEIGHT), (255, 255, 255, 255))
qr_draw = ImageDraw.Draw(qr_page)
im_page = Image.new("RGBA", (A4_WIDTH, A4_HEIGHT), (255, 255, 255, 255))
im_draw = ImageDraw.Draw(im_page)
font = ImageFont.truetype("./fonts/Helvetica-Bold.ttf", FONT_HEIGHT)


for i in range(3):
    for j in range(5):
        n = i + j * 3 + 1
        if n > TOTAL:
            continue

        # Draw QR tag.
        tag = segno.make(f"https://ishara.uk/{PREFIX}{n:02}")
        tag = tag.to_pil(scale=5)

        pos = (
            i * (DIAMETER + SPACING) + MARGIN_LEFT + (DIAMETER - tag.width) // 2,
            j * (DIAMETER + SPACING) + MARGIN_TOP + 10,
        )

        qr_page.paste(tag, pos)


for i in range(3):
    for j in range(5):
        n = i + j * 3 + 1
        if n > TOTAL:
            continue

        box = (
            i * (DIAMETER + SPACING) + MARGIN_LEFT,            j * (DIAMETER + SPACING) + MARGIN_TOP,
            i * (DIAMETER + SPACING) + DIAMETER + MARGIN_LEFT, j * (DIAMETER + SPACING) + DIAMETER + MARGIN_TOP
        )

        # Draw image
        image = Image.open(f"images/{PREFIX}/{PREFIX}13.png")
        min_size = min(image.width, image.height)
        crop_box = (
            (image.width - min_size) // 2,
            (image.height - min_size) // 2,
            (image.width - min_size) // 2 + min_size,
            (image.height - min_size) // 2 + min_size,
        )
        image = image.crop(crop_box).resize((DIAMETER, DIAMETER))
        im_page.paste(image, box)

        # Draw circle
        box = (
            i * (DIAMETER + SPACING) + MARGIN_LEFT,            j * (DIAMETER + SPACING) + MARGIN_TOP,
            i * (DIAMETER + SPACING) + DIAMETER + MARGIN_LEFT, j * (DIAMETER + SPACING) + DIAMETER + MARGIN_TOP
        )

        qr_draw.ellipse(box, fill=None, outline=(0, 0, 0))
        im_draw.ellipse(box, fill=None, outline=(0, 0, 0))


        # Draw label
        label = f"{PREFIX}{n:02}"
        width = font.getlength(label)
        pos = (
            i * (DIAMETER + SPACING) + MARGIN_LEFT + (DIAMETER - width) // 2,
            j * (DIAMETER + SPACING) + MARGIN_TOP + (DIAMETER - 36),
        )

        im_draw.rectangle((pos[0] - 2, pos[1] - 1, pos[0] + width + 4, pos[1] + FONT_HEIGHT + 2), fill=(0, 0, 0), outline=None)

        qr_draw.text(pos, label, font=font, fill=(0, 0, 0))
        im_draw.text(pos, label, font=font, fill=(200, 200, 200))

qr_page.save(f"output/{PREFIX}_qr_codes.png")
im_page.save(f"output/{PREFIX}_images.png")
