from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

Builder.load_file('kv/CustomTitleBar.kv')

class CustomTitleBar(BoxLayout):
    def __init__(self, **kwargs):
        super(CustomTitleBar, self).__init__(**kwargs)
        self.dragging = False

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.dragging = True
            self.touch_start = touch.pos
        return super(CustomTitleBar, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.dragging:
            x, y = touch.pos
            dx = x - self.touch_start[0]
            dy = y - self.touch_start[1]
            Window.left += dx
            Window.top -= dy
            self.touch_start = touch.pos
        return super(CustomTitleBar, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        self.dragging = False
        return super(CustomTitleBar, self).on_touch_up(touch)

    def minimize(self):
        Window.minimize()

    def maximize(self):
        if Window.fullscreen == 'auto':
            Window.fullscreen = False
        else:
            Window.fullscreen = 'auto'
