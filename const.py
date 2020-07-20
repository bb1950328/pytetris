BOARD_WIDTH = 10
BOARD_HEIGHT = 20

BOARD_TILE_PX = 32

SIDEBAR_WIDTH_PX = 128


def scale(factor):
    for k in globals().keys():
        if k.lower().endswith("px"):
            globals()[k] = int(globals()[k] * factor)
