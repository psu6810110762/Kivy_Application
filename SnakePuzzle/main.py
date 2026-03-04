from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock

# กำหนดขนาดหน้าจอเกม (กว้าง x สูง)
CELL_SIZE = 20
GRID_WIDTH = 800 // CELL_SIZE
GRID_HEIGHT = 600 // CELL_SIZE

class SnakeGame(Widget):
    # คลาสนี้คือ "กระดานเกม" เดี๋ยวเราจะมาเขียนตัวงูและแอปเปิ้ลลงในนี้
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # ทิศทางเริ่มต้น
        self.direction = (1, 0)
        # ตำแหน่งงู (หัวอยู่ index 0)
        self.snake = [(5, 5), (4, 5), (3, 5)]
        # เริ่ม Game Loop
        Clock.schedule_interval(self.update, 1/10)  # 10 FPS

    def move_snake(self):
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
    # เพิ่มหัวใหม่
        self.snake.insert(0, new_head)
    # ลบหางออก (ถ้ายังไม่กินอะไร)
        self.snake.pop()

    def check_collision(self):
        head_x, head_y = self.snake[0]
    # ชนขอบ
        if head_x < 0 or head_x >= GRID_WIDTH:
            return True
        if head_y < 0 or head_y >= GRID_HEIGHT:
            return True
    # ชนตัวเอง
        if self.snake[0] in self.snake[1:]:
            return True

        return False

class SnakeApp(App):
    def build(self):
        # ฟังก์ชันนี้ใช้สร้างหน้าจอตอนเปิดแอป
        return SnakeGame()

if __name__ == '__main__':
    # สั่งรันแอป
    SnakeApp().run()