import re

from PIL import Image, ImageDraw
from contextlib import contextmanager

from .utils import (mm_to_px, stickers, draw_circle, get_wrapped_text, A4_WIDTH, A4_HEIGHT,
                    FONT_HEIGHT_SMALL, FONT_HEIGHT_LARGE)

DIAMETER = mm_to_px(37)
PITCH = mm_to_px(39)
MARGIN_LEFT = mm_to_px(8.5 - 1)  # Always prints with a left margin.
MARGIN_TOP = mm_to_px(13)
MAX_LINE_LENGTH = mm_to_px(28)


def name(index):
    if index in {0, 1, 2, 3}:
        return "link"
    else:
        return "evaluate"


def draw_icon(page, icons: dict, j: int) -> None:
    icon = icons[name(j)]

    x = round((DIAMETER - icon.width) / 2)
    y = round((DIAMETER - icon.height) / 2)
    page.paste(icon, (x, y))


def draw_icon_discs(with_border: bool) -> None:
    icons = {
        "link": Image.open("./images/icons/link.png"),
        "evaluate": Image.open("./images/icons/evaluate.png"),
    }

    page = Image.new("RGBA", (A4_WIDTH, A4_HEIGHT), (255, 255, 255, 255))

    for i, j, _ in stickers(5, 7):
        with draw_sticker(page, i=i, j=j, with_border=with_border) as sticker:
            draw_icon(sticker, icons, j=j)

    page.save(f"./output/actions_icon{'_b' if with_border else ''}.png")


@contextmanager
def draw_sticker(page, i: int, j: int, with_border: bool):
    sticker = Image.new("RGBA", (PITCH, PITCH), (255, 255, 255, 255))
    sticker_draw = ImageDraw.Draw(sticker)

    if with_border:
        draw_circle(sticker_draw, diameter=DIAMETER, offset=int(round((PITCH - DIAMETER) / 2)))

    yield sticker

    page.paste(sticker, (MARGIN_TOP + i * PITCH, MARGIN_LEFT + j * PITCH))


def draw_text_line(draw, y_offset, text, font):
    width = font.getlength(text)
    pos = (
        (DIAMETER - width) // 2,
        y_offset,
    )
    draw.text(pos, text, font=font, fill=(0, 0, 0))


def draw_text(draw, text: str, title_font, body_font) -> None:
    y_offset = -110
    try:
        title, body = re.split(r" *: *", text)

        draw_text_line(draw, y_offset, title, title_font)
        y_offset += FONT_HEIGHT_LARGE + 8
    except ValueError:
        body = text

    for line in get_wrapped_text(text=body, font=body_font, line_length=MAX_LINE_LENGTH):
        draw_text_line(draw, y_offset, line, body_font)
        y_offset += FONT_HEIGHT_SMALL + 4


def draw_text_discs(t: hash, language_code: str, title_font, body_font, with_border: bool) -> None:
    page = Image.new("RGBA", (A4_WIDTH, A4_HEIGHT), (255, 255, 255, 255))

    for i, j, _ in stickers(5, 7):
        with draw_sticker(page, i=i, j=j, with_border=with_border) as sticker:
            sticker_draw = ImageDraw.Draw(sticker)
            draw_text(sticker_draw, t[name(j)], title_font, body_font)

    page.save(f"./output/{language_code}_actions_text{'_b' if with_border else ''}.png")


def draw_discs(t: hash, language_code: str, title_font, body_font) -> None:
    draw_icon_discs(with_border=True)
    draw_icon_discs(with_border=False)

    draw_text_discs(t=t, title_font=title_font, body_font=body_font, language_code=language_code, with_border=True)
    draw_text_discs(t=t, title_font=title_font, body_font=body_font, language_code=language_code, with_border=False)
