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
        self.is_paused = False
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
            px, py = state["portal"]
            Color(0.6, 0.1, 0.6, 1)
            Rectangle(pos=(self.x + px*cell, self.y + py*cell), size=(cell, cell))
            Color(0.9, 0.5, 0.9, 1) # ขอบประตูสว่างๆ
            Line(rectangle=(self.x + px*cell, self.y + py*cell, cell, cell), width=1.5)

            #กำแพง
            for wx, wy in state["walls"]:
                Color(0.5, 0.3, 0.15, 1)
                Rectangle(pos=(self.x + wx*cell, self.y + wy*cell), size=(cell, cell))
                Color(0.2, 0.1, 0.05, 1) # เส้นขอบกำแพงสีเข้ม
                Line(rectangle=(self.x + wx*cell, self.y + wy*cell, cell, cell), width=1.2)

            #แอปเปิ้ล
            Color(0.9, 0.2, 0.2, 1)
            for ax, ay in state["apples"]:
                # วาดแอปเปิ้ลให้เล็กลงกว่าช่อง
                padding = 4
                Rectangle(pos=(self.x + ax*cell + padding, self.y + ay*cell + padding), 
                          size=(cell - padding*2, cell - padding*2))

            #งู
            snake_coords = state["snake"]
            if snake_coords:
                # ลำตัว
                Color(0.3, 0.8, 0.3, 1)
                for sx, sy in snake_coords[1:]:
                    # ลำตัวเล็กกว่าช่องนิดนึง
                    pad = 2
                    Rectangle(pos=(self.x + sx*cell + pad, self.y + sy*cell + pad), 
                              size=(cell - pad*2, cell - pad*2))
                
                # หัวงู
                hx, hy = snake_coords[0]
                Color(0.1, 0.5, 0.1, 1)
                Rectangle(pos=(self.x + hx*cell, self.y + hy*cell), size=(cell, cell))

        app = App.get_running_app()
        if app and app.root and app.root.has_screen("game"):
            screen = app.root.get_screen("game")
            
            current_level = state["current_level"] + 1
            apples_left = len(state["apples"])
            
            if 'level_label' in screen.ids:
                screen.ids.level_label.text = f"[color=#FFD84D][b]Level {current_level}[/b][/color]"
            if 'apple_label' in screen.ids:
                screen.ids.apple_label.text = f"[color=#FF5555][b]Apples: {apples_left}[/b][/color]"

    def on_key_down(self, window, key, *args):
        if self.is_paused or self.engine.game_over or self.engine.game_won: #ล็อกไม่ให้เดินถ้าอยู่ในหน้านี้
            return
        if key == 276:   # Left
            self.engine.step(-1, 0)
        elif key == 275: # Right
            self.engine.step(1, 0)
        elif key == 273: # Up
            self.engine.step(0, 1)
            
        # สั่งให้วาดกราฟิกใหม่ทุกครั้งที่กดปุ่มเดิน
        self.draw_elements()

        # เช็คว่าตาย/ตก หรือยัง
        app = App.get_running_app()
        if app and app.root and app.root.has_screen("game"):
            screen = app.root.get_screen("game")
            
            # กรณีตกเหว (Game Over)
            if self.engine.game_over:
                screen.ids.game_over_layout.opacity = 1
                screen.ids.game_over_layout.disabled = False
            
            # กรณีชนะเกม (Game Won)
            elif self.engine.game_won:
                screen.ids.game_won_layout.opacity = 1
                screen.ids.game_won_layout.disabled = False

    def restart_game(self):
        self.engine.restart_game()

        app = App.get_running_app()
        if app and app.root and app.root.has_screen("game"):
            screen = app.root.get_screen("game")
            screen.ids.game_over_layout.opacity = 0
            screen.ids.game_over_layout.disabled = True
            
            # ปิดหน้าต่างชนะด้วย
            if 'game_won_layout' in screen.ids:
                screen.ids.game_won_layout.opacity = 0
                screen.ids.game_won_layout.disabled = True
                
        self.draw_elements()

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        
        app = App.get_running_app()
        if app and app.root and app.root.has_screen("game"):
            screen = app.root.get_screen("game")
            if 'pause_layout' in screen.ids:
                screen.ids.pause_layout.opacity = 1 if self.is_paused else 0
                screen.ids.pause_layout.disabled = not self.is_paused

class SnakeApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(GameScreen(name="game"))
        return sm

if __name__ == '__main__':
    SnakeApp().run()