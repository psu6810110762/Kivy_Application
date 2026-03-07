# game_engine.py
from levels import LEVELS


class GameEngine:

    def __init__(self):
        print("INIT RUNNING")
        self.current_level = 0
        self.game_won = False
        self.rocks          = []
        self.load_level(self.current_level)

    # ------------------------------------------------------------------
    def apply_gravity(self):
        #หิน
        changed = True
        while changed:
            changed = False
            for i, (rx, ry) in enumerate(self.rocks):
                if ry - 1 < 0:
                    continue
                below = (rx, ry - 1)
                if below not in self.walls and below not in self.rocks:
                    self.rocks[i] = (rx, ry - 1)
                    changed = True

        #งู            
        """ตกทีละ 1 step — คืนค่า True ถ้ายังตกอยู่, False ถ้าหยุดแล้ว"""
        supported = False

        for x, y in self.snake:
            below = (x, y - 1)
            if below in self.walls:
                supported = True
                break
            if below in self.apples:  # ← เพิ่มตรงนี้
                supported = True
                break
            if below in self.rocks:
                supported = True
                break
            if y - 1 < 0:
                self.game_over = True 
                self.falling = True
                self.snake = [(x, y - 1) for x, y in self.snake]
                return True  # ยังตกอยู่

        if supported:
            self.falling = False
            return False  # หยุดแล้ว

        self.snake = [(x, y - 1) for x, y in self.snake]
        return True  # ยังตกอยู่

        # ── gravity หิน ─────────────────────────────────────────────────
        changed = True
        while changed:
            changed = False
            for i, (rx, ry) in enumerate(self.rocks):
                if ry - 1 < 0:
                    continue
                below = (rx, ry - 1)
                if below not in self.walls and below not in self.rocks:
                    self.rocks[i] = (rx, ry - 1)
                    changed = True

    # ------------------------------------------------------------------
    def move(self, dx, dy):
        head_x, head_y = self.snake[0]
        new_head = (head_x + dx, head_y + dy)

        if new_head[0] < 0 or new_head[1] < 0:
            return False

        # ชนก้อนหิน → ดันหิน
        if new_head in self.rocks:
            rock_new = (new_head[0] + dx, new_head[1] + dy)
            if (rock_new in self.walls or
                rock_new in self.rocks or
                rock_new[0] < 0 or rock_new[1] < 0):
                return False
            self.rocks.remove(new_head)
            self.rocks.append(rock_new)

        if new_head in self.walls:
            return False

        if new_head in self.snake[:-1]:
            return False

        self.snake = [new_head] + self.snake[:-1]
        return True

    # ------------------------------------------------------------------
    def step(self, dx, dy):
        if self.game_over:
            return

        # ถ้าจบด่านแล้วห้ามเดินต่อ
        if self.level_complete:
            return

        moved = self.move(dx, dy)
        if moved:
            self.apply_gravity()
            self.check_apple()
            self.check_portal()

    # ------------------------------------------------------------------
    def check_apple(self):
        head = self.snake[0]
        if head in self.apples:
            self.apples.remove(head)
            self.snake.append(self.snake[-1])

    # ------------------------------------------------------------------
    def check_portal(self):
        if self.snake[0] == self.portal:
            self.level_complete = True
            self.next_level()  # ← ไปด่านถัดไปทันที

    # ------------------------------------------------------------------
    def get_state(self):
        return {
            "background":     self.background,
            "snake":          self.snake,
            "walls":          self.walls,
            "apples":         self.apples,
            "portal":         self.portal,
            "rocks":          self.rocks,
            "game_over":      self.game_over,
            "level_complete": self.level_complete,
            "current_level":  self.current_level,
            "game_won":       self.game_won,
        }
    
    # def load_level(self, level_index):
    #     level = LEVELS[level_index]

    #     required_keys = ["snake", "walls", "apples", "portal"]
    #     for key in required_keys:
    #         if key not in level:
    #             raise ValueError(f"Level missing key: {key}")

    #     self.game_over = False
    #     self.level_complete = False

    def load_level(self, level_index):
        print("Loading level", level_index)

        level = LEVELS[level_index]

        self.snake = level["snake"].copy()
        print("Snake set:", self.snake)

        self.walls = level["walls"].copy()
        self.apples = level["apples"].copy()
        self.portal = level["portal"]

        required_keys = ["snake", "walls", "apples", "portal"]
        for key in required_keys:
            if key not in level:
                raise ValueError(f"Level missing key: {key}")

        self.background = level.get("background", "assets/bg_sky.png")  # ← เพิ่ม
        self.snake  = list(level["snake"])
        self.walls  = set(level["walls"])
        self.apples = list(level["apples"])
        self.rocks = list(level.get("rocks", []))
        self.portal = level["portal"]
        self.game_over = False
        self.level_complete = False

    def check_apple(self):
        head = self.snake[0]
        if head in self.apples:
            self.apples.remove(head)
            # ต่อหางในทิศตรงข้ามกับทิศที่หางกำลังเดิน
            tx, ty = self.snake[-1]
            if len(self.snake) >= 2:
                px, py = self.snake[-2]
                dx, dy = tx - px, ty - py  # ทิศหาง
            else:
                dx, dy = 0, -1
            self.snake.append((tx + dx, ty + dy))

    def reset_level(self):
        self.load_level(self.current_level)

    def next_level(self):
        if self.current_level + 1 < len(LEVELS):
            self.current_level += 1
            self.load_level(self.current_level)
        else:
            self.game_won = True

    def restart_game(self):
        self.current_level = 0
        self.game_won      = False
        self.load_level(self.current_level)