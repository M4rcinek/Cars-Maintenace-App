from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ListProperty, StringProperty
from kivy.uix.screenmanager import Screen
from RepairsPanel import RepairsPanel

Builder.load_file('kv/RepairsScreen.kv')

class RepairsScreen(Screen):
    reg_number = StringProperty("")
    data = ListProperty()

    def RefreshLabels(self):
        self.ids.button_add_repair.text = App.get_running_app().get_translation("add_repair")
        self.ids.button_cancel.text = App.get_running_app().get_translation("cancel")
        self.ids.input.hint_text = App.get_running_app().get_translation("search")
        self.ids.repairs_title_text.text = App.get_running_app().get_translation("repairs_for_this_car")
    def on_enter(self, *args):
        conn = App.get_running_app().conn
        cursor = conn.cursor()
        cursor.execute("Select * from repairs where reg_number = %s;", (self.reg_number,))
        self.records = cursor.fetchall()
        self.data = [{"Repair": r,"text": r[1] + " " + str(r[3]) + " " + r[2]} for r in self.records]

    def SearchRepair(self, Text):
        Data1 = []
        for i in self.records:
            if any(Text in str(item) for item in i):
                Data1.append(i)
        self.data = [{"Repair": r,"text": r[1] + " " + str(r[3]) + " " + r[2]} for r in Data1]

    def GetBack(self):
        App.get_running_app().sm.current = 'cardetails'

    def OpenAddRepairWindow(self):
        App.get_running_app().sm.current = 'repairadd'
        screen = App.get_running_app().sm.get_screen('repairadd')
        screen.reg_number = self.reg_number



    pass