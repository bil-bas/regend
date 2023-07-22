import segno
from PIL import Image, ImageDraw

from .utils import mm_to_px, stickers, draw_circle, A4_HEIGHT, A4_WIDTH, FONT_HEIGHT_QR


DIAMETER = mm_to_px(51)
PITCH = mm_to_px(53)
MARGIN_LEFT = mm_to_px(26.5)
MARGIN_TOP = mm_to_px(17)


def draw_qr_code(prefix: str, language_code: str, page, i: int, j: int, n: int) -> None:
    # Draw QR tag.
    qr_code = segno.make(f"https://ishara.uk/{prefix}{n:02}{language_code if language_code != 'en' else ''}")
    qr_code = qr_code.to_pil(scale=5)
    pos = (
        i * PITCH + MARGIN_LEFT + (DIAMETER - qr_code.width) // 2,
        j * PITCH + MARGIN_TOP + 10,
    )
    page.paste(qr_code, pos)


def draw_image(prefix: str, page, i: int, j: int, n: int):
    box = (
        i * PITCH + MARGIN_LEFT, j * PITCH + MARGIN_TOP,
        i * PITCH + PITCH + MARGIN_LEFT, j * PITCH + PITCH + MARGIN_TOP
    )

    image = Image.open(f"./images/{prefix}/{prefix}{n:02}.jpeg")
    min_size = min(image.width, image.height)
    crop_box = (
        (image.width - min_size) // 2,
        (image.height - min_size) // 2,
        (image.width - min_size) // 2 + min_size,
        (image.height - min_size) // 2 + min_size,
    )
    image = image.crop(crop_box).resize((PITCH, PITCH))
    page.paste(image, box)


def draw_label(label, language_code, draw, i: int, j: int, n: int, font, color, background_color=None) -> None:
    width = font.getlength(label)
    pos = (
        i * PITCH + MARGIN_LEFT + (DIAMETER - width) // 2,
        j * PITCH + MARGIN_TOP + (DIAMETER - (44 if language_code == "or" else 36)),
    )
    if background_color is not None:
        draw.rectangle((pos[0] - 2, pos[1] - 1, pos[0] + width + 4, pos[1] + FONT_HEIGHT_QR + 2),
                       fill=background_color, outline=None)
    draw.text(pos, label, font=font, fill=color)


def draw_images(t, prefix: str, language_code: str, font, with_border: bool):
    im_page = Image.new("RGBA", (A4_WIDTH, A4_HEIGHT), (255, 255, 255, 255))
    im_draw = ImageDraw.Draw(im_page)

    for i, j, n in stickers(3, 5):
        try:
            draw_image(prefix, im_page, i, j, n)
            label = qr_label(prefix, n, language_code)
        except FileNotFoundError:
            label = "?"

        draw_label(label, language_code, im_draw, i, j, n, font, color=(0, 0, 0), background_color=(255, 255, 255))
        if with_border:
            draw_circle(im_draw, i, j, diameter=DIAMETER, pitch=PITCH,
                        margin_top=MARGIN_TOP, margin_left=MARGIN_LEFT)

    im_page.save(f"./output/{language_code}_{prefix}_images{'_b' if with_border else ''}.png")


def qr_label(prefix, n, language_code):
    return f"{prefix}{n:02}{language_code if language_code != 'en' else ''}"


def draw_qr_codes(t, prefix: str, language_code: str, font, with_border: bool) -> None:
    qr_page = Image.new("RGBA", (A4_WIDTH, A4_HEIGHT), (255, 255, 255, 255))
    qr_draw = ImageDraw.Draw(qr_page)

    for i, j, n in stickers(3, 5, 12):
        draw_qr_code(prefix, language_code, qr_page, i, j, n)

    for i, j, n in stickers(3, 5):
        if n <= 12:
            label = qr_label(prefix, n, language_code)
        else:
            label = t["joker"]
        draw_label(label, language_code, qr_draw, i, j, n, font, color=(0, 0, 0))

        if with_border:
            draw_circle(qr_draw, i, j, diameter=DIAMETER, pitch=PITCH,
                        margin_top=MARGIN_TOP, margin_left=MARGIN_LEFT)

    qr_page.save(f"./output/{language_code}_{prefix}_qr_codes{'_b' if with_border else ''}.png")


def draw_discs(t, prefix, language_code, font):
    draw_images(t, prefix, language_code, font, with_border=True)
    draw_images(t, prefix, language_code, font, with_border=False)

    draw_qr_codes(t, prefix, language_code, font, with_border=True)
    draw_qr_codes(t, prefix, language_code, font, with_border=False)


