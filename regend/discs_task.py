import segno
from PIL import Image, ImageDraw

from .utils import mm_to_px, stickers, draw_circle, A4_HEIGHT, A4_WIDTH, LINE_WIDTH


DIAMETER = mm_to_px(51)
PITCH = mm_to_px(53)
MARGIN_LEFT = mm_to_px(26.5)
MARGIN_TOP = mm_to_px(17)


def draw_joker_icon(page, i: int, j: int) -> None:
    icon = Image.open("./images/icons/joker_mini.png")

    x = i * PITCH + MARGIN_LEFT + round((DIAMETER - icon.width) / 2)
    y = j * PITCH + MARGIN_TOP + 12
    page.paste(icon, (x, y))


def draw_qr_code(prefix: str, language_code: str, page, i: int, j: int, n: int) -> None:
    # Draw QR tag.
    qr_code = segno.make(f"https://ishara.uk/{prefix}{n:02}{language_code if language_code != 'en' else ''}")
    qr_code = qr_code.to_pil(scale=5)
    pos = (
        i * PITCH + MARGIN_LEFT + (DIAMETER - qr_code.width) // 2,
        j * PITCH + MARGIN_TOP + 10,
    )
    page.paste(qr_code, pos)


def image_file(language_code: str, prefix: str, n: int):
    try:
        image = Image.open(f"./images/{prefix}/{language_code}/{prefix}{n:02}.png")
    except FileNotFoundError:
        try:
            image = Image.open(f"./images/{prefix}/{language_code}/{prefix}{n:02}.jpeg")
        except FileNotFoundError:
            # Default to english version of the file.
            if language_code != "en":
                image = image_file("en", prefix=prefix, n=n)
            else:
                raise FileNotFoundError("No image found for {language_code}/{prefix}{n:02}")
    return image


def draw_image(language_code: str, prefix: str, page, i: int, j: int, n: int):
    box = (
        i * PITCH + MARGIN_LEFT - 3, j * PITCH + MARGIN_TOP - 3,
        i * PITCH + PITCH + MARGIN_LEFT - 3, j * PITCH + PITCH + MARGIN_TOP - 3
    )
    image = image_file(language_code=language_code, prefix=prefix, n=n)

    min_size = min(image.width, image.height)
    crop_box = (
        (image.width - min_size) // 2,
        (image.height - min_size) // 2,
        (image.width - min_size) // 2 + min_size,
        (image.height - min_size) // 2 + min_size,
    )
    image = image.crop(crop_box).resize((PITCH, PITCH))
    page.paste(image, box)


def draw_label(label: str, language_code: str, draw, i: int, j: int, font, color, background_color=None) -> None:
    width = font.getlength(label)
    pos = (
        i * PITCH + MARGIN_LEFT + (DIAMETER - width) // 2,
        j * PITCH + MARGIN_TOP + (DIAMETER - (44 if language_code == "or" else 36)),
    )

    if background_color is not None:
        for x, y in [(2, 0), (0, 2), (-2, 0), (0, -2)]:
            draw.text((pos[0] + x, pos[1] + y), label, font=font, fill=background_color)

    draw.text(pos, label, font=font, fill=color)


def draw_images(t, prefix: str, language_code: str, font, with_border: bool, config: hash) -> int:
    im_page = Image.new("RGBA", (A4_WIDTH, A4_HEIGHT), (255, 255, 255, 255))
    im_draw = ImageDraw.Draw(im_page)

    num_tasks = None
    for i, j, n in stickers(3, 5):
        try:
            draw_image(language_code=language_code, prefix=prefix, page=im_page, i=i, j=j, n=n)
            label = qr_label(prefix=prefix, n=n, language_code=language_code)
        except FileNotFoundError:
            label = t["joker"]
            draw_joker_icon(im_page, i, j)
            if num_tasks is None:
                num_tasks = n - 1

        text_color = (200, 0, 0) if n in config["hints"] else (0, 0, 0)
        draw_label(label, language_code, im_draw, i, j, font, color=text_color, background_color=(255, 255, 255))
        if with_border:
            draw_circle(im_draw, i, j, diameter=DIAMETER, pitch=PITCH,
                        margin_top=MARGIN_TOP, margin_left=MARGIN_LEFT)

    im_page.save(f"./output/{language_code}_{prefix}_images{'_b' if with_border else ''}.png")

    return num_tasks


def qr_label(prefix, n, language_code):
    return f"{prefix}{n:02}{language_code if language_code != 'en' else ''}"


def draw_qr_codes(t, prefix: str, language_code: str, font, with_border: bool, num_tasks: int, config: hash) -> None:
    qr_page = Image.new("RGBA", (A4_WIDTH, A4_HEIGHT), (255, 255, 255, 255))
    qr_draw = ImageDraw.Draw(qr_page)

    for i, j, n in stickers(3, 5, num_tasks):
        draw_qr_code(prefix, language_code, qr_page, i, j, n)

    for i, j, n in stickers(3, 5):
        if n <= num_tasks:
            label = qr_label(prefix, n, language_code)
        else:
            draw_joker_icon(qr_page, i, j)
            label = t["joker"]

        text_color = (200, 0, 0) if n in config["hints"] else (0, 0, 0)
        draw_label(label, language_code, qr_draw, i, j, font, color=text_color)

        if with_border:
            draw_circle(qr_draw, i, j, diameter=DIAMETER, pitch=PITCH,
                        margin_top=MARGIN_TOP, margin_left=MARGIN_LEFT)

    qr_page.save(f"./output/{language_code}_{prefix}_qr_codes{'_b' if with_border else ''}.png")


def draw_single_qr_code(t, prefix: str, language_code: str, font, index: int, config: hash) -> None:
    qr_image = Image.new("RGBA", (DIAMETER, DIAMETER), (255, 255, 255, 255))
    qr_draw = ImageDraw.Draw(qr_image)

    # QR code
    qr_code = segno.make(f"https://ishara.uk/{prefix}{index:02}{language_code if language_code != 'en' else ''}")
    qr_code = qr_code.to_pil(scale=5)
    qr_image.paste(qr_code, ((DIAMETER - qr_code.width) // 2, (DIAMETER - qr_code.height) // 2 - 5))

    # Label
    label = qr_label(prefix, index, language_code)
    width = font.getlength(label)
    v_offset = (DIAMETER - (44 if language_code == "or" else 36))
    qr_draw.text(((DIAMETER - width) // 2, v_offset), label, font=font, fill=(0, 0, 0))

    # circle
    qr_draw.ellipse((0, 0, DIAMETER - 1, DIAMETER - 1), fill=None, outline=(0, 0, 0), width=LINE_WIDTH)

    qr_image.save(f"./output/qr_codes/{prefix}_{label}.png")


def draw_discs(t: hash, prefix: str, language_code: str, font, config: hash) -> int:
    draw_images(t, prefix, language_code, font, config=config, with_border=True)
    num_tasks = draw_images(t, prefix, language_code, font, config=config, with_border=False)

    draw_qr_codes(t, prefix, language_code, font, with_border=True, config=config, num_tasks=num_tasks)
    draw_qr_codes(t, prefix, language_code, font, with_border=False, config=config, num_tasks=num_tasks)

    for i in range(num_tasks):
        draw_single_qr_code(t, prefix, language_code, font, index=i + 1, config=config)

    return num_tasks
