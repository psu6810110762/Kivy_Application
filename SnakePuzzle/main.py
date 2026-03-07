from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle
from game_engine import GameEngine


# กำหนดขนาดหน้าจอเกม (กว้าง x สูง)
CELL_SIZE = 20
GRID_WIDTH = 800 // CELL_SIZE
GRID_HEIGHT = 600 // CELL_SIZE

class MenuScreen(Screen):
    pass


class GameScreen(Screen):
    pass


class GameBoard(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.draw_grid, pos=self.draw_grid)

    def draw_grid(self, *args):
        self.canvas.before.clear()
        self.canvas.clear()

        cell = 40

        # วาดพื้น + grid
        with self.canvas.before:
            Color(0, 0, 0, 1)
            Rectangle(pos=self.pos, size=self.size)

            Color(0.2, 0.2, 0.2, 1)

            for x in range(0, int(self.width), cell):
                Line(points=[self.x + x, self.y,
                            self.x + x, self.top])

            for y in range(0, int(self.height), cell):
                Line(points=[self.x, self.y + y,
                            self.right, self.y + y])

        # งู
        with self.canvas:
            Color(0, 1, 0, 1)  # เขียว
            Rectangle(pos=(self.x + 5*cell, self.y + 5*cell),
                    size=(cell, cell))

            # แอปเปิ้ล
            Color(1, 0, 0, 1)  # แดง
            Rectangle(pos=(self.x + 8*cell, self.y + 8*cell),
                    size=(cell, cell))


class SnakeGame(Widget):
    # คลาสนี้คือ "กระดานเกม" เดี๋ยวเราจะมาเขียนตัวงูและแอปเปิ้ลลงในนี้
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.engine = GameEngine()
        Window.bind(on_key_down=self.on_key_down)

    def on_key_down(self, window, key, *args):
        if key == 276:
            self.engine.step(-1,0)
        elif key == 275:
            self.engine.step(1,0)
        elif key == 273:
            self.engine.step(0,1)

        print(self.engine.snake)


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