MM_TO_PX = 3.7795275591


def mm_to_px(mm):
    return round(mm * MM_TO_PX)


A4_WIDTH, A4_HEIGHT = mm_to_px(210), mm_to_px(297)


def stickers(x, y, limit=None):
    for j in range(y):
        for i in range(x):
            n = i + j * x + 1

            if limit is not None and n > limit:
                return

            yield i, j, n


def draw_circle(draw, i, j, diameter, pitch, margin_left, margin_top):
    draw.ellipse((
            i * pitch + margin_left, j * pitch + margin_top,
            i * pitch + diameter + margin_left, j * pitch + diameter + margin_top
        ),
        fill=None,
        outline=(0, 0, 0)
    )
