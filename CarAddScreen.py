import re
from datetime import datetime

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.filechooser import FileChooserListView
import os
import shutil

Builder.load_file('kv/CarAddScreen.kv')

class CarAddScreen(Screen):

    def RefreshLabels(self):
        self.ids.reg_number_text.text = App.get_running_app().get_translation("reg_number")
        self.ids.make_text.text = App.get_running_app().get_translation("make")
        self.ids.model_text.text = App.get_running_app().get_translation("model")
        self.ids.vin_text.text = App.get_running_app().get_translation("vin")
        self.ids.displacement_text.text = App.get_running_app().get_translation("displacement")
        self.ids.date_of_purchase_text.text = App.get_running_app().get_translation("date_of_purchase")
        self.ids.fuel_text.text = App.get_running_app().get_translation("fuel_type")
        self.ids.save_button.text = App.get_running_app().get_translation("save")
        self.ids.back_button.text = App.get_running_app().get_translation("cancel")
        self.ids.photo_text.text = App.get_running_app().get_translation("photo")
        self.ids.filechooser.text = App.get_running_app().get_translation("add_photo")

    def on_pre_leave(self, *args):
        self.ids.reg_number.text = ""
        self.ids.make.text = ""
        self.ids.model.text = ""
        self.ids.vin.text = ""
        self.ids.displacement.text = ""
        self.ids.date_of_purchase.text = ""
        self.ids.fuel.text = ""

    def CancelAndGoBack(self):
        App.get_running_app().sm.current = 'main'

    def SaveAndAdd(self):
        RegNumber = self.ids.reg_number.text
        Make = self.ids.make.text
        Model = self.ids.model.text
        Vin = self.ids.vin.text
        Displacement = self.ids.displacement.text
        DateOfPurchase = self.ids.date_of_purchase.text
        Fuel = self.ids.fuel.text

        photo_path = None

        if hasattr(self, "selected_photo") and self.selected_photo:
            os.makedirs("media", exist_ok=True)

            extension = os.path.splitext(self.selected_photo)[1]
            filename = RegNumber.upper() + extension

            destination = os.path.join("media", filename)

            shutil.copy2(self.selected_photo, destination)

            photo_path = destination
        if not (len(RegNumber) < 9 and Displacement.isdigit() and re.match(r"^\d{4}-\d{2}-\d{2}$", DateOfPurchase)):
            App.get_running_app().show_popup_acknowledge(App.get_running_app().get_translation('bad_data_popup'))
            pass

        try:
            conn = App.get_running_app().conn
            cursor = conn.cursor()
            cursor.execute("INSERT INTO cars (reg_number,make,model,displacement,buy_date,fuel_type,VIN,photo) "
                "values(%s,%s,%s,%s,%s,%s,%s,%s)",(RegNumber.upper(), Make.upper(), Model.upper(), int(Displacement), datetime.strptime(DateOfPurchase, "%Y-%m-%d").date(),
                Fuel.upper(), Vin.upper(),photo_path))
            conn.commit()
            App.get_running_app().sm.get_screen('main').ids.car_panel.LoadCars()
            App.get_running_app().show_popup_acknowledge(App.get_running_app().get_translation('success_adding_record'))

        except:
            App.get_running_app().show_popup_acknowledge(App.get_running_app().get_translation('save_error_popup'))

    def AddPhoto(self):
        chooser = FileChooserListView(
            filters=["*.png", "*.jpg", "*.jpeg"]
        )

        popup = Popup(
            title="Wybierz zdjęcie",
            size_hint=(0.9, 0.9)
        )

        select_button = Button(
            text="Wybierz",
            size_hint_y=None,
            height=50
        )

        def SelectPhoto(instance):
            if chooser.selection:
                self.selected_photo = chooser.selection[0]
                popup.dismiss()

        select_button.bind(on_release=SelectPhoto)

        layout = BoxLayout(
            orientation="vertical"
        )

        layout.add_widget(chooser)
        layout.add_widget(select_button)

        popup.content = layout
        popup.open()

    pass