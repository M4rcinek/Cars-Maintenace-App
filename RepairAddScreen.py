import re
from datetime import datetime
from decimal import Decimal

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.screenmanager import Screen

Builder.load_file('kv/RepairAddScreen.kv')

class RepairAddScreen(Screen):

    def RefreshLabels(self):
        self.ids.button_cancel.text = App.get_running_app().get_translation("cancel")
        self.ids.button_save.text = App.get_running_app().get_translation("save")
        self.ids.cost_text.text = App.get_running_app().get_translation("cost")
        self.ids.mileage_text.text = App.get_running_app().get_translation("mileage")
        self.ids.repair_date_text.text = App.get_running_app().get_translation("repair_date")
        self.ids.part_number_text.text = App.get_running_app().get_translation("part_number")
        self.ids.reg_number_text.text = App.get_running_app().get_translation("reg_number")
        self.ids.repair_type_text.text = App.get_running_app().get_translation("repair_type")
        self.ids.description_text.text = App.get_running_app().get_translation("description")

    def on_enter(self, *args):
        self.ids.reg_number.text = self.reg_number

    def GetBack(self):
        App.get_running_app().sm.current='repairs'

    def SaveAndAdd(self):
        Type = self.ids.repair_type.text
        Description = self.ids.description.text
        Cost = self.ids.cost.text
        Mileage = self.ids.mileage.text
        RepairDate = self.ids.repair_date.text
        PartNumber = self.ids.part_number.text
        RegNumber = self.reg_number

        if not (Mileage.isdigit() and re.match(r"^\d{4}-\d{2}-\d{2}$", RepairDate) and re.match(r"^\d+\.\d{2}$",Cost)):
            App.get_running_app().show_popup_acknowledge(App.get_running_app().get_translation('bad_data_popup'))
            pass

        try:
            conn = App.get_running_app().conn
            cursor = conn.cursor()
            cursor.execute("INSERT INTO repairs (repair_type,description,cost,repair_date,part_number,reg_number,mileage) "
                           "values(%s,%s,%s,%s,%s,%s,%s)", (
                           Type, Description, Decimal(Cost), datetime.strptime(RepairDate, "%Y-%m-%d").date(),
                           PartNumber, RegNumber,int(Mileage)))
            conn.commit()
            App.get_running_app().show_popup_acknowledge(App.get_running_app().get_translation('success_adding_record'))

        except:
            App.get_running_app().show_popup_acknowledge(App.get_running_app().get_translation('save_error_popup'))

    pass