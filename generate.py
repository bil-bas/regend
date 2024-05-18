#!/usr/bin/env python3.9

import argparse
import zipfile
import datetime
import os
import yaml

import polib
from PIL import ImageFont

from regend import discs_task, discs_action, spinner_base, board_tasks, board_actions
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

    language_code = language[0:2]

    prefix = args.prefix.upper()

    for folder in ("output/releases", "output/qr_codes"):
        os.makedirs(folder, exist_ok=True)

    with open(f"images/{prefix}/meta.yaml") as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)

    spinner_base.draw_spinner()

    discs_task.draw_discs(t=t, prefix=prefix, language_code=language_code, config=config)
    board_tasks.draw_circles(prefix=prefix, num_tasks=config["num_tasks"])

    discs_action.draw_discs(t=t, language_code=language_code)
    board_actions.draw_circles()

    date_str = datetime.date.today()
    file_str = f"output/releases/regen-d_{prefix}_{language_code}_{date_str}.zip"

    with zipfile.ZipFile(file_str, mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipped:
        zipped.write("output/actions_icon_b.pdf", "action_disks_front.png")
        zipped.write(f"output/{language_code}_actions_text_b.pdf", "action_disks_back.pdf")

        zipped.write(f"output/{language_code}_{prefix}_images_b.pdf", "task_disks_front.pdf")
        zipped.write(f"output/{language_code}_{prefix}_qr_codes_b.pdf", "task_disks_back.pdf")

        zipped.write("output/spinner.svg", "spinner.svg")
        zipped.write("output/spinner.pdf", "spinner.pdf")

        zipped.write("output/board_actions.pdf", "extras/actions_board.pdf")
        zipped.write(f"output/{prefix}_board_tasks.pdf", "extras/tasks_board.pdf")


if __name__ == "__main__":
    parse(create_parser())


