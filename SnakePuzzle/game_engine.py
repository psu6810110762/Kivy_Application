class GameEngine:
    def __init__(self):
        self.snake = [(3,5), (2,5)]
        self.walls = [(0,0), (1,0), (2,0), (3,0)]
        self.apples = [(6,5)]
        self.portal = (10,5)

        self.game_over = False
        self.level_complete = False
    
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
        if self.game_over or self.level_complete:
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
            "level_complete": self.level_complete
        }