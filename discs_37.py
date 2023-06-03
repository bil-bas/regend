#!/usr/bin/env python3

from PIL import Image, ImageDraw

from regend.utils import mm_to_px, stickers, A4_WIDTH, A4_HEIGHT


DIAMETER = mm_to_px(37)
PITCH = mm_to_px(39)
MARGIN_LEFT = mm_to_px(8.5)
MARGIN_TOP = mm_to_px(13)

image = Image.new("RGBA", (A4_WIDTH, A4_HEIGHT), (255, 255, 255, 255))
draw = ImageDraw.Draw(image)

icons = {
    "link": Image.open("./images/link.png"),
    "evaluate": Image.open("./images/evaluate.png"),
}

icons = {name: i.resize((i.width * 2, i.height * 2)) for name, i in icons.items()}


for i, j, _ in stickers(5, 7):
    # Draw circle
    draw.ellipse((
                  i * PITCH + MARGIN_LEFT,            j * PITCH + MARGIN_TOP,
                  i * PITCH + DIAMETER + MARGIN_LEFT, j * PITCH + DIAMETER + MARGIN_TOP
                 ),
                 fill=None,
                 outline=(0, 0, 0))

    # Draw icon
    if j in {0, 1, 2, 3}:
        icon = icons["link"]
    else:
        icon = icons["evaluate"]

    x = i * PITCH + MARGIN_LEFT + (DIAMETER - icon.width) // 2
    y = j * PITCH + MARGIN_TOP + (DIAMETER - icon.height) // 2
    image.paste(icon, (x, y))


image.save("./output/37.png")
