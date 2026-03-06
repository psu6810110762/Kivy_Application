# levels.py
def make_platform(x1, x2, y1, y2):
    tiles = set()
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            tiles.add((x, y))
    return tiles

# ── ด่าน 1 ──────────────────────────────────────────────────────────────────
# พื้นบน  col 7-11, row 10 → y_kivy = 20-10 = 10
_d1_top    = make_platform(7, 11, 10, 10)
# พื้นล่าง col 6-12, row 13 → y_kivy = 20-13 = 7
_d1_bottom = make_platform(6, 12, 7, 7)
_d1_walls  = _d1_top | _d1_bottom

# ── ด่าน 2-5 (ใช้ชั่วคราว) ──────────────────────────────────────────────────
_temp = make_platform(0, 4, 4, 4) | make_platform(7, 12, 4, 4) | make_platform(15, 19, 4, 4)

# ── ด่าน 2 ──────────────────────────────────────────────────────────────────
_d2_left   = make_platform(3,  9,  5, 5)   # พื้นซ้าย (เว้น col 10)
_d2_right  = make_platform(11, 14, 5, 5)   # พื้นขวา (เว้น col 10)
_d2_low    = make_platform(8,  12,  4, 4)   # พื้นต่ำ
_d2_mid    = make_platform(8,  9,  7, 7)   # พื้นกลาง
_d2_step   = make_platform(10, 10, 7, 8)   # ขั้นบันได
_d2_walls  = _d2_left | _d2_right | _d2_low | _d2_mid | _d2_step

# ── ด่าน 3 ──────────────────────────────────────────────────────────────────
_d3_a = make_platform(6,  7,  7, 9)   # แท่งซ้าย
_d3_b = make_platform(8,  12, 9, 9)   # พื้นบนกลาง
_d3_c = make_platform(6,  8,  5, 5)   # พื้นล่างซ้าย
_d3_d = make_platform(13, 13, 10, 13) # แท่งขวา
_d3_e = make_platform(14, 15, 10, 10) # พื้นขวาบน
_d3_f = make_platform(13, 14, 6, 8)   # พื้นขวาล่าง
_d3_walls = _d3_a | _d3_b | _d3_c | _d3_d | _d3_e | _d3_f

LEVELS = [
    # ด่าน 1
    {
        "name":       "ก้าวแรกบนฟ้า",
        "background": "assets/bg_sky.png",
        # งูเริ่ม row 12 → y_kivy = 20-12 = 8, หัวที่ col 9
        "snake":  [(9, 8), (8, 8), (7, 8)],
        "walls":  _d1_walls,
        # แอปเปิ้ล col 11, row 10 → y_kivy = 10+1 = 11 (บนพื้น y=10)
        "apples": [(12, 10),(6, 10)],
        "rocks": [(8, 12)],  # ก้อนหินตำแหน่งเริ่มต้น
        # วางประตูบนพื้นบน col 7, y=11
        "portal": (10,14),
    },
    # ด่าน 2
    {
        "name":       "ป่าลึก",
        "background": "assets/bg_forest.png",
        "snake":  [(5, 6), (4, 6), (3, 6)],
        "walls":  _d2_walls,
        "apples": [(3, 9)],
        "portal": (14, 10),
        "rocks":  [(8, 8), (7, 6)],
    },
    # ด่าน 3
    {
        "name":       "ใต้ทะเล",
        "background": "assets/bg_ocean.png",
        "snake":  [(8, 6), (7, 6), (6, 6)],
        "walls":  _d3_walls,
        "apples": [(8, 10), (13, 14)],
        "portal": (14, 6),
        "rocks":  [(11, 8)],
    },
    # ด่าน 4
    {
        "name":       "ถ้ำมืด",
        "background": "assets/bg_cave.png",
        "snake":  [(3, 5), (2, 5), (1, 5)],
        "walls":  _temp,
        "apples": [(9, 5)],
        "portal": (18, 5),
    },
    # ด่าน 5
    {
        "name":       "อวกาศ",
        "background": "assets/bg_space.png",
        "snake":  [(3, 5), (2, 5), (1, 5)],
        "walls":  _temp,
        "apples": [(9, 5)],
        "portal": (18, 5),
    },
]