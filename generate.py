#!/usr/bin/env python3.9

import argparse

import polib
from PIL import ImageFont

from regend import discs_qr, discs_action, spinner_icons
from regend.utils import FONT_HEIGHT_ACTION, FONT_HEIGHT_QR


def create_parser():
    parser = argparse.ArgumentParser(description="Layout generator for Ishara Press Regen-D game")

    parser.add_argument("prefix", type=str)
    parser.add_argument("--language", type=str, default="en")

    return parser


def parse(parser):
    args = parser.parse_args()

    language = args.language
    try:
        translations = polib.pofile(f"translations/{language}.po")
        t = {entry.msgid: entry.msgstr for entry in translations}
    except (FileNotFoundError, OSError):
        t = None
        parser.error(f"Language not supported: {language}")

    if language == "or":
        font_file = "NotoSansOriya-Bold"
    else:
        font_file = "Arimo-Bold"

    language_code = language[0:2]

    font_qr = ImageFont.truetype(f"./fonts/{font_file}.ttf", FONT_HEIGHT_QR)
    font_action = ImageFont.truetype(f"./fonts/{font_file}.ttf", FONT_HEIGHT_ACTION)

    prefix = args.prefix.upper()

    spinner_icons.draw_spinner()

    discs_qr.draw_discs(t=t, prefix=prefix, font=font_qr, language_code=language_code)

    discs_action.draw_discs(title_font=font_qr, body_font=font_action, t=t, language_code=language_code)


if __name__ == "__main__":
    parse(create_parser())


