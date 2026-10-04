from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivy.app import App
from LoginScreen import LoginScreen
from MainScreen import MainScreen
from CarAddScreen import CarAddScreen
from UserManagementScreen import UserManagementScreen
from RaportScreen import RaportScreen
from CustomPopup import CustomPopup
from CarDetailsScreen import CarDetailsScreen
from RepairsScreen import RepairsScreen
from SettingsScreen import SettingsScreen
from RepairAddScreen import RepairAddScreen
from RepairDetailsScreen import RepairDetailsScreen
import mysql.connector
import configparser
import os

from kivy.properties import ListProperty
import configparser

import configparser
import os
import mysql.connector

from kivy.app import App
from kivy.properties import ListProperty
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window


class AplikacjaApp(App):

    accent_color = ListProperty([0.2, 1, 0.45, 1])

    def build(self):

        self.settings_file = "settings.ini"

        self.config = configparser.ConfigParser()

        if not os.path.exists(self.settings_file):
            self.CreateDefaultSettings()

        self.config.read(
            self.settings_file,
            encoding="utf-8"
        )

        # LANGUAGE

        self.lang = self.config.get(
            "app",
            "language",
            fallback="en"
        )

        if self.lang not in ["en", "pl"]:
            self.lang = "en"


        color = self.config.get(
            "app",
            "accent_color",
            fallback="33CC66"
        )

        self.accent_color = self.HexToRGBA(color)
        self.ConnectDatabase()

        self.user = ''
        self.role = ''

        self.sm = ScreenManager()

        self.sm.add_widget(LoginScreen(name="login"))
        self.sm.add_widget(MainScreen(name="main"))
        self.sm.add_widget(CarAddScreen(name="caradd"))
        self.sm.add_widget(UserManagementScreen(name="usermanagement"))
        self.sm.add_widget(RaportScreen(name="raport"))
        self.sm.add_widget(CarDetailsScreen(name="cardetails"))
        self.sm.add_widget(RepairsScreen(name="repairs"))
        self.sm.add_widget(SettingsScreen(name="settings"))
        self.sm.add_widget(RepairAddScreen(name="repairadd"))
        self.sm.add_widget(RepairDetailsScreen(name="repairdetails"))

        Window.borderless = True
        Window.clearcolor = (0, 0, 0, 1)

        return self.sm

    def HexToRGBA(self, color):

        color = color.replace("#", "")

        if len(color) != 6:
            return [0.2, 1, 0.45, 1]

        r = int(color[0:2], 16) / 255
        g = int(color[2:4], 16) / 255
        b = int(color[4:6], 16) / 255

        return [r, g, b, 1]

    def RGBAToHex(self, color):

        r = int(color[0] * 255)
        g = int(color[1] * 255)
        b = int(color[2] * 255)

        return f"{r:02X}{g:02X}{b:02X}"

    def ConnectDatabase(self):

        db_config = self.config["database"]

        self.conn = mysql.connector.connect(
            host=db_config["host"],
            port=int(db_config["port"]),
            user=db_config["user"],
            password=db_config["password"],
            database=db_config["database"]
        )

    def get_translation(self, key):

        from Translations import translations

        return translations[self.lang].get(
            key,
            key
        )

    def show_popup_acknowledge(self, text):

        popup = CustomPopup()

        popup.ids.custom_label.text = text
        popup.ids.yes.text = "OK"
        popup.ids.no.text = self.get_translation("close")

        popup.ids.yes.on_release = popup.dismiss
        popup.ids.no.on_release = popup.dismiss

        popup.open()

    def show_popup_confirm(self, text, callback):

        popup = CustomPopup()

        popup.ids.custom_label.text = text
        popup.ids.yes.text = self.get_translation("yes")
        popup.ids.no.text = self.get_translation("no")

        popup.callback = callback

        popup.open()

    def RefreshLabels(self):

        for screen in self.sm.screens:

            if hasattr(screen, "RefreshLabels"):
                screen.RefreshLabels()

    def SaveSettings(self):
        with open(self.settings_file, "w", encoding="utf-8") as file:
            self.config.write(file)

if __name__ == '__main__':
    AplikacjaApp().run()