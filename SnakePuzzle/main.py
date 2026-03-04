from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from game_engine import GameEngine


# กำหนดขนาดหน้าจอเกม (กว้าง x สูง)
CELL_SIZE = 20
GRID_WIDTH = 800 // CELL_SIZE
GRID_HEIGHT = 600 // CELL_SIZE

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
        # ฟังก์ชันนี้ใช้สร้างหน้าจอตอนเปิดแอป
        return SnakeGame()

if __name__ == '__main__':
    # สั่งรันแอป
    SnakeApp().run()