from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivy.uix.recycleview import RecycleView
from RepairRecordBox import RepairRecordBox

Builder.load_file('kv/RepairsPanel.kv')

class RepairsPanel(RecycleView):
    records = ListProperty([])
    pass