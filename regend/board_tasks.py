import drawsvg as svg

from .utils import mm_to_px, A4_WIDTH, A4_HEIGHT, stickers, Color, create_page

RADIUS = mm_to_px(51 / 2)
PITCH = mm_to_px(56)
MARGIN_TOP = mm_to_px(6)
MARGIN_LEFT = mm_to_px(20)
LINE_WIDTH = mm_to_px(3)


def draw_circles(prefix: str, num_tasks: int) -> None:
    with create_page(f"{prefix}_board_tasks", "pdf") as page:
        for i, j, _ in stickers(3, 5, num_tasks + 2):
            x, y = MARGIN_LEFT + (i + 0.5) * PITCH, MARGIN_TOP + (j + 0.5) * PITCH
            page.append(svg.Circle(x, y, RADIUS, fill="none", stroke="black", stroke_width=LINE_WIDTH))

