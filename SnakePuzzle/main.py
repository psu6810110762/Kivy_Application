from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen

# กำหนดขนาดหน้าจอเกม (กว้าง x สูง)
CELL_SIZE = 20
GRID_WIDTH = 800 // CELL_SIZE
GRID_HEIGHT = 600 // CELL_SIZE

class MenuScreen(Screen):
    pass

class GameScreen(Screen):
    pass

class SnakeGame(Widget):
    # คลาสนี้คือ "กระดานเกม" เดี๋ยวเราจะมาเขียนตัวงูและแอปเปิ้ลลงในนี้
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.snake = [(3,5), (2,5)]
        self.walls = [(0,0), (1,0), (2,0), (3,0)]  # พื้น
        self.apples = [(6,5)]
        self.portal = (10,5)
        self.game_over = False

        self.direction = (0,0)

        Window.bind(on_key_down=self.on_key_down)
       

    def apply_gravity(self):
        while True:
            supported = False

            for x, y in self.snake:
                below = (x, y - 1)

                # ถ้ามีพื้นรองรับจริง ๆ
                if below in self.walls:
                    supported = True
                    break

                # ตกเหว
                if y - 1 < 0:
                    self.game_over = True
                    print("GAME OVER")
                    return

            if supported:
                return  # มีพื้นแล้ว หยุดตก

            # ไม่มีพื้นเลย → ร่วงลง
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

    def on_key_down(self, window, key, *args):
        moved = False

        if key == 276:
            moved = self.move(-1,0)
        elif key == 275:
            moved = self.move(1,0)
        elif key == 273:
            moved = self.move(0,1)

        if moved:
            self.apply_gravity()
            self.check_apple()
            self.check_portal()

    def check_apple(self):
        head = self.snake[0]

        if head in self.apples:
            self.apples.remove(head)

        # เพิ่มความยาว 1 ช่อง (ต่อท้าย)
            self.snake.append(self.snake[-1])

    def check_portal(self):
        if self.snake[0] == self.portal:
            print("LEVEL COMPLETE")

class SnakeApp(App):
    def build(self):
        sm = ScreenManager()

        sm.add_widget(MenuScreen(name="menu"))

        game_screen = GameScreen(name="game")
        game_screen.add_widget(SnakeGame())
        sm.add_widget(game_screen)

        return sm

if __name__ == '__main__':
    # สั่งรันแอป
    SnakeApp().run()