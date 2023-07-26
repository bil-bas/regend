import re

from PIL import Image, ImageDraw

from .utils import (mm_to_px, stickers, draw_circle, get_wrapped_text, A4_WIDTH, A4_HEIGHT,
                    FONT_HEIGHT_SMALL, FONT_HEIGHT_LARGE)

DIAMETER = mm_to_px(37)
PITCH = mm_to_px(39)
MARGIN_LEFT = mm_to_px(8.5)
MARGIN_TOP = mm_to_px(13)
MAX_LINE_LENGTH = mm_to_px(28)


def name(index):
    if index in {0, 1, 2, 3}:
        return "link"
    else:
        return "evaluate"


def draw_icon(page, icons: dict, i: int, j: int) -> None:
    icon = icons[name(j)]

    x = i * PITCH + MARGIN_LEFT + round((DIAMETER - icon.width) / 2)
    y = j * PITCH + MARGIN_TOP + round((DIAMETER - icon.height) / 2)
    page.paste(icon, (x, y))


def draw_icon_discs(with_border: bool) -> None:
    icons = {
        "link": Image.open("./images/icons/link.png"),
        "evaluate": Image.open("./images/icons/evaluate.png"),
    }

    page = Image.new("RGBA", (A4_WIDTH, A4_HEIGHT), (255, 255, 255, 255))
    draw = ImageDraw.Draw(page)

    for i, j, _ in stickers(5, 7):
        if with_border:
            draw_circle(draw, i, j, diameter=DIAMETER, pitch=PITCH, margin_top=MARGIN_TOP, margin_left=MARGIN_LEFT)

        draw_icon(page, icons, i, j)

    page.save(f"./output/actions_icon{'_b' if with_border else ''}.png")


def draw_text_line(draw, i, j, y_offset, text, font):
    width = font.getlength(text)
    pos = (
        i * PITCH + MARGIN_LEFT + (DIAMETER - width) // 2,
        j * PITCH + MARGIN_TOP + DIAMETER + y_offset,
    )
    draw.text(pos, text, font=font, fill=(0, 0, 0))


def draw_text(draw, i: int, j: int, text: str, title_font, body_font) -> None:
    y_offset = -110
    try:
        title, body = re.split(r" *: *", text)

        draw_text_line(draw, i, j, y_offset, title, title_font)
        y_offset += FONT_HEIGHT_LARGE + 8
    except ValueError:
        body = text

    for line in get_wrapped_text(text=body, font=body_font, line_length=MAX_LINE_LENGTH):
        draw_text_line(draw, i, j, y_offset, line, body_font)
        y_offset += FONT_HEIGHT_SMALL + 4


def draw_text_discs(t: hash, language_code: str, title_font, body_font, with_border: bool) -> None:
    page = Image.new("RGBA", (A4_WIDTH, A4_HEIGHT), (255, 255, 255, 255))
    draw = ImageDraw.Draw(page)

    for i, j, _ in stickers(5, 7):
        if with_border:
            draw_circle(draw, i, j, diameter=DIAMETER, pitch=PITCH, margin_top=MARGIN_TOP, margin_left=MARGIN_LEFT)
        draw_text(draw, i, j, t[name(j)], title_font, body_font)

    page.save(f"./output/{language_code}_actions_text{'_b' if with_border else ''}.png")


def draw_discs(t: hash, language_code: str, title_font, body_font) -> None:
    draw_icon_discs(with_border=True)
    draw_icon_discs(with_border=False)

    draw_text_discs(t=t, title_font=title_font, body_font=body_font, language_code=language_code, with_border=True)
    draw_text_discs(t=t, title_font=title_font, body_font=body_font, language_code=language_code, with_border=False)
