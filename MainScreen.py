from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.lang import Builder
from CustomTitleBar import CustomTitleBar
from CarPanel import CarPanel

Builder.load_file('kv/MainScreen.kv')

class MainScreen(Screen):
    form_window = None

    def RefreshLabels(self):
        self.ids.input.hint_text = App.get_running_app().get_translation("search")

    def on_enter(self, *args):
        title_bar = self.ids.custom_title_bar
        title_bar.ids.logged.text = App.get_running_app().get_translation('logged_as') + App.get_running_app().user +" (" +App.get_running_app().role + ")"

    def OpenCarAddWindow(self):
        App.get_running_app().sm.current = 'caradd'

    def OpenRaportWindow(self):
        App.get_running_app().sm.current = 'raport'

    def OpenUserManagementWindow(self):
        App.get_running_app().sm.current = 'usermanagement'

    def OpenSettingsWindow(self):
        App.get_running_app().sm.current = 'settings'

    def Logout(self):
        App.get_running_app().sm.current = 'login'

    def ShowDropdown(self, MainButton):
        dropdown = DropDown(auto_width = False)
        dropdown.width = 300

        # Przycisk 1 – przejdź do ekranu "ustawienia"
        Btn1 = Button(text=App.get_running_app().get_translation("add_car"), size_hint_y=None, height=44, size_hint_x=None,width=300, background_color=( 0, 0, 0, 1), color=App.get_running_app().accent_color)
        Btn1.bind(on_release=lambda *a: (dropdown.dismiss(), self.OpenCarAddWindow()))
        dropdown.add_widget(Btn1)

        # Przycisk 2 – przejdź do ekranu "o aplikacji"
        Btn2 = Button(text=App.get_running_app().get_translation("generate_raport"), size_hint_y=None, height=44, size_hint_x=None,width=300, background_color=( 0, 0, 0, 1), color= App.get_running_app().accent_color)
        Btn2.bind(on_release=lambda *a: (dropdown.dismiss(), self.OpenRaportWindow()))
        dropdown.add_widget(Btn2)

        # Przycisk 3 – zamknij aplikację
        Btn3 = Button(text=App.get_running_app().get_translation("manage_users"), size_hint_y=None, height=44,size_hint_x=None,width=300, background_color=( 0, 0, 0, 1), color= App.get_running_app().accent_color)
        Btn3.bind(on_release=lambda *a: (dropdown.dismiss(), self.OpenUserManagementWindow()))
        dropdown.add_widget(Btn3)

        # Przycisk 3 – zamknij aplikację
        Btn4 = Button(text=App.get_running_app().get_translation("logout"), size_hint_y=None, height=44, size_hint_x=None, width=300, background_color=( 0, 0, 0, 1), color= App.get_running_app().accent_color)
        Btn4.bind(on_release=lambda *a: (dropdown.dismiss(), self.Logout()))
        dropdown.add_widget(Btn4)

        dropdown.open(MainButton)
    pass