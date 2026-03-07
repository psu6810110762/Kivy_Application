# levels.py
def make_platform(x1, x2, y1, y2):
    """สร้าง wall tiles สำหรับ platform สี่เหลี่ยม"""
    tiles = set()
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            tiles.add((x, y))
    return tiles


# ── Platform ทั้งหมดของด่าน 1 ────────────────────────────────────────────────

# ฐานซ้าย (x 0-4, y=4 เท่านั้น)
_left  = make_platform(0, 4, 4, 4)

# ฐานกลาง (x 7-12, y=4 เท่านั้น)
_mid   = make_platform(7, 12, 4, 4)

# ฐานขวา (x 15-19, y=4 เท่านั้น)
_right = make_platform(15, 19, 4, 4)

_all_walls = _left | _mid | _right

LEVELS = [
    {
        "name":       "ก้าวแรกบนฟ้า",
        "background": "assets/bg_sky.png",      # ← เพิ่ม
        "snake":  [(3, 5), (2, 5), (1, 5)],
        "walls":  _all_walls,
        "apples": [(9, 5)],
        "portal": (18, 5),
    },
    # ด่าน 2
    {
        "name":       "ป่าลึก",
        "background": "assets/bg_forest.png",
        "snake":  [(3, 5), (2, 5), (1, 5)],
        "walls":  _all_walls,
        "apples": [(9, 5)],
        "portal": (18, 5),
    },
    # ด่าน 3
    {
        "name":       "ใต้ทะเล",
        "background": "assets/bg_ocean.png",
        "snake":  [(3, 5), (2, 5), (1, 5)],
        "walls":  _all_walls,
        "apples": [(9, 5)],
        "portal": (18, 5),
    },
    # ด่าน 4
    {
        "name":       "ถ้ำมืด",
        "background": "assets/bg_cave.png",
        "snake":  [(3, 5), (2, 5), (1, 5)],
        "walls":  _all_walls,
        "apples": [(9, 5)],
        "portal": (18, 5),
    },
    # ด่าน 5
    {
        "name":       "อวกาศ",
        "background": "assets/bg_space.png",
        "snake":  [(3, 5), (2, 5), (1, 5)],
        "walls":  _all_walls,
        "apples": [(9, 5)],
        "portal": (18, 5),
    },
]
