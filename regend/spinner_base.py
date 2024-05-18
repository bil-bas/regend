import drawsvg as svg

from .utils import mm_to_px, A4_WIDTH, A4_HEIGHT, Color, create_page


RADIUS = mm_to_px(70)
HOLE_RADIUS = mm_to_px(2)
CORNER_RADIUS = mm_to_px(10)
WIDTH, HEIGHT = mm_to_px(200), mm_to_px(200)
CENTER_X, CENTER_Y = WIDTH / 2, HEIGHT / 2
ICONS = ["joker", "qr", "qr", "evaluate", "qr", "link", "qr", "evaluate", "qr", "qr", "link", "qr"]
LINE_WIDTH, LINE_LENGTH = 10, 100
ICON_WIDTH = 50


def draw_spinner():
    for format_ in ["svg", "pdf"]:
        with create_page("spinner", format=format_) as page:
            page.extend(spinner())


def spinner():
    yield svg.Rectangle(0, 0, WIDTH, HEIGHT, rx=CORNER_RADIUS, ry=CORNER_RADIUS, fill="none",
                        stroke=Color.CUT)
    yield svg.Circle(CENTER_X, CENTER_Y, r=HOLE_RADIUS, fill="none", stroke=Color.CUT)

    content = svg.Group(transform=f"translate({CENTER_X}, {CENTER_Y})")

    for i, icon in enumerate(ICONS):
        angle = -90 + 360 * i / len(ICONS)
        content.append(svg.Image(-ICON_WIDTH / 2, -ICON_WIDTH / 2, ICON_WIDTH, ICON_WIDTH,
                                 f"./images/icons/{icon}.png", embed=True,
                                 transform=f"rotate({angle}), translate({RADIUS}, 0), rotate(90)"))

        angle = 360 * (i + 0.5) / len(ICONS)
        content.append(svg.Rectangle(0, -LINE_WIDTH / 2, LINE_LENGTH, LINE_WIDTH, fill=Color.ENGRAVE,
                                     transform=f"rotate({angle}), translate({RADIUS - LINE_LENGTH / 2}, 0)"))

    yield content


if __name__ == "__main__":
    draw_spinner()
