from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Line, Rectangle

from game_engine import GameEngine

# กำหนดขนาดหน้าจอเกม (กว้าง x สูง)
Window.size = (800, 600)

CELL_SIZE = 40
GRID_WIDTH = 800 // CELL_SIZE
GRID_HEIGHT = 600 // CELL_SIZE

class MenuScreen(Screen):
    pass


class GameScreen(Screen):
    pass


class SnakeGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.engine = GameEngine()
        Window.bind(on_key_down=self.on_key_down)
        
        # ผูกฟังก์ชันวาดเข้ากับการเปลี่ยนขนาดหน้าจอ
        self.bind(size=self.draw_elements, pos=self.draw_elements)

    def draw_elements(self, *args):
        # เคลียร์ Canvas ก่อนวาดเฟรมใหม่
        self.canvas.clear()
        
        cell = CELL_SIZE
        state = self.engine.get_state()

        with self.canvas:
            #ประตูมิติ
            Color(0.8, 0.2, 0.8, 1)
            px, py = state["portal"]
            Rectangle(pos=(self.x + px*cell, self.y + py*cell), size=(cell, cell))

            #กำแพง
            Color(0.6, 0.4, 0.2, 1)
            for wx, wy in state["walls"]:
                Rectangle(pos=(self.x + wx*cell, self.y + wy*cell), size=(cell, cell))

            #แอปเปิ้ล
            Color(0.9, 0.2, 0.2, 1)
            for ax, ay in state["apples"]:
                Rectangle(pos=(self.x + ax*cell, self.y + ay*cell), size=(cell, cell))

            #งู
            Color(0.2, 0.8, 0.2, 1)
            for sx, sy in state["snake"]:
                Rectangle(pos=(self.x + sx*cell, self.y + sy*cell), size=(cell, cell))

    def on_key_down(self, window, key, *args):
        if key == 276:   # Left
            self.engine.step(-1, 0)
        elif key == 275: # Right
            self.engine.step(1, 0)
        elif key == 273: # Up
            self.engine.step(0, 1)
            
        # สั่งให้วาดกราฟิกใหม่ทุกครั้งที่กดปุ่มเดิน
        self.draw_elements()

class SnakeApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(GameScreen(name="game"))
        return sm

if __name__ == '__main__':
    SnakeApp().run()