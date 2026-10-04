from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior

Builder.load_file('kv/RepairRecordBox.kv')

class RepairRecordBox(RecycleDataViewBehavior, BoxLayout):
    text = StringProperty("")
    Repair = ListProperty()

    def ShowRepairInfo(self):
        screen = App.get_running_app().sm.get_screen('repairdetails')
        screen.Repair = self.Repair
        App.get_running_app().sm.current='repairdetails'

    pass