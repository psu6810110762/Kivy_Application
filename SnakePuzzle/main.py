from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import (Color, Line, Rectangle, Ellipse,
                            RoundedRectangle, PushMatrix,
                            PopMatrix, Rotate, Translate)
from kivy.clock import Clock
from game_engine import GameEngine

CELL = 40
Window.size = (800, 600)


class MenuScreen(Screen):
    pass

class SelectLevelScreen(Screen):
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
        self._fall_event = None
        self.bind(size=self.redraw, pos=self.redraw)
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self.on_key_down)
        self.is_paused = False

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self.on_key_down)
        self._keyboard = None

    def on_key_down(self, keyboard, keycode, text, modifiers):
        if getattr(self, 'is_paused', False):
            return
        key = keycode[0]

        if self.engine.game_over:
            if text == 'r' or key == 13:
                self.engine.reset_level()
                self.redraw()
            return
        
        if self.engine.level_complete:
            if text == 'r' or key == 13: # (แถม: กด Enter เพื่อไปด่านต่อไปได้เลย)
                self.engine.next_level()
                self.redraw()
            return
        
        if self.engine.game_won:
            if text == 'r' or key == 13:
                self.engine.restart_game()
                self.redraw()
            return

        # ถ้ากำลัง falling อยู่ ไม่รับ input
        if self._fall_event:
            return

        key_map = {
            276: (-1, 0),
            275: ( 1, 0),
            273: ( 0, 1),
            274: ( 0,-1),
        }
        if key in key_map:
            self.engine.step(*key_map[key])
            self._start_fall_animation()  # ← เรียก fall animation
            self.redraw()
        elif text == 'r':
            self.engine.reset_level()
            self.redraw()

    def _start_fall_animation(self):
        """เช็คว่าต้องตกมั้ย ถ้าใช่ให้เริ่ม animate"""
        still_falling = self.engine.apply_gravity()
        self.redraw()
        if still_falling:
            self._fall_event = Clock.schedule_interval(self._fall_step, 0.08)

    def _fall_step(self, dt):
        """เรียกทุก 0.08 วินาที ให้งูตกทีละ step"""
        still_falling = self.engine.apply_gravity()
        self.redraw()
        if  self.engine.game_over or not still_falling:
            self._fall_event.cancel()
            self._fall_event = None
            if not self.engine.game_over:
                self.engine.check_apple()
                self.engine.check_portal()
                self.redraw()

    def _start_fall_animation(self):
        """เช็คว่าต้องตกมั้ย ถ้าใช่ให้เริ่ม animate"""
        still_falling = self.engine.apply_gravity()
        self.redraw()
        if still_falling:
            self._fall_event = Clock.schedule_interval(self._fall_step, 0.08)

    def _fall_step(self, dt):
        """เรียกทุก 0.08 วินาที ให้งูตกทีละ step"""
        still_falling = self.engine.apply_gravity()
        self.redraw()
        if  self.engine.game_over or not still_falling:
            self._fall_event.cancel()
            self._fall_event = None
            if not self.engine.game_over:
                self.engine.check_apple()
                self.engine.check_portal()
                self.redraw()

    # ------------------------------------------------------------------
    def draw_snake(self, snake, ox, oy, c):
        if not snake:
            return

        for i, (sx, sy) in enumerate(snake):
            x = ox + sx * c
            y = oy + sy * c

            if i == 0:
                if len(snake) > 1:
                    nx, ny = snake[1]
                    dx, dy = sx - nx, sy - ny
                else:
                    dx, dy = 1, 0
                source = 'assets/head3.png'

            elif i == len(snake) - 1:
                px, py = snake[i - 1]
                dx, dy = sx - px, sy - py
                source = 'assets/tail2.png'

            else:
                px, py = snake[i - 1]
                dx, dy = px - sx, py - sy
                source = 'assets/body3.png'

            angle_map = {
                ( 1,  0): 0,
                (-1,  0): 180,
                ( 0,  1): 90,
                ( 0, -1): 270,
            }
            angle = angle_map.get((dx, dy), 0)

            Color(1, 1, 1, 1)
            PushMatrix()
            Translate(x + c / 2, y + c / 2)
            Rotate(angle=angle, axis=(0, 0, 1), origin=(0, 0))
            Rectangle(source=source, pos=(-c / 2, -c / 2), size=(c, c))
            PopMatrix()

    def draw_apple(self, apples, ox, oy, c):
        Color(1, 1, 1, 1)
        for (ax, ay) in apples:
            Rectangle(
                source='assets/apple.png',
                pos=(ox + ax * c, oy + ay * c),
                size=(c, c)
            )

    def draw_portal(self, portal, ox, oy, c):
        px, py = portal
        Color(1, 1, 1, 1)
        Rectangle(
            source='assets/portal.png',
            pos=(ox + px * c, oy + py * c),
            size=(c, c)
        )

    # ------------------------------------------------------------------
    def redraw(self, *args):
        self.canvas.clear()
        state = self.engine.get_state()
        c  = CELL
        ox = self.x
        oy = self.y

        with self.canvas:

            Color(1, 1, 1, 1)
            Rectangle(
                source=state["background"],
                pos=self.pos,
                size=self.size
            )

            # walls
            Color(0.35, 0.38, 0.55, 0.85)
            for (wx, wy) in state["walls"]:
                Rectangle(pos=(ox+wx*c, oy+wy*c), size=(c, c))
            Color(0.60, 0.63, 0.80, 1)
            for (wx, wy) in state["walls"]:
                Line(points=[ox+wx*c, oy+wy*c+c,
                              ox+wx*c+c, oy+wy*c+c], width=2)

            # rocks
            Color(0.5, 0.5, 0.5, 1)
            for (rx, ry) in state["rocks"]:
                Rectangle(pos=(ox+rx*c, oy+ry*c), size=(c, c))
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

            app = App.get_running_app()
            if app and app.root and app.root.has_screen("game"):
                screen = app.root.get_screen("game")
                
                # อัปเดต Level
                if 'level_label' in screen.ids:
                    current_lv = state["current_level"] + 1
                    screen.ids.level_label.text = f'LEVEL  {current_lv}'
                    
                # อัปเดต Apple
                if 'apple_label' in screen.ids:
                    apples_left = len(state["apples"])
                    screen.ids.apple_label.text = f'APPLES LEFT: {apples_left}'

                # เช็คสถานะ Game Over เพื่อสลับแสดงหน้าต่าง
                if 'game_over_layout' in screen.ids:
                    is_over = state["game_over"]
                    screen.ids.game_over_layout.opacity = 1 if is_over else 0
                    screen.ids.game_over_layout.disabled = not is_over

                # เช็คสถานะผ่านด่าน (Level Complete) แต่ยังไม่จบเกมสุดท้าย
                if 'level_complete_layout' in screen.ids:
                    is_cleared = state["level_complete"] and not state["game_won"]
                    screen.ids.level_complete_layout.opacity = 1 if is_cleared else 0
                    screen.ids.level_complete_layout.disabled = not is_cleared

                # เช็คสถานะ Game Won
                if 'game_won_layout' in screen.ids:
                    is_won = state["game_won"]
                    screen.ids.game_won_layout.opacity = 1 if is_won else 0
                    screen.ids.game_won_layout.disabled = not is_won

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
        sm.add_widget(SelectLevelScreen(name="select_level"))
        sm.add_widget(GameScreen(name="game"))
        return sm
    
    def start_level(self, level_index):
        # ดึงหน้าต่างเกมขึ้นมา
        screen = self.root.get_screen("game")
        board = screen.ids.game_board
        
        # บังคับโหลดด่านตามเลขที่ส่งมา (Index เริ่มที่ 0)
        board.engine.current_level = level_index
        board.engine.game_won = False
        board.engine.load_level(level_index)
        
        # ปิดหน้าต่าง UI ที่อาจจะค้างอยู่ (Pause, Game Over, etc.)
        board.is_paused = False
        for layout_id in ['game_over_layout', 'level_complete_layout', 'game_won_layout', 'pause_layout']:
            if layout_id in screen.ids:
                screen.ids[layout_id].opacity = 0
                screen.ids[layout_id].disabled = True
                
        # วาดหน้าจอใหม่ แล้วสลับไปหน้าเกม
        board.redraw()
        self.root.current = "game"


if __name__ == "__main__":
    SnakeApp().run()