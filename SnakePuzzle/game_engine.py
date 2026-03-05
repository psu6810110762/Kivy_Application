from levels import LEVELS

class GameEngine:
    def __init__(self):
        self.current_level = 0
        self.game_won = False
        self.load_level(self.current_level)
    
    def apply_gravity(self):
        while True:
            supported = False

            for x, y in self.snake:
                below = (x, y - 1)

                # มีพื้นจริงรองรับ
                if below in self.walls:
                    supported = True
                    break

                # ตกเหว
                if y - 1 < 0:
                    self.game_over = True
                    return

            if supported:
                return

            self.snake = [(x, y - 1) for x, y in self.snake]

    def move(self, dx, dy):
        new_positions = [(x+dx, y+dy) for x,y in self.snake]
        for pos in new_positions:
            if pos in self.walls:
                return False
        # กันชนตัวเอง
        if len(set(new_positions)) != len(new_positions):
            return False
        self.snake = new_positions
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

    def check_apple(self):
        head = self.snake[0]

        if head in self.apples:
            self.apples.remove(head)
            self.snake.append(self.snake[-1])

    def check_portal(self):
        if self.snake[0] == self.portal:
            self.level_complete = True
            

    def get_state(self):
        return {
            "snake": self.snake,
            "walls": self.walls,
            "apples": self.apples,
            "portal": self.portal,
            "game_over": self.game_over,
            "level_complete": self.level_complete,
            "current_level": self.current_level,
            "game_won": self.game_won
        }
    
    def load_level(self, level_index):
        level = LEVELS[level_index]

        self.snake = list(level["snake"])
        self.walls = list(level["walls"])
        self.apples = list(level["apples"])
        self.portal = level["portal"]

        required_keys = ["snake", "walls", "apples", "portal"]
        for key in required_keys:
            if key not in level:
                raise ValueError(f"Level missing key: {key}")

        self.game_over = False
        self.level_complete = False

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