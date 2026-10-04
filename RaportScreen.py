import csv
import os
from datetime import datetime

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

Builder.load_file('kv/RaportScreen.kv')


class RaportScreen(Screen):

    def RefreshLabels(self):
        self.ids.vehicles.text = App.get_running_app().get_translation("vehicles")
        self.ids.criteria.text = App.get_running_app().get_translation("provide_criteria")
        self.ids.repairs.text = App.get_running_app().get_translation("repairs")
        self.ids.vehicle.text = App.get_running_app().get_translation("choose_vehicle")

        self.ids.make_text.text = App.get_running_app().get_translation("make")
        self.ids.make_value.hint_text = App.get_running_app().get_translation("provide_make")

        self.ids.model_text.text = App.get_running_app().get_translation("model")
        self.ids.model_value.hint_text = App.get_running_app().get_translation("provide_model")

        self.ids.displacement_text.text = App.get_running_app().get_translation("displacement")
        self.ids.displacement_value.hint_text = App.get_running_app().get_translation("provide_displacement")

        self.ids.date_of_purchase_text.text = App.get_running_app().get_translation("date_of_purchase")
        self.ids.date_of_purchase_value.hint_text = App.get_running_app().get_translation("provide_date_of_pur")

        self.ids.fuel_text.text = App.get_running_app().get_translation("fuel_type")
        self.ids.fuel_value.hint_text = App.get_running_app().get_translation("provide_fuel_type")

        self.ids.vin_text.text = App.get_running_app().get_translation("vin")
        self.ids.vin_value.hint_text = App.get_running_app().get_translation("provide_vin")

        self.ids.button_generate.text = App.get_running_app().get_translation("generate")
        self.ids.button_cancel.text = App.get_running_app().get_translation("cancel")

        self.ids.type_text.text = App.get_running_app().get_translation("repair_type")
        self.ids.type_value.hint_text = App.get_running_app().get_translation("provide_type")

        self.ids.cost_text.text = App.get_running_app().get_translation("cost")
        self.ids.cost_value.hint_text = App.get_running_app().get_translation("provide_cost")

        self.ids.mileage_text.text = App.get_running_app().get_translation("mileage")
        self.ids.mileage_value.hint_text = App.get_running_app().get_translation("provide_mileage")

        self.ids.repair_date_text.text = App.get_running_app().get_translation("repair_date")
        self.ids.repair_date_value.hint_text = App.get_running_app().get_translation("provide_date")

        self.ids.part_number_text.text = App.get_running_app().get_translation("part_number")
        self.ids.part_number_value.hint_text = App.get_running_app().get_translation("provide_part_number")

    def on_enter(self, *args):
        self.LoadVehicles()

    def LoadVehicles(self):
        conn = App.get_running_app().conn
        cursor = conn.cursor()

        cursor.execute("""
            SELECT reg_number
            FROM cars
            ORDER BY reg_number
        """)

        vehicles = cursor.fetchall()

        self.ids.vehicle.values = [
            row[0] for row in vehicles
        ]

    def GetBack(self):
        App.get_running_app().sm.current = 'main'

    def AddCondition(self, conditions, values, column, operator, value):
        """
        Adds a SQL condition only if the user entered a value.
        """

        if not value.strip():
            return

        allowed_operators = ["=", "!=", ">", "<", ">=", "<="]

        if operator not in allowed_operators:
            operator = "="

        conditions.append(f"{column} {operator} %s")
        values.append(value.strip())

    def generuj(self):

        # ---------------------------------------
        # CHECK WHICH REPORT USER WANTS
        # ---------------------------------------

        if not self.ids.pojazdy.active and not self.ids.naprawy.active:
            App.get_running_app().show_popup_acknowledge(
                "Select Vehicles or Repairs."
            )
            return

        conn = App.get_running_app().conn
        cursor = conn.cursor()

        # ---------------------------------------
        # VEHICLES REPORT
        # ---------------------------------------

        if self.ids.pojazdy.active:

            query = """
                SELECT
                    reg_number,
                    make,
                    model,
                    displacement,
                    buy_date,
                    fuel_type,
                    VIN
                FROM cars
            """

            conditions = []
            values = []

            # Selected vehicle
            selected_vehicle = self.ids.vehicle.text

            if selected_vehicle != App.get_running_app().get_translation("choose_vehicle"):
                conditions.append("reg_number = %s")
                values.append(selected_vehicle)

            else:
                # Make
                self.AddCondition(
                    conditions,
                    values,
                    "make",
                    self.ids.operator_marka.text,
                    self.ids.make_value.text
                )

                # Model
                self.AddCondition(
                    conditions,
                    values,
                    "model",
                    self.ids.operator_model.text,
                    self.ids.model_value.text
                )

                # Displacement
                if self.ids.displacement_value.text.strip():
                    try:
                        displacement = int(self.ids.displacement_value.text)

                        operator = self.ids.operator_pojemnosc.text

                        if operator not in ["=", "!=", ">", "<", ">=", "<="]:
                            operator = "="

                        conditions.append(
                            f"displacement {operator} %s"
                        )
                        values.append(displacement)

                    except ValueError:
                        App.get_running_app().show_popup_acknowledge(
                            "Displacement must be a number."
                        )
                        return

                # Date of purchase
                self.AddCondition(
                    conditions,
                    values,
                    "buy_date",
                    self.ids.operator_data.text,
                    self.ids.date_of_purchase_value.text
                )

                # Fuel
                self.AddCondition(
                    conditions,
                    values,
                    "fuel_type",
                    self.ids.operator_paliwo.text,
                    self.ids.fuel_value.text
                )

                # VIN
                self.AddCondition(
                    conditions,
                    values,
                    "VIN",
                    self.ids.operator_vin.text,
                    self.ids.vin_value.text
                )

            # Add WHERE
            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            query += " ORDER BY reg_number"

            try:
                cursor.execute(query, tuple(values))
                rows = cursor.fetchall()

                if not rows:
                    App.get_running_app().show_popup_acknowledge(
                        "No vehicles found."
                    )
                    return

                headers = [
                    "Registration number",
                    "Make",
                    "Model",
                    "Displacement",
                    "Date of purchase",
                    "Fuel type",
                    "VIN"
                ]

                self.SaveCSV(
                    "vehicles",
                    headers,
                    rows
                )

            except Exception as e:
                print(e)

                App.get_running_app().show_popup_acknowledge(
                    "Error generating report."
                )

        # ---------------------------------------
        # REPAIRS REPORT
        # ---------------------------------------

        elif self.ids.naprawy.active:

            query = """
                SELECT
                    reg_number,
                    repair_type,
                    cost,
                    mileage,
                    repair_date,
                    part_number,
                    description
                FROM repairs
            """

            conditions = []
            values = []

            # Selected vehicle
            selected_vehicle = self.ids.vehicle.text

            if selected_vehicle != App.get_running_app().get_translation("choose_vehicle"):
                conditions.append("reg_number = %s")
                values.append(selected_vehicle)

            else:

                # Repair type
                self.AddCondition(
                    conditions,
                    values,
                    "repair_type",
                    self.ids.operator_rodzaj.text,
                    self.ids.type_value.text
                )

                # Cost
                if self.ids.cost_value.text.strip():
                    try:
                        cost = float(self.ids.cost_value.text.replace(",", "."))

                        operator = self.ids.operator_koszt.text

                        if operator not in ["=", "!=", ">", "<", ">=", "<="]:
                            operator = "="

                        conditions.append(
                            f"cost {operator} %s"
                        )
                        values.append(cost)

                    except ValueError:
                        App.get_running_app().show_popup_acknowledge(
                            "Cost must be a number."
                        )
                        return

                # Mileage
                if self.ids.mileage_value.text.strip():
                    try:
                        mileage = int(self.ids.mileage_value.text)

                        operator = self.ids.operator_przebieg.text

                        if operator not in ["=", "!=", ">", "<", ">=", "<="]:
                            operator = "="

                        conditions.append(
                            f"mileage {operator} %s"
                        )
                        values.append(mileage)

                    except ValueError:
                        App.get_running_app().show_popup_acknowledge(
                            "Mileage must be a number."
                        )
                        return

                # Repair date
                self.AddCondition(
                    conditions,
                    values,
                    "repair_date",
                    self.ids.operator_data.text,
                    self.ids.repair_date_value.text
                )

                # Part number
                self.AddCondition(
                    conditions,
                    values,
                    "part_number",
                    self.ids.operator_kod.text,
                    self.ids.part_number_value.text
                )

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            query += " ORDER BY repair_date"

            try:
                cursor.execute(query, tuple(values))
                rows = cursor.fetchall()

                if not rows:
                    App.get_running_app().show_popup_acknowledge(
                        "No repairs found."
                    )
                    return

                headers = [
                    "Registration number",
                    "Repair type",
                    "Cost",
                    "Mileage",
                    "Repair date",
                    "Part number",
                    "Description"
                ]

                self.SaveCSV(
                    "repairs",
                    headers,
                    rows
                )

            except Exception as e:
                print(e)

                App.get_running_app().show_popup_acknowledge(
                    "Error generating report."
                )

    def SaveCSV(self, report_type, headers, rows):

        reports_directory = "reports"

        if not os.path.exists(reports_directory):
            os.makedirs(reports_directory)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        filename = f"{report_type}_{timestamp}.csv"

        filepath = os.path.join(
            reports_directory,
            filename
        )

        with open(
            filepath,
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            writer = csv.writer(
                file,
                delimiter=";",
                quoting=csv.QUOTE_MINIMAL
            )

            writer.writerow(headers)

            for row in rows:
                writer.writerow(row)

        App.get_running_app().show_popup_acknowledge(
            f"Report generated:\n{filepath}"
        )

    pass