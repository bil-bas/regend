#!/usr/bin/env python3

import segno
from PIL import Image, ImageDraw, ImageFont

DIAMETER = 300

image = Image.new("RGBA", (210 * 5, 297 * 5), (255, 255, 255, 255))
draw = ImageDraw.Draw(image)
font = ImageFont.truetype("./Helvetica-Bold.ttf", 50)

for i in range(3):
    for j in range(5):
       n = i + j * 3 + 1
       tag = segno.make(f"https://ishara.uk/WM{n:02}")
       tag = tag.to_pil(scale=6)

       x, y = i * DIAMETER + 50, j * DIAMETER + 30
       image.paste(tag, (x, y))


for i in range(3):
    for j in range(5):
        n = i + j * 3 + 1
        draw.ellipse((i * DIAMETER, j * DIAMETER,
                     (i + 1) * DIAMETER, (j + 1) * DIAMETER),
                    fill=None,
                    outline=(0, 0, 0))
        label = f"WM{n:02}"
        width, _ = font.getsize(label)
        draw.text(((i + 0.5) * DIAMETER - width // 2, (j + 1) * DIAMETER - 80),
                  label,
                  font=font,
                  fill=(0, 0, 0))

image.save("tags.png")
