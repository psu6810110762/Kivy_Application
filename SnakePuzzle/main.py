from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import (Color, Line, Rectangle,
                            Ellipse, RoundedRectangle)

from game_engine import GameEngine

CELL = 40
Window.size = (800, 600)


class MenuScreen(Screen):
    pass


class GameScreen(Screen):
    def restart(self):
        for widget in self.walk():
            if isinstance(widget, GameBoard):
                widget.engine.reset_level()
                widget.redraw()
                break


class GameBoard(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.engine = GameEngine()
        self.bind(size=self.redraw, pos=self.redraw)
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self.on_key_down)

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self.on_key_down)
        self._keyboard = None

    def on_key_down(self, keyboard, keycode, text, modifiers):
        key = keycode[0]

        # ถ้า game over กด R หรือ Enter เพื่อเล่นใหม่
        if self.engine.game_over:
            if text == 'r' or key == 13:
                self.engine.reset_level()
                self.redraw()
            return

        key_map = {
            276: (-1,  0),
            275: ( 1,  0),
            273: ( 0,  1),
            274: ( 0, -1),
        }
        if key in key_map:
            self.engine.step(*key_map[key])
            self.redraw()
        elif text == 'r':
            self.engine.reset_level()
            self.redraw()

    # ------------------------------------------------------------------
    # draw helpers
    # ------------------------------------------------------------------
    def draw_snake(self, snake, ox, oy, c):
        for i, (sx, sy) in enumerate(snake):
            x = ox + sx * c
            y = oy + sy * c

            if i == 0:
                # หัวงู
                Color(0.1, 0.80, 0.35, 1)
                RoundedRectangle(pos=(x+2, y+2), size=(c-4, c-4), radius=[10])
                # ตาขาว
                Color(1, 1, 1, 1)
                Ellipse(pos=(x+7,  y+c-17), size=(9, 9))
                Ellipse(pos=(x+c-16, y+c-17), size=(9, 9))
                # ตาดำ
                Color(0.05, 0.05, 0.05, 1)
                Ellipse(pos=(x+9,  y+c-15), size=(5, 5))
                Ellipse(pos=(x+c-14, y+c-15), size=(5, 5))
                # ลิ้นแฉก
                Color(0.95, 0.2, 0.2, 1)
                Line(points=[x+c*0.5, y+4,
                              x+c*0.35, y-4], width=1.5)
                Line(points=[x+c*0.5, y+4,
                              x+c*0.65, y-4], width=1.5)
            else:
                # ตัวงู ไล่สีเข้มขึ้นตามความยาว
                t = i / max(len(snake) - 1, 1)
                Color(0.05, 0.65 - t * 0.2, 0.25, 1)
                RoundedRectangle(pos=(x+4, y+4), size=(c-8, c-8), radius=[7])
                # ลายเกล็ด
                Color(0.0, 0.45 - t * 0.1, 0.15, 0.5)
                Ellipse(pos=(x+10, y+10), size=(c-20, c-20))

    def draw_apple(self, apples, ox, oy, c):
        for (ax, ay) in apples:
            x = ox + ax * c
            y = oy + ay * c
            m = c * 0.1

            # ลูกแอปเปิ้ล
            Color(0.88, 0.12, 0.12, 1)
            Ellipse(pos=(x+m, y+m), size=(c-m*2, c-m*2))
            # เงาด้านซ้ายล่าง
            Color(0.55, 0.05, 0.05, 0.55)
            Ellipse(pos=(x+m, y+m), size=(c*0.4, c*0.4))
            # แสงสะท้อนด้านขวาบน
            Color(1, 0.65, 0.65, 0.65)
            Ellipse(pos=(x+c*0.52, y+c*0.50), size=(c*0.22, c*0.22))
            # ก้าน
            Color(0.35, 0.20, 0.04, 1)
            Line(points=[x+c*0.50, y+c-m*1.5,
                          x+c*0.62, y+c+2], width=2.5)
            # ใบ
            Color(0.18, 0.68, 0.18, 1)
            Ellipse(pos=(x+c*0.50, y+c-m*2), size=(c*0.28, c*0.18))

    def draw_portal(self, portal, ox, oy, c):
        px, py = portal
        x  = ox + px * c
        y  = oy + py * c
        cx = x + c / 2
        cy = y + c / 2

        # วงนอกสุด — ม่วงจาง
        Color(0.55, 0.05, 0.95, 0.35)
        Ellipse(pos=(x+2, y+2), size=(c-4, c-4))
        # วงแหวนชั้นนอก
        Color(0.80, 0.25, 1.0, 0.80)
        Line(circle=(cx, cy, c*0.44), width=3)
        # วงแหวนชั้นกลาง
        Color(0.95, 0.60, 1.0, 1)
        Line(circle=(cx, cy, c*0.28), width=2)
        # แกนกลางสว่าง
        Color(1, 1, 1, 1)
        Ellipse(pos=(cx-5, cy-5), size=(10, 10))
        # เส้นรัศมี 4 ทิศ
        Color(0.85, 0.45, 1.0, 0.55)
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            Line(points=[cx + dx*c*0.28, cy + dy*c*0.28,
                          cx + dx*c*0.44, cy + dy*c*0.44], width=1.5)

    # ------------------------------------------------------------------
    # redraw
    # ------------------------------------------------------------------
    def redraw(self, *args):
        self.canvas.clear()
        state = self.engine.get_state()
        c  = CELL
        ox = self.x
        oy = self.y

        with self.canvas:

            # background รูปภาพ
            Color(1, 1, 1, 1)
            Rectangle(
                source=state["background"],
                pos=self.pos,
                size=self.size
            )

            # grid จางๆ ทับ background
            Color(0, 0, 0, 0.15)
            for x in range(0, int(self.width) + c, c):
                Line(points=[ox+x, oy, ox+x, oy+self.height])
            for y in range(0, int(self.height) + c, c):
                Line(points=[ox, oy+y, ox+self.width, oy+y])

            # walls
            Color(0.35, 0.38, 0.55, 0.85)
            for (wx, wy) in state["walls"]:
                Rectangle(pos=(ox+wx*c, oy+wy*c), size=(c, c))
            Color(0.60, 0.63, 0.80, 1)
            for (wx, wy) in state["walls"]:
                Line(points=[ox+wx*c, oy+wy*c+c,
                              ox+wx*c+c, oy+wy*c+c], width=2)

            # apples
            self.draw_apple(state["apples"], ox, oy, c)

            # portal
            if not state["level_complete"]:
                self.draw_portal(state["portal"], ox, oy, c)

            # snake
            self.draw_snake(state["snake"], ox, oy, c)

            # overlay — game over
            if state["game_over"]:
                Color(0.8, 0.1, 0.1, 0.55)
                Rectangle(pos=self.pos, size=self.size)

            # overlay — level complete
            if state["level_complete"]:
                Color(0.1, 0.8, 0.4, 0.45)
                Rectangle(pos=self.pos, size=self.size)

            # overlay — game won
            if state["game_won"]:
                Color(0.9, 0.7, 0.1, 0.55)
                Rectangle(pos=self.pos, size=self.size)


class SnakeApp(App):

    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(GameScreen(name="game"))
        return sm


if __name__ == "__main__":
    SnakeApp().run()