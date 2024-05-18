import io
import os.path

import segno
import drawsvg as svg
from PIL import Image, ImageDraw

from .utils import (mm_to_px, stickers, A4_HEIGHT, A4_WIDTH, LINE_WIDTH, Color, create_page, icon, FONT_HEIGHT_LARGE,
                    font_from_language)


DIAMETER = mm_to_px(51)
PITCH = mm_to_px(53)
MARGIN_LEFT = mm_to_px(26.5)
MARGIN_TOP = mm_to_px(17)
ICON_SIZE_JOKER = mm_to_px(8)
ICON_SIZE_BANK = mm_to_px(28)
MAX_IMAGE_SIZE = 512


def draw_joker_icon() -> svg.Image:
    return svg.Image((PITCH - ICON_SIZE_JOKER) / 2, 12, ICON_SIZE_JOKER, ICON_SIZE_JOKER, icon("joker"), embed=True)


def draw_bank_icon() -> svg.Image:
    return svg.Image((PITCH - ICON_SIZE_BANK) / 2, 42, ICON_SIZE_BANK, ICON_SIZE_BANK, icon("joker_bank"), embed=True)


def draw_qr_code(prefix: str, language_code: str, n: int) -> svg.Image:
    # Draw QR tag.
    qr_code = segno.make(f"https://ishara.uk/{prefix}{n:02}{language_code if language_code != 'en' else ''}")
    qr_code = qr_code.to_pil(scale=5)
    data = io.BytesIO()
    qr_code.save(data, format="png")

    return svg.Image((PITCH - qr_code.width) / 2, 10, qr_code.width, qr_code.height, data=data.getvalue())


def image_file(language_code: str, prefix: str, n: int):
    png = f"./images/{prefix}/{language_code}/{prefix}{n:02}.png"
    if os.path.exists(png):
        return png

    jpeg = f"./images/{prefix}/{language_code}/{prefix}{n:02}.jpeg"
    if os.path.exists(jpeg):
        return jpeg

    if language_code != "en":
        return image_file("en", prefix=prefix, n=n)
    else:
        raise FileNotFoundError(f"No image found for {language_code}/{prefix}{n:02}")


def draw_image(language_code: str, prefix: str, n: int, crop_circle=False):
    image = image_file(language_code=language_code, prefix=prefix, n=n)

    image = Image.open(image)
    min_size = min(image.width, image.height)
    crop_box = (
        (image.width - min_size) // 2,
        (image.height - min_size) // 2,
        (image.width - min_size) // 2 + min_size,
        (image.height - min_size) // 2 + min_size,
    )
    image = image.crop(crop_box)
    if image.width > MAX_IMAGE_SIZE:
        image = image.resize((MAX_IMAGE_SIZE, MAX_IMAGE_SIZE), Image.LANCZOS)

    if crop_circle:
        scale = image.width / PITCH
        round_image = Image.new("RGBA", image.size)
        mask = Image.new('L', image.size, color=0)
        draw = ImageDraw.Draw(mask)
        offset = int(round((PITCH - DIAMETER) / 2) * scale)
        draw.ellipse((offset, offset, DIAMETER * scale + 7, DIAMETER * scale + 7), fill=255)
        round_image.paste(image, (0, 0), mask=mask)
        image = round_image

    data = io.BytesIO()
    image.save(data, format="png")
    return svg.Image(0, 0, PITCH, PITCH, data=data.getvalue(), mime_type="image/png", embed=True)


def draw_label(label: str, language_code: str, font_size: float, color, background_color=None) -> None:
    pos = (PITCH / 2, PITCH - mm_to_px(8))
    font_family = font_from_language(language_code)

    # Outline
    yield svg.Text(label, font_size, *pos, center=True, font_family=font_family,
                   style=f"stroke: {background_color}; stroke-linejoin: round: paint-order: stroke; stroke-width: 4px")

    # Actual text.
    yield svg.Text(label, font_size, *pos, fill=color, center=True, font_family=font_family)


def draw_images(t, prefix: str, language_code: str, with_border: bool, config: hash) -> int:
    for i, j, n in stickers(3, 5):
        sticker = svg.Group(transform=f"translate({MARGIN_TOP + i * PITCH}, {MARGIN_LEFT + j * PITCH})")
        try:
            sticker.append(draw_image(language_code=language_code, prefix=prefix, n=n, crop_circle=with_border))

            label = qr_label(prefix=prefix, n=n, language_code=language_code)
        except FileNotFoundError:
            label = t["joker"]

            if prefix == "LL" and n == 15:
                sticker.append(draw_bank_icon())

            sticker.append(draw_joker_icon())

        text_color = "rgb(200, 0, 0)" if n in config["hints"] else "black"
        sticker.extend(draw_label(label, language_code, FONT_HEIGHT_LARGE, color=text_color, background_color="white"))

        if with_border:
            sticker.append(svg.Circle(PITCH / 2, PITCH / 2, DIAMETER / 2, fill="none", stroke="black"))

        yield sticker


def qr_label(prefix, n, language_code):
    return f"{prefix}{n:02}{language_code if language_code != 'en' else ''}"


def draw_qr_codes(t, prefix: str, language_code: str, with_border: bool, num_tasks: int, config: hash) -> None:
    for i, j, n in stickers(3, 5):
        sticker = svg.Group(transform=f"translate({MARGIN_TOP + i * PITCH}, {MARGIN_LEFT + j * PITCH})")

        sticker.extend(single_qr_code(config=config, language_code=language_code, n=n, num_tasks=num_tasks,
                                      prefix=prefix, t=t, with_border=with_border))

        yield sticker


def single_qr_code(config, language_code, n, num_tasks, prefix, t, with_border):
    if n <= num_tasks:
        yield draw_qr_code(prefix, language_code, n)
        label = qr_label(prefix, n, language_code)
    else:
        label = t["joker"]

        if prefix == "LL" and n == 15:
            yield draw_bank_icon()

        yield draw_joker_icon()

    text_color = "rgb(200, 0, 0)" if n in config["hints"] else "black"
    yield from draw_label(label, language_code, font_size=FONT_HEIGHT_LARGE, color=text_color)
    if with_border:
        yield svg.Circle(PITCH / 2, PITCH / 2, DIAMETER / 2, fill="none", stroke="black")


def draw_discs(t: hash, prefix: str, language_code: str, config: hash) -> int:
    with create_page(f"{language_code}_{prefix}_images_b", format="pdf", language_code=language_code) as page:
        page.extend(draw_images(t, prefix, language_code, config=config, with_border=True))

    with create_page(f"{language_code}_{prefix}_images", format="pdf", language_code=language_code) as page:
        page.extend(draw_images(t, prefix, language_code, config=config, with_border=False))

    num_tasks = 12

    with create_page(f"{language_code}_{prefix}_qr_codes_b", format="pdf", language_code=language_code) as page:
        page.extend(draw_qr_codes(t, prefix, language_code, with_border=True, config=config, num_tasks=num_tasks))

    with create_page(f"{language_code}_{prefix}_qr_codes", format="pdf", language_code=language_code) as page:
        page.extend(draw_qr_codes(t, prefix, language_code, with_border=False, config=config, num_tasks=num_tasks))

    for i in range(num_tasks):
        label = qr_label(prefix, i, language_code)
        with create_page(f"qr_codes/{prefix}_{label}", format="png", width=DIAMETER, height=DIAMETER,
                         language_code=language_code) as page:
            page.extend(single_qr_code(config=config, language_code=language_code, n=i + 1, prefix=prefix, t=t,
                                       with_border=True, num_tasks=num_tasks))

    return num_tasks
