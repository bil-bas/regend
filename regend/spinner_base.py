import drawsvg as svg

from .utils import mm_to_px, A4_WIDTH, A4_HEIGHT, Color, create_page


RADIUS = mm_to_px(70)
HOLE_RADIUS = mm_to_px(1.5)
CORNER_RADIUS = mm_to_px(20)
WIDTH, HEIGHT = mm_to_px(190), mm_to_px(190)
ICONS = ["joker", "qr", "qr", "evaluate", "qr", "link", "qr", "evaluate", "qr", "qr", "link", "qr"]
LINE_WIDTH, LINE_LENGTH = 3, 160
ICON_WIDTH = 65


def draw_spinner():
    with create_page("spinner", "svg,pdf") as page:
        page.extend(spinner())


def spinner():
    content = svg.Group(transform=f"translate({35 + WIDTH / 2}, {35 + HEIGHT / 2})")

    content.append(svg.Rectangle(-WIDTH / 2, -HEIGHT / 2, WIDTH, HEIGHT, rx=CORNER_RADIUS, ry=CORNER_RADIUS,
                                 fill="none", stroke=Color.CUT))
    content.append(svg.Circle(0, 0, r=HOLE_RADIUS, fill="none", stroke=Color.CUT))

    for i, icon in enumerate(ICONS):
        angle = -90 - 360 * i / len(ICONS)
        content.append(svg.Image(-ICON_WIDTH / 2, -ICON_WIDTH / 2, ICON_WIDTH, ICON_WIDTH,
                                 f"./images/icons/{icon}.png", embed=True,
                                 transform=f"rotate({angle}) translate({RADIUS}, 0), rotate(90)"))

        angle = 360 * (i + 0.5) / len(ICONS)
        content.append(svg.Rectangle(0, -LINE_WIDTH / 2, LINE_LENGTH, LINE_WIDTH, fill=Color.ENGRAVE,
                                     transform=f"rotate({angle}) translate({RADIUS - LINE_LENGTH / 2}, 0)"))

    yield content


if __name__ == "__main__":
    draw_spinner()
