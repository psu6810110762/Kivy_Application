#game_engine.py
from levels import LEVELS

class GameEngine:
    def __init__(self):
        print("INIT RUNNING")
        self.current_level = 0
        self.game_won = False
        self.load_level(self.current_level)
    
    def apply_gravity(self):
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

    def move(self, dx, dy):
        head_x, head_y = self.snake[0]
        new_head = (head_x + dx, head_y + dy)

    # กันออกนอกขอบหน้าจอ
        if new_head[0] < 0 or new_head[1] < 0:
            return False

    # ❌ เดินเข้าด้านข้างของ wall ไม่ได้
    # wall tile มีพื้นที่ทั้งช่อง — ถ้าหัวจะไปอยู่ใน wall = ชน
    # แต่งูเดิน "บน" wall ได้ (y = wall_y + 1)
    # ดังนั้นเช็คว่า new_head ตรงกับ wall tile ไหม
        if new_head in self.walls:
            return False

    # กันชนตัวเอง (ยกเว้นหาง เพราะหางจะขยับออกไป)
        body_without_tail = self.snake[:-1]
        if new_head in body_without_tail:
            return False

    # หัวใหม่ + ตัวเดิมตัดหางออก
        self.snake = [new_head] + self.snake[:-1]
        return True
    
    def step(self, dx, dy):

        if self.game_over:
            return

        # ถ้าด่านจบแล้ว ให้ไปด่านถัดไป
        if self.level_complete:
            self.next_level()
            return

        moved = self.move(dx, dy)

        if moved:
            self.apply_gravity()
            self.check_apple()
            self.check_portal()


    def check_portal(self):
        if self.snake[0] == self.portal:
            self.level_complete = True
            

    def get_state(self):
        return {
            "background": self.background,
            "snake": self.snake,
            "walls": self.walls,
            "apples": self.apples,
            "portal": self.portal,
            "game_over": self.game_over,
            "level_complete": self.level_complete,
            "current_level": self.current_level,
            "game_won": self.game_won
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

        self.snake = list(level["snake"])
        self.walls = list(level["walls"])
        self.apples = list(level["apples"])
        self.portal = level["portal"]

        self.snake = level["snake"].copy()
        print("Snake set:", self.snake)

        self.walls = level["walls"].copy()
        self.apples = level["apples"].copy()
        self.portal = level["portal"]

        self.background = level.get("background", "assets/bg_sky.png")  # ← เพิ่ม
        self.snake  = list(level["snake"])
        self.walls  = set(level["walls"])
        self.apples = list(level["apples"])
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
        self.game_won = False
        self.load_level(self.current_level)