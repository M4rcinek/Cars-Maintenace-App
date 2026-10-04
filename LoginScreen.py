from kivy.uix.screenmanager import Screen
from kivy.app import App
import bcrypt
from kivy.lang import Builder

Builder.load_file('kv/LoginScreen.kv')

class LoginScreen(Screen):

    def RefreshLabels(self):
        self.ids.logging.text = App.get_running_app().get_translation("logging")
        self.ids.username.hint_text = App.get_running_app().get_translation("username")
        self.ids.password.hint_text = App.get_running_app().get_translation("password")
        self.ids.login.text = App.get_running_app().get_translation("log_in")
        self.ids.close.text = App.get_running_app().get_translation("close")

    def AuthenticateUser(self):

        UserLogin = self.ids.username.text
        UserPassword = self.ids.password.text

        cursor = App.get_running_app().conn.cursor()
        cursor.execute("SELECT * from users WHERE login= %s",(UserLogin,))
        Row = cursor.fetchall()

        if Row:
            if bcrypt.checkpw(UserPassword.encode('utf-8'), Row[0][3].encode('utf-8')):
                App.get_running_app().user=UserLogin

                cursor.execute("SELECT name from roles INNER JOIN users on roles.id=users.role WHERE login= %s", (UserLogin,))
                Row = cursor.fetchall()
                App.get_running_app().role = Row[0][0]

                App.get_running_app().sm.current = 'main'

            else:
                App.get_running_app().show_popup_acknowledge(App.get_running_app().get_translation('user_logon_error'))
        else:
            App.get_running_app().show_popup_acknowledge(App.get_running_app().get_translation('user_logon_error'))

    def ChangeToEN(self):
        App.get_running_app().lang="en"
        App.get_running_app().RefreshLabels()

    def ChangeToPL(self):
        App.get_running_app().lang="pl"
        App.get_running_app().RefreshLabels()

    def on_pre_enter(self, *args):
        self.ids.username.text = ""
        self.ids.password.text = ""
    pass