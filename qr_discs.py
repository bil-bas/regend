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

image = Image.new("RGBA", (A4_WIDTH, A4_HEIGHT), (255, 255, 255, 255))
draw = ImageDraw.Draw(image)
font = ImageFont.truetype("./Helvetica-Bold.ttf", FONT_HEIGHT)


for i in range(3):
    for j in range(5):
        n = i + j * 3 + 1
        if n > TOTAL:
            continue

        # Draw QR tag.
        tag = segno.make(f"https://ishara.uk/{PREFIX}{n:02}")
        tag = tag.to_pil(scale=5)

        x, y = i * (DIAMETER + SPACING) + MARGIN_LEFT + (DIAMETER - tag.width) // 2, j * (DIAMETER + SPACING) + MARGIN_TOP + 10
        image.paste(tag, (x, y))


for i in range(3):
    for j in range(5):
        n = i + j * 3 + 1
        if n > TOTAL:
            continue

        # Draw circle
        draw.ellipse((
                      i * (DIAMETER + SPACING) + MARGIN_LEFT,            j * (DIAMETER + SPACING) + MARGIN_TOP,
                      i * (DIAMETER + SPACING) + DIAMETER + MARGIN_LEFT, j * (DIAMETER + SPACING) + DIAMETER + MARGIN_TOP
                     ),
                     fill=None,
                     outline=(0, 0, 0))

        # Draw label
        label = f"{PREFIX}{n:02}"
        width = font.getlength(label)
        draw.text((
                      i * (DIAMETER + SPACING) + MARGIN_LEFT + (DIAMETER - width) // 2,
                      j * (DIAMETER + SPACING) + MARGIN_TOP + (DIAMETER - 36),
                  ),
                  label,
                  font=font,
                  fill=(0, 0, 0))

image.save(f"{PREFIX}_tags.png")
