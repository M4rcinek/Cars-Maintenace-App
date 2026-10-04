from kivy.app import App
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
import bcrypt

Builder.load_file('kv/UserManagementScreen.kv')

class UserManagementScreen(Screen):
    usernames=ListProperty()
    def RefreshLabels(self):
        self.ids.button_add_user.text = App.get_running_app().get_translation("add_user")
        self.ids.button_cancel.text = App.get_running_app().get_translation("cancel")
        self.ids.button_delete_user.text = App.get_running_app().get_translation("delete_user")
        self.ids.button_change_pass.text = App.get_running_app().get_translation("change_pass")
        self.ids.button_change_permissions.text = App.get_running_app().get_translation("change_permissions")
        self.ids.options_text.text = App.get_running_app().get_translation("options")
        self.ids.choose_user_text.text = App.get_running_app().get_translation("choose_user")
        self.ids.user_management_text.text = App.get_running_app().get_translation("user_management")

    def on_enter(self, *args):
        conn = App.get_running_app().conn
        cursor = conn.cursor()
        cursor.execute("Select * from users;")
        self.records = cursor.fetchall()
        self.usernames = [r[1] for r in self.records]

    def GetBack(self):
        App.get_running_app().sm.current = 'main'

    def ChangePassword(self):
        if self.ids.username_list.text == "":
            App.get_running_app().show_popup_acknowledge(App.get_running_app().get_translation('no_user_error'))

        else:
            User = self.ids.username_list.text
            popup = Popup(title=App.get_running_app().get_translation('provide_and_confirm_pass'), size_hint=(0.6, 0.6),
                              background_color=(0, 0, 0, 1), title_color=(0.725, 1, 0.3, 0.7))
            PopupLayout = BoxLayout(orientation='vertical', spacing=10, padding=10)

            Password1 = TextInput(
                    size_hint=(1, 0.3),
                    password=True
            )

            Password2 = TextInput(
                    size_hint=(1, 0.3),
                    password=True
                )

            def ConfirmChange(event):
                if (Password1.text==Password2.text):
                    NewPassword = Password1.text.encode('utf-8')
                    HashedNewPassword = bcrypt.hashpw(NewPassword, bcrypt.gensalt())
                    try:
                        conn = App.get_running_app().conn
                        cursor = conn.cursor()
                        cursor.execute("UPDATE users SET password =%s where login=%s", (HashedNewPassword,str(User)))
                        conn.commit()
                        App.get_running_app().show_popup_acknowledge(App.get_running_app().get_translation('changing_pass_confirm'))
                    except:
                        App.get_running_app().show_popup_acknowledge(App.get_running_app().get_translation('error_changing_pass'))
                else:
                    App.get_running_app().show_popup_acknowledge(App.get_running_app().get_translation('pass_dont_match'))

            OkButton = Button(
                text=App.get_running_app().get_translation('change_pass'),
                size_hint=(1, 0.1),
                on_press=ConfirmChange,
                background_color=(0, 0, 0, 0.8),
                color=(0.725, 1, 0.3, 0.7),
                on_release = popup.dismiss
            )

            PopupLayout.add_widget(Password1)
            PopupLayout.add_widget(Password2)
            PopupLayout.add_widget(OkButton)

            popup.content = PopupLayout

            popup.open()


    def AddUser(self):
        popup = Popup(title=App.get_running_app().get_translation('add_user'), size_hint=(0.6, 0.6),
                      background_color=(0, 0, 0, 1), title_color=(0.725, 1, 0.3, 0.7))
        PopupLayout  = BoxLayout(orientation='vertical', spacing=10, padding=10)


        Login = TextInput(
            size_hint=(1,0.3),
            hint_text=App.get_running_app().get_translation('insert_login'),
        )

        Password1 = TextInput(
            size_hint=(1,0.3),
            hint_text=App.get_running_app().get_translation('insert_password'),
            password= True
        )

        Password2 = TextInput(
            size_hint=(1,0.3),
            hint_text=App.get_running_app().get_translation('confirm_password'),
            password= True
        )

        Role = Spinner(
            values = ["Administrator","Operator", "Serwisant", "Przegladacz"],
            size_hint=(1,0.3),
            text=App.get_running_app().get_translation('choose_role'),
        )
        def AddConfirm(event):
            if (Password1.text == Password2.text):
                NewPassword = Password1.text.encode('utf-8')
                HashedNewPassword = bcrypt.hashpw(NewPassword, bcrypt.gensalt())
                try:
                    conn = App.get_running_app().conn
                    cursor = conn.cursor()
                    cursor.execute("Select id from roles where name=%s", (str(Role.text),))
                    RoleId = cursor.fetchall()
                    cursor.execute("Insert into users  (login, role, password) values(%s,%s,%s)",
                                   (Login.text, int(RoleId[0][0]), HashedNewPassword))
                    conn.commit()
                    App.get_running_app().show_popup_acknowledge(App.get_running_app().get_translation('adding_user_confirm'))
                except:
                    App.get_running_app().show_popup_acknowledge(App.get_running_app().get_translation('error_adding_user'))
            else:
                App.get_running_app().show_popup_acknowledge(App.get_running_app().get_translation('pass_dont_match'))

        OkButton = Button(
            text=App.get_running_app().get_translation('add_user'),
            size_hint=(1, 0.1),
            background_color=(0, 0, 0, 1),
            color=(0.725, 1, 0.3, 0.7),
            on_press = AddConfirm,
            on_release = popup.dismiss
        )

        PopupLayout.add_widget(Login)
        PopupLayout.add_widget(Password1)
        PopupLayout.add_widget(Password2)
        PopupLayout.add_widget(Role)
        PopupLayout.add_widget(OkButton)

        popup.content = PopupLayout

        popup.open()

    def DeleteUser(self):
        if self.ids.username_list.text == "":
            App.get_running_app().show_popup_acknowledge(App.get_running_app().get_translation('no_user_error'))
        else:
            App.get_running_app().show_popup_confirm(App.get_running_app().get_translation('user_delete_confirm'), self.OnConfirmDelete)

    def OnConfirmDelete(self, result):
        if result:
            try:
                conn = App.get_running_app().conn
                cursor = conn.cursor()
                cursor.execute("DELETE from users WHERE login= %s", (self.ids.username_list.text,))
                conn.commit()
                App.get_running_app().show_popup_acknowledge(
                    App.get_running_app().get_translation('user_deleting_success'))

            except:
                App.get_running_app().show_popup_acknowledge(App.get_running_app().get_translation('error_deleting_user'))

    def ChangePermissions(self):
        if self.ids.username_list.text == "":
            App.get_running_app().show_popup_acknowledge(App.get_running_app().get_translation('no_user_error'))

        else:
            User = self.ids.username_list.text
            popup = Popup(title=App.get_running_app().get_translation('choose_new_role'), size_hint=(0.6, 0.4),
                          background_color=(0, 0, 0, 1), title_color=(0.725, 1, 0.3, 0.7))
            PopupLayout = BoxLayout(orientation='vertical', spacing=10, padding=10)

            Role = Spinner(
                values=["Administrator", "Operator", "Serwisant", "Przegladacz"],
                size_hint=(1, 0.3),
                text=App.get_running_app().get_translation('choose_role'),
            )

            def ChangeConfirm(event):
                try:
                    conn = App.get_running_app().conn
                    cursor = conn.cursor()
                    cursor.execute("Select id from roles where name=%s", (str(Role.text),))
                    RoleId = cursor.fetchall()
                    cursor.execute("Update users Set role=%s where login=%s", (int(RoleId[0][0]),User))
                    conn.commit()
                    App.get_running_app().show_popup_acknowledge(
                        App.get_running_app().get_translation('permission_change_success'))
                except:
                    App.get_running_app().show_popup_acknowledge(
                        App.get_running_app().get_translation('error_changing_permissions'))

            OkButton = Button(
                text=App.get_running_app().get_translation('change_permissions'),
                size_hint=(1, 0.1),
                on_press = ChangeConfirm,
                background_color=(0, 0, 0, 1),
                color=(0.725, 1, 0.3, 0.7),
                on_release = popup.dismiss
            )

            PopupLayout.add_widget(Role)
            PopupLayout.add_widget(OkButton)

            popup.content = PopupLayout

            popup.open()
    pass