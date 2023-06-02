#!/usr/bin/env python3

from PIL import Image, ImageDraw

MM_TO_PX = 3.7795275591

def mm_to_px(mm):
    return round(mm * MM_TO_PX)

A4_WIDTH, A4_HEIGHT = mm_to_px(210), mm_to_px(297)
DIAMETER = mm_to_px(37)
MARGIN_LEFT = mm_to_px(8.5)
MARGIN_TOP = mm_to_px(13)
SPACING = mm_to_px(2)

image = Image.new("RGBA", (A4_WIDTH, A4_HEIGHT), (255, 255, 255, 255))
draw = ImageDraw.Draw(image)

icons = {
    "link": Image.open("./images/link.png"),
    "evaluate": Image.open("./images/evaluate.png"),
}

icons = {name: i.resize((i.width * 2, i.height * 2)) for name, i in icons.items()}


for i in range(5):
    for j in range(7):

        # Draw circle
        draw.ellipse((
                      i * (DIAMETER + SPACING) + MARGIN_LEFT,            j * (DIAMETER + SPACING) + MARGIN_TOP,
                      i * (DIAMETER + SPACING) + DIAMETER + MARGIN_LEFT, j * (DIAMETER + SPACING) + DIAMETER + MARGIN_TOP
                     ),
                     fill=None,
                     outline=(0, 0, 0))

        # Draw icon
        if j in {0, 1, 2, 3}:
           icon = icons["link"]
        else:
           icon = icons["evaluate"]

        x, y = i * (DIAMETER + SPACING) + MARGIN_LEFT + (DIAMETER - icon.width) // 2, j * (DIAMETER + SPACING) + MARGIN_TOP + (DIAMETER - icon.height) // 2
        image.paste(icon, (x, y))


image.save(f"./output/37.png")
