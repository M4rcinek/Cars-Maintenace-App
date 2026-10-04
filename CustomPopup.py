from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup

Builder.load_file('kv/CustomPopup.kv')

class CustomPopup(Popup):
    callback = ObjectProperty(None)

    def on_yes(self):
        self.dismiss()
        if self.callback:
            self.callback(True)

    def on_no(self):
        self.dismiss()
        if self.callback:
            self.callback(False)