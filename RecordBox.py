from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior

Builder.load_file('kv/RecordBox.kv')


class RecordBox(RecycleDataViewBehavior, BoxLayout):
    text = StringProperty("")
    car = ListProperty()

    def ShowCarInfo(self):
        screen = App.get_running_app().sm.get_screen('cardetails')
        screen.car = self.car
        App.get_running_app().sm.current = 'cardetails'

    def refresh_view_attrs(self, rv, index, data):
        super().refresh_view_attrs(rv, index, data)

        if self.car and len(self.car) > 7:
            if self.car[7]:
                self.ids.car_photo.source = self.car[7]
            else:
                self.ids.car_photo.source = "media/default_car.jpg"

        return True

    pass