import re
from datetime import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.screenmanager import Screen

Builder.load_file('kv/CarDetailsScreen.kv')

class CarDetailsScreen(Screen):

    car = ListProperty()

    def RefreshLabels(self):
        self.ids.button_cancel.text = App.get_running_app().get_translation("cancel")
        self.ids.button_edit.text = App.get_running_app().get_translation("edit")
        self.ids.button_repairs.text = App.get_running_app().get_translation("repairs")
        self.ids.button_car_delete.text = App.get_running_app().get_translation("delete_car")
        self.ids.reg_number_text.text = App.get_running_app().get_translation("reg_number")
        self.ids.make_text.text = App.get_running_app().get_translation("make")
        self.ids.model_text.text = App.get_running_app().get_translation("model")
        self.ids.vin_text.text = App.get_running_app().get_translation("vin")
        self.ids.displacement_text.text = App.get_running_app().get_translation("displacement")
        self.ids.date_of_pur_text.text = App.get_running_app().get_translation("date_of_purchase")
        self.ids.fuel_type_text.text = App.get_running_app().get_translation("fuel_type")

    def on_enter(self, *args):
        conn = App.get_running_app().conn
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cars WHERE reg_number=%s;",
                       (self.car[0],))
        cars = cursor.fetchall()

        self.car = cars[0]

        self.ids.car_photo.source = self.car[7]

        self.ids.reg_number_value.text = self.car[0]
        self.ids.mark_value.text = self.car[1]
        self.ids.model_value.text = self.car[2]
        self.ids.fuel_type_value.text = self.car[5]
        self.ids.vin_value.text = self.car[6]
        self.ids.displacement_value.text = str(self.car[3])
        self.ids.year_value.text = str(self.car[4])

        self.ids.button_edit.bind(on_release=self.EditCarData)
        self.ids.button_cancel.bind(on_release=self.GetBack)

        screen = App.get_running_app().sm.get_screen('repairs')
        screen.reg_number = self.car[0]

    def GetBack(self, *args):
        App.get_running_app().sm.current = 'main'

    def ShowRepairs(self):
        App.get_running_app().sm.current = 'repairs'

    def SaveEditData(self,*args):
        RegNumber = self.ids.reg_number_value.text
        Make = self.ids.mark_value.text
        Model = self.ids.model_value.text
        Vin = self.ids.vin_value.text
        Displacement = self.ids.displacement_value.text
        DateOfPurchase = self.ids.year_value.text
        Fuel = self.ids.fuel_type_value.text

        if not (len(RegNumber) < 9 and Displacement.isdigit() and re.match(r"^\d{4}-\d{2}-\d{2}$", DateOfPurchase)):
            App.get_running_app().show_popup_acknowledge(App.get_running_app().get_translation('bad_data_popup'))
            pass

        try:
            conn = App.get_running_app().conn
            cursor = conn.cursor()
            cursor.execute("UPDATE cars SET reg_number=%s,make=%s,model=%s,displacement=%s,buy_date=%s,fuel_type=%s,VIN=%s WHERE reg_number=%s;",
                           (
                           RegNumber.upper(), Make.upper(), Model.upper(), int(Displacement),
                           datetime.strptime(DateOfPurchase, "%Y-%m-%d").date(),
                           Fuel.upper(), Vin.upper(), self.car[0]))
            App.get_running_app().show_popup_acknowledge(App.get_running_app().get_translation('change_data_success'))

            self.ids.reg_number_value.disabled = True
            self.ids.mark_value.disabled = True
            self.ids.model_value.disabled = True
            self.ids.fuel_type_value.disabled = True
            self.ids.vin_value.disabled = True
            self.ids.displacement_value.disabled = True
            self.ids.year_value.disabled = True

            self.ids.button_edit.unbind(on_release=self.SaveEditData)
            self.ids.button_edit.bind(on_release=self.EditCarData)

            self.ids.button_cancel.unbind(on_release=self.CancelEdit)
            self.ids.button_cancel.bind(on_release=self.GetBack)
            self.ids.button_edit.text = App.get_running_app().get_translation('cancel')

        except:
            App.get_running_app().show_popup_acknowledge(App.get_running_app().get_translation('save_error_popup'))

    def CancelEdit(self, *args):
        self.ids.reg_number_value.disabled = True
        self.ids.mark_value.disabled = True
        self.ids.model_value.disabled = True
        self.ids.fuel_type_value.disabled = True
        self.ids.vin_value.disabled = True
        self.ids.displacement_value.disabled = True
        self.ids.year_value.disabled = True

        self.ids.reg_number_value.text = self.car[0]
        self.ids.mark_value.text = self.car[1]
        self.ids.model_value.text = self.car[2]
        self.ids.fuel_type_value.text = self.car[5]
        self.ids.vin_value.text = self.car[6]
        self.ids.displacement_value.text = str(self.car[3])
        self.ids.year_value.text = str(self.car[4])

        self.ids.button_edit.unbind(on_release=self.SaveEditData)
        self.ids.button_edit.bind(on_release=self.EditCarData)

        self.ids.button_cancel.unbind(on_release=self.CancelEdit)
        self.ids.button_cancel.bind(on_release=self.GetBack)
        self.ids.button_edit.text = App.get_running_app().get_translation('edit')

    def EditCarData(self, *args):
        self.ids.reg_number_value.disabled = False
        self.ids.mark_value.disabled = False
        self.ids.model_value.disabled = False
        self.ids.fuel_type_value.disabled = False
        self.ids.vin_value.disabled = False
        self.ids.displacement_value.disabled = False
        self.ids.year_value.disabled = False

        self.ids.button_edit.text = App.get_running_app().get_translation('save')

        self.ids.button_edit.unbind(on_release=self.EditCarData)
        self.ids.button_edit.bind(on_release=self.SaveEditData)

        self.ids.button_cancel.unbind(on_release=self.GetBack)
        self.ids.button_cancel.bind(on_release=self.CancelEdit)

    def DeleteCar(self):
        App.get_running_app().show_popup_confirm(App.get_running_app().get_translation('confirm_deleting_car'),self.OnConfirmDelete)

    def OnConfirmDelete(self, result):
        if result:
            try:
                conn = App.get_running_app().conn
                cursor = conn.cursor()
                cursor.execute("DELETE from cars WHERE reg_number= %s", (self.car[0],))
                conn.commit()
                App.get_running_app().sm.current='main'
                App.get_running_app().sm.get_screen('main').ids.car_panel.LoadCars()
                App.get_running_app().show_popup_acknowledge(
                    App.get_running_app().get_translation('success_deleting_record'))

            except:
                App.get_running_app().show_popup_acknowledge(App.get_running_app().get_translation('error_deleting_car'))

    pass