import re
import textwrap

import drawsvg as svg

from .utils import (mm_to_px, stickers, FONT_HEIGHT_SMALL, FONT_HEIGHT_LARGE, create_page,
                    icon, font_from_language)

DIAMETER = mm_to_px(37)
PITCH = mm_to_px(39)
MARGIN_LEFT = mm_to_px(8.5 - 1)  # Always prints with a left margin.
MARGIN_TOP = mm_to_px(13)
MAX_LINE_LENGTH = 15
ICON_WIDTH = mm_to_px(20)


def name(index):
    if index in {0, 1, 2, 3}:
        return "link"
    else:
        return "evaluate"


def draw_icon_discs(with_border: bool) -> None:
    for i, j, _ in stickers(5, 7):
        sticker = svg.Group(transform=f"translate({MARGIN_LEFT + i * PITCH}, {MARGIN_TOP + j * PITCH})")
        if with_border:
            sticker.append(border())

        offset = (PITCH - ICON_WIDTH) / 2
        sticker.append(svg.Image(offset, offset, ICON_WIDTH, ICON_WIDTH, icon(name(j)), embed=True))

        yield sticker


def border():
    return svg.Circle(PITCH / 2, PITCH / 2, DIAMETER / 2, fill="none", stroke="black")


def draw_text(text: str, language_code: str) -> None:
    y_offset = mm_to_px(13)
    font_family = font_from_language(language_code)
    try:
        title, body = re.split(r" *: *", text)

        yield svg.Text(title, FONT_HEIGHT_LARGE, PITCH / 2, y_offset, center=True, font_family=font_family,
                       font_weight="bold")
        y_offset += FONT_HEIGHT_LARGE + 8
    except ValueError:
        body = text

    wrapped = textwrap.fill(body, MAX_LINE_LENGTH)
    yield svg.Text(wrapped, FONT_HEIGHT_SMALL, PITCH / 2, y_offset, center=True, font_family=font_family,
                   font_weight="bold")


def draw_text_discs(t: hash, language_code: str, with_border: bool) -> None:
    for i, j, _ in stickers(5, 7):
        sticker = svg.Group(transform=f"translate({MARGIN_LEFT + i * PITCH}, {MARGIN_TOP + j * PITCH})")
        if with_border:
            sticker.append(border())
        sticker.extend(draw_text(t[name(j)], language_code))
        yield sticker


def draw_discs(t: hash, language_code: str) -> None:
    with create_page("actions_icon_b", "pdf", language_code=language_code) as page:
        page.extend(draw_icon_discs(with_border=True))

    with create_page("actions_icon", "pdf", language_code=language_code) as page:
        page.extend(draw_icon_discs(with_border=False))

    with create_page(f"{language_code}_actions_text_b", "pdf", language_code=language_code) as page:
        page.extend(draw_text_discs(t=t, language_code=language_code, with_border=True))

    with create_page(f"{language_code}_actions_text", "pdf", language_code=language_code) as page:
        page.extend(draw_text_discs(t=t, language_code=language_code, with_border=False))
