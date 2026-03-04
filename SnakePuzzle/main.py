from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window

# กำหนดขนาดหน้าจอเกม (กว้าง x สูง)
Window.size = (800, 600)

class SnakeGame(Widget):
    # คลาสนี้คือ "กระดานเกม" เดี๋ยวเราจะมาเขียนตัวงูและแอปเปิ้ลลงในนี้
    pass 

class SnakeApp(App):
    def build(self):
        # ฟังก์ชันนี้ใช้สร้างหน้าจอตอนเปิดแอป
        return SnakeGame()

if __name__ == '__main__':
    # สั่งรันแอป
    SnakeApp().run()