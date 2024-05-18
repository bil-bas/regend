import drawsvg as svg

from .utils import mm_to_px, A4_WIDTH, A4_HEIGHT, Color, create_page

CIRCLE_RADIUS = mm_to_px(37 / 2)
FULL_RADIUS = A4_WIDTH / 3
LINE_WIDTH = mm_to_px(3)
NUM_ACTIONS = 7


def draw_circles() -> None:
    with create_page("board_actions", format="pdf") as page:
        for n in range(NUM_ACTIONS):
            angle = n * 360 / NUM_ACTIONS
            transform = f"translate({A4_WIDTH / 2}, {A4_HEIGHT / 2}), rotate({angle}), translate({FULL_RADIUS}, 0)"
            page.append(svg.Circle(0, 0, CIRCLE_RADIUS, stroke=Color.DRAW, fill="none", stroke_width=LINE_WIDTH,
                        transform=transform))
