import re
from datetime import datetime
from decimal import Decimal

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.screenmanager import Screen

Builder.load_file('kv/RepairDetailsScreen.kv')

class RepairDetailsScreen(Screen):

    Repair = ListProperty([])

    def RefreshLabels(self):
        self.ids.button_cancel.text = App.get_running_app().get_translation("cancel")
        self.ids.cost_text.text = App.get_running_app().get_translation("cost")
        self.ids.mileage_text.text = App.get_running_app().get_translation("mileage")
        self.ids.repair_date_text.text = App.get_running_app().get_translation("repair_date")
        self.ids.part_number_text.text = App.get_running_app().get_translation("part_number")
        self.ids.reg_number_text.text = App.get_running_app().get_translation("reg_number")

    def on_enter(self, *args):
        self.ids.repair_type_value.text = self.Repair[1]
        self.ids.description_value.text = self.Repair[2]
        self.ids.cost_value.text = str(self.Repair[3])
        self.ids.repair_date_value.text = str(self.Repair[4])
        self.ids.part_number_value.text = self.Repair[5]
        self.ids.reg_number_value.text = self.Repair[6]
        self.ids.mileage_value.text = str(self.Repair[7])
        self.ids.button_edit.bind(on_release=self.EditRepairData)
        self.ids.button_cancel.bind(on_release=self.GetBack)

    def SaveEditData(self,*args):
        Type = self.ids.repair_type_value.text
        Description = self.ids.description_value.text
        Cost = self.ids.cost_value.text
        Mileage = self.ids.mileage_value.text
        RepairDate = self.ids.repair_date_value.text
        PartNumber = self.ids.part_number_value.text

        if not (Mileage.isdigit() and re.match(r"^\d{4}-\d{2}-\d{2}$", RepairDate) and re.match(r"^\d+\.\d{2}$", Cost)):
            App.get_running_app().show_popup_acknowledge(App.get_running_app().get_translation('bad_data_popup'))
            pass

        try:
            conn = App.get_running_app().conn
            cursor = conn.cursor()
            cursor.execute("UPDATE repairs SET repair_type=%s,description=%s,cost=%s,repair_date=%s,part_number=%s,mileage=%s WHERE id=%s ", (
                    Type, Description, Decimal(Cost), datetime.strptime(RepairDate, "%Y-%m-%d").date(),
                    PartNumber, int(Mileage),self.Repair[0]))
            conn.commit()
            App.get_running_app().show_popup_acknowledge(App.get_running_app().get_translation('change_data_success'))

            self.ids.cost_value.disabled = True
            self.ids.repair_date_value.disabled = True
            self.ids.part_number_value.disabled = True
            self.ids.mileage_value.disabled = True

            self.ids.button_edit.unbind(on_release=self.SaveEditData)
            self.ids.button_edit.bind(on_release=self.EditRepairData)

            self.ids.button_cancel.unbind(on_release=self.CancelEdit)
            self.ids.button_cancel.bind(on_release=self.GetBack)
            self.ids.button_edit.text = App.get_running_app().get_translation('cancel')

        except:
            App.get_running_app().show_popup_acknowledge(App.get_running_app().get_translation('save_error_popup'))

    def CancelEdit(self,*args):
        self.ids.repair_type_value.text = self.Repair[1]
        self.ids.description_value.text = self.Repair[2]
        self.ids.cost_value.text = str(self.Repair[3])
        self.ids.repair_date_value.text = str(self.Repair[4])
        self.ids.part_number_value.text = self.Repair[5]
        self.ids.mileage_value.text = str(self.Repair[7])

        self.ids.cost_value.disabled = True
        self.ids.repair_date_value.disabled = True
        self.ids.part_number_value.disabled = True
        self.ids.mileage_value.disabled = True

        self.ids.button_edit.unbind(on_release=self.SaveEditData)
        self.ids.button_edit.bind(on_release=self.EditRepairData)

        self.ids.button_cancel.unbind(on_release=self.CancelEdit)
        self.ids.button_cancel.bind(on_release=self.GetBack)
        self.ids.button_edit.text = App.get_running_app().get_translation('edit')

    def EditRepairData(self,*args):
        self.ids.cost_value.disabled = False
        self.ids.repair_date_value.disabled = False
        self.ids.part_number_value.disabled = False
        self.ids.mileage_value.disabled = False

        self.ids.button_edit.text = App.get_running_app().get_translation('save')

        self.ids.button_edit.unbind(on_release=self.EditRepairData)
        self.ids.button_edit.bind(on_release=self.SaveEditData)

        self.ids.button_cancel.unbind(on_release=self.GetBack)
        self.ids.button_cancel.bind(on_release=self.CancelEdit)

    def GetBack(self,*args):
        App.get_running_app().sm.current='repairs'

    def DeleteRepair(self):
        App.get_running_app().show_popup_confirm(App.get_running_app().get_translation('confirm_deleting_repair'),self.OnConfirmDelete)

    def OnConfirmDelete(self, result):
        if result:
            try:
                conn = App.get_running_app().conn
                cursor = conn.cursor()
                cursor.execute("DELETE from repairs WHERE id= %s", (self.Repair[0],))
                conn.commit()
                App.get_running_app().sm.current='repairs'
                App.get_running_app().show_popup_acknowledge(
                    App.get_running_app().get_translation('success_deleting_record'))

            except:
                App.get_running_app().show_popup_acknowledge(App.get_running_app().get_translation('error_deleting_car'))

    pass