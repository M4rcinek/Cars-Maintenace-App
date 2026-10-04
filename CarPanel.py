from kivy.app import App
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from RecordBox import RecordBox

Builder.load_file('kv/CarPanel.kv')

class CarPanel(RecycleView):
    records = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.LoadCars()

    def LoadCars(self):
        conn = App.get_running_app().conn
        cursor = conn.cursor()
        cursor.execute("Select * from cars;")
        self.records = cursor.fetchall()
        self.data = [{"car": r,"text": r[0] + " " + r[1] + " " + r[2]} for r in self.records]

    def SearchCars(self, Text):
        Data1 = []
        for i in self.records:
            if any(Text.upper() in str(item) for item in i):
                Data1.append(i)
        self.data = [{"car": r,"text": r[0] + " " + r[1] + " " + r[2]} for r in Data1]
    pass