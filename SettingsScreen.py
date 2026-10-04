import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

Builder.load_file('kv/SettingsScreen.kv')


class SettingsScreen(Screen):

    def on_enter(self):
        self.LoadSettingsToScreen()

    def LoadSettingsToScreen(self):

        app = App.get_running_app()

        # LANGUAGE
        self.ids.language_input.text = app.lang

        # DATABASE
        db_config = app.config["database"]

        self.ids.database_input.text = db_config.get("host", "127.0.0.1")
        self.ids.port_input.text = db_config.get("port", "3306")
        self.ids.user_input.text = db_config.get("user", "sql")
        self.ids.password_input.text = db_config.get("password", "sql")
        self.ids.database_name_input.text = db_config.get(
            "database",
            "car_maintenance"
        )

        # COLOR
        self.ids.color_picker.color = app.accent_color

    def GetBack(self):
        App.get_running_app().sm.current = 'main'

    def RefreshLabels(self):

        app = App.get_running_app()

        self.ids.settings_title.text = app.get_translation("settings")
        self.ids.interface.text = app.get_translation("interface_color")
        self.ids.language.text = app.get_translation("language")
        self.ids.database.text = app.get_translation("database")

        self.ids.host_label.text = app.get_translation("database_host")
        self.ids.port_label.text = app.get_translation("database_port")
        self.ids.user_label.text = app.get_translation("database_user")
        self.ids.password_label.text = app.get_translation("database_password")
        self.ids.database_name_label.text = app.get_translation("database_name")

        self.ids.button_scan.text = app.get_translation("scan")
        self.ids.button_save.text = app.get_translation("save")
        self.ids.button_cancel.text = app.get_translation("cancel")

    def ChangeColor(self, color_picker, color):

        App.get_running_app().accent_color = color

    def ChangeLanguage(self, language):

        app = App.get_running_app()

        app.lang = language

        # Od razu odświeżamy napisy całej aplikacji
        if app.sm:
            app.RefreshLabels()

    def SaveSettings(self):
        app = App.get_running_app()

        app.lang = self.ids.language_input.text

        app.config.set(
            "app",
            "language",
            app.lang
        )

        app.accent_color = self.ids.color_picker.color

        app.config.set(
            "app",
            "accent_color",
            app.RGBAToHex(app.accent_color)
        )

        app.config.set(
            "database",
            "host",
            self.ids.database_input.text.strip()
        )

        app.config.set(
            "database",
            "port",
            self.ids.port_input.text.strip()
        )

        app.config.set(
            "database",
            "user",
            self.ids.user_input.text.strip()
        )

        app.config.set(
            "database",
            "password",
            self.ids.password_input.text
        )

        app.config.set(
            "database",
            "database",
            self.ids.database_name_input.text.strip()
        )

        # ZAPISZ USTAWIENIA NIEZALEŻNIE OD BAZY
        app.SaveSettings()

        # Spróbuj połączyć się z nową konfiguracją bazy
        try:

            if app.conn:
                app.conn.close()

            app.ConnectDatabase()

        except Exception as e:

            print("Database connection error:", e)

            app.RefreshLabels()

            app.show_popup_acknowledge(
                app.get_translation("database_connection_error")
            )

            return

        app.RefreshLabels()

        app.show_popup_acknowledge(
            app.get_translation("settings_saved")
        )

    def FindDatabases(self):

        self.ids.button_scan.disabled = True
        self.ids.button_scan.text = "Scanning..."

        # Skanowanie w tle, żeby GUI się nie zawiesiło
        from threading import Thread

        Thread(
            target=self.ScanNetwork,
            daemon=True
        ).start()

    def ScanNetwork(self):

        found = []

        try:

            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)

            network = ipaddress.ip_network(
                local_ip + "/24",
                strict=False
            )

            hosts = [str(ip) for ip in network.hosts()]

            def check_host(ip):

                port = 3306

                sock = socket.socket(
                    socket.AF_INET,
                    socket.SOCK_STREAM
                )

                sock.settimeout(0.2)

                try:

                    result = sock.connect_ex(
                        (ip, port)
                    )

                    if result == 0:
                        return ip

                except Exception:
                    pass

                finally:
                    sock.close()

                return None

            with ThreadPoolExecutor(max_workers=50) as executor:

                results = executor.map(
                    check_host,
                    hosts
                )

            for result in results:

                if result:
                    found.append(result)

        except Exception as e:

            print("Network scan error:", e)

        Clock.schedule_once(
            lambda dt: self.ScanFinished(found)
        )

    def ScanFinished(self, found):

        self.ids.button_scan.disabled = False
        self.ids.button_scan.text = App.get_running_app().get_translation(
            "scan"
        )

        if found:

            self.ids.database_input.values = found

            # Jeśli aktualnego hosta nie ma na liście,
            # wybieramy pierwszy znaleziony.
            if self.ids.database_input.text not in found:
                self.ids.database_input.text = found[0]

            print("Found MySQL servers:")

            for host in found:
                print(host)

        else:

            self.ids.database_input.values = []

            App.get_running_app().show_popup_acknowledge(
                "No MySQL servers found."
            )
pass