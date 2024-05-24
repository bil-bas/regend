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
    with create_page("spinner_base", "svg,pdf", width=A4_WIDTH, height=A4_WIDTH) as page:
        content = svg.Group(transform=f"translate({35 + WIDTH / 2}, {35 + HEIGHT / 2})")
        content.extend(spinner())
        page.append(content)


def spinner():
    yield svg.Rectangle(-WIDTH / 2, -HEIGHT / 2, WIDTH, HEIGHT, rx=CORNER_RADIUS, ry=CORNER_RADIUS,
                        fill="none", stroke=Color.CUT)
    yield svg.Circle(0, 0, r=HOLE_RADIUS, fill="none", stroke=Color.CUT)

    for i, icon in enumerate(ICONS):
        angle = -90 - 360 * i / len(ICONS)
        yield svg.Image(-ICON_WIDTH / 2, -ICON_WIDTH / 2, ICON_WIDTH, ICON_WIDTH,
                        f"./images/icons/{icon}.png", embed=True,
                        transform=f"rotate({angle}) translate({RADIUS}, 0), rotate(90)")

        angle = 360 * (i + 0.5) / len(ICONS)
        yield svg.Rectangle(0, -LINE_WIDTH / 2, LINE_LENGTH, LINE_WIDTH, fill=Color.ENGRAVE,
                            transform=f"rotate({angle}) translate({RADIUS - LINE_LENGTH / 2}, 0)")


if __name__ == "__main__":
    draw_spinner()
