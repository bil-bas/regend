#!/usr/bin/env python3.9

import argparse
import zipfile
import datetime
import yaml

import polib
from PIL import ImageFont

from regend import discs_task, discs_action, spinner_icons, board_tasks, board_actions
from regend.utils import FONT_HEIGHT_SMALL, FONT_HEIGHT_LARGE, svg_to_png


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

    font_large = ImageFont.truetype(f"./fonts/{font_file}.ttf", FONT_HEIGHT_LARGE)
    font_small = ImageFont.truetype(f"./fonts/{font_file}.ttf", FONT_HEIGHT_SMALL)

    prefix = args.prefix.upper()

    with open(f"images/{prefix}/meta.yaml") as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)

    spinner_icons.draw_spinner()

    num_tasks = discs_task.draw_discs(t=t, prefix=prefix, font=font_large, language_code=language_code, config=config)
    board_tasks.draw_circles(prefix=prefix, num_tasks=num_tasks)

    discs_action.draw_discs(title_font=font_large, body_font=font_small, t=t, language_code=language_code)
    board_actions.draw_circles()

    date_str = datetime.date.today()
    file_str = f"output/regen-d_{prefix}_{language_code}_{date_str}.zip"
    svg_to_png("spinner.svg")
    with zipfile.ZipFile(file_str, mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipped:
        zipped.write("output/actions_icon_b.png", "action_disks_front.png")
        zipped.write(f"output/{language_code}_actions_text_b.png", "action_disks_back.png")

        zipped.write(f"output/{language_code}_{prefix}_images_b.png", "task_disks_front.png")
        zipped.write(f"output/{language_code}_{prefix}_qr_codes_b.png", "task_disks_back.png")

        zipped.write("output/spinner.png", "spinner.png")
        zipped.write("output/board_actions.png", "actions_board_optional.png")
        zipped.write(f"output/{prefix}_board_tasks.png", "tasks_board_optional.png")


if __name__ == "__main__":
    parse(create_parser())


