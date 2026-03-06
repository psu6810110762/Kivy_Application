from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import (Color, Line, Rectangle, Ellipse,
                            RoundedRectangle, PushMatrix,
                            PopMatrix, Rotate, Translate)

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
        if not snake:
            return

        for i, (sx, sy) in enumerate(snake):
            x = ox + sx * c
            y = oy + sy * c

        # หาทิศทางของแต่ละ segment
            if i == 0:
            # หัวงู — หาทิศจาก head → segment ถัดไป
                if len(snake) > 1:
                    nx, ny = snake[1]
                    dx, dy = sx - nx, sy - ny
                else:
                    dx, dy = 1, 0
                source = 'assets/head.png'

            elif i == len(snake) - 1:
            # หาง — หาทิศจาก segment ก่อนหน้า → tail
                px, py = snake[i-1]
                dx, dy = sx - px, sy - py
                source = 'assets/tail.png'

            else:
            # ตัวงู — หาทิศจาก segment ก่อน → ถัดไป
                px, py = snake[i-1]
                dx, dy = px - sx, py - sy
                source = 'assets/body.png'

        # หมุนรูปตามทิศทาง
        # dx,dy:  (1,0)=ขวา  (-1,0)=ซ้าย  (0,1)=ขึ้น  (0,-1)=ลง
            angle_map = {
                ( 1,  0): 0,    # ขวา
                (-1,  0): 180,  # ซ้าย
                ( 0,  1): 90,   # ขึ้น
                ( 0, -1): 270,  # ลง
            }
            angle = angle_map.get((dx, dy), 0)

            Color(1, 1, 1, 1)
            PushMatrix()
            Translate(x + c/2, y + c/2)
            Rotate(angle=angle, axis=(0, 0, 1), origin=(0, 0))
            Rectangle(
                source=source,
                pos=(-c/2, -c/2),
                size=(c, c))
            PopMatrix()

    def draw_apple(self, apples, ox, oy, c):
        Color(1, 1, 1, 1)
        for (ax, ay) in apples:
            Rectangle(
            source='assets/apple.png',
            pos=(ox + ax*c, oy + ay*c),
            size=(c, c)
        )

    def draw_portal(self, portal, ox, oy, c):
        px, py = portal
        Color(1, 1, 1, 1)
        Rectangle(
        source='assets/portal.png',
        pos=(ox + px*c, oy + py*c),
        size=(c, c)
    )

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
            #rock
            # rocks
        Color(0.5, 0.5, 0.5, 1)
for (rx, ry) in state["rocks"]:
    Rectangle(pos=(ox+rx*c, oy+ry*c), size=(c, c))
# เส้นขอบหิน
Color(0.35, 0.35, 0.35, 1)
for (rx, ry) in state["rocks"]:
    Line(rectangle=(ox+rx*c, oy+ry*c, c, c), width=1.5)
    
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


if __name__ == "__main__":
    SnakeApp().run()