# Cars-Maintenance-App

Desktop application for managing vehicles, repairs and user accounts.

The application was developed in **Python and Kivy** and uses **MySQL** as its database. It allows users to manage their vehicles, record performed repairs, generate reports and manage user accounts with different permissions.

The project was originally developed as an **academic project as part of my engineering degree** and was later extended with additional functionality and improvements.

## Features

* Vehicle management — adding, editing and deleting vehicles
* Repair management — recording repairs and associated costs
* User authentication
* Role-based permissions
* Vehicle photo management
* CSV report generation
* Polish and English language support
* Configurable UI accent color
* MySQL connection configuration
* Local network scanning for available MySQL servers
* Configuration stored in an external `.ini` file
* Docker-based MySQL database

## Technologies

* **Python**
* **Kivy**
* **MySQL**
* **SQL**
* **Docker**
* **ConfigParser**
* **CSV**
* **Git**

## Application Structure

The application is divided into Python modules responsible for application logic and Kivy `.kv` files responsible for the user interface.

Most screens consist of a pair of files:

```text
RepairAddScreen.py
RepairAddScreen.kv
```

The Python file contains the screen logic, while the `.kv` file defines its user interface.

The project also contains reusable components such as `CustomTitleBar` and `CustomPopup`.

A simplified project structure:

```text
CarMaintenanceApp/
│
├── kv/
│   ├── MainScreen.kv
│   ├── CarAddScreen.kv
│   ├── CarDetailsScreen.kv
│   ├── RepairAddScreen.kv
│   ├── RepairDetailsScreen.kv
│   ├── RepairsScreen.kv
│   ├── SettingsScreen.kv
│   └── ...
│
├── media/
│   ├── Daewoo_Matiz.jpg/
│   └── ...
│
│
├── MainScreen.py
├── CarAddScreen.py
├── CarDetailsScreen.py
├── RepairAddScreen.py
├── RepairDetailsScreen.py
├── RepairsScreen.py
├── SettingsScreen.py
├── Translations.py
├── CustomPopup.py
├── CustomTitleBar.py
├── main.py
├── car_maintenance.sql
└── settings.ini
```

## Database

MySQL is used as the application's relational database. It is in my case run as a Docker container

The main entities include:

* `cars` — vehicle information
* `repairs` — repair history and costs
* `users` — application users
* `roles` — user permissions

The database structure is provided as an SQL file that can be used to create the required database.

## Configuration

Application settings are stored in an external `settings.ini` file.

The configuration contains:

```ini
[app]
language = en
accent_color = 33CC66

[database]
host = 127.0.0.1
port = 3306
user = sql
password = sql
database = car_maintenance
```

`settings.ini` file is provided as a template, that is why it contains passwords as a text etc.

This allows the application to be configured without modifying the source code.

## Local Network Database Discovery

The application includes a small network discovery feature used to find MySQL servers available on the local network.

When the user starts a scan, the application:

1. Determines the local IPv4 network.
2. Generates available host addresses.
3. Checks whether port `3306` is accessible.
4. Performs the checks concurrently using `ThreadPoolExecutor`.
5. Displays discovered hosts in the database configuration screen.

This functionality was implemented to simplify database configuration when the MySQL server is running on another machine in the local network.

## User Management

The application includes authentication and role-based access control.

Users can be managed from the application interface, including:

* Creating users
* Changing passwords
* Changing roles
* Deleting users

Passwords are stored using **bcrypt hashing** rather than plain text.

Roles describe what a particular member can do like Only check the repairs/cars, Check and add repairs/cars, have permission to everything (admin) 

## Reporting

The application can generate CSV reports based on selected criteria.

Reports can contain information about:

* Vehicles
* Repairs
* Repair costs
* Selected vehicles
* Other user-defined filters

## Internationalization

The application supports two languages:

* English
* Polish

Translations are separated from the application logic and stored in `Translations.py`.

This allows UI text to be changed without modifying the individual screens.

## What I Learned

During development, I worked with:

* Building a desktop application using Python and Kivy
* Designing and querying a relational MySQL database
* Connecting Python applications to MySQL
* Implementing authentication and role-based permissions
* Handling configuration using `.ini` files
* Working with files and CSV reports
* Multithreading and concurrent network operations
* Docker containers and MySQL
* Separating application logic from UI definitions
* Debugging and maintaining an application consisting of multiple modules

## Screenshots

### Main Screen

<img width="799" height="603" alt="obraz" src="https://github.com/user-attachments/assets/0f507d0c-f5ba-4453-9db9-259fb946bdfa" />

### Vehicle Details

<img width="780" height="561" alt="obraz" src="https://github.com/user-attachments/assets/3fa21970-6973-4d21-8b23-c89d4b38b4f8" />

### Repair Management

<img width="793" height="590" alt="obraz" src="https://github.com/user-attachments/assets/958b2f5b-2a5a-4bff-81e9-d8b7244dde6e" />

### Settings

<img width="797" height="599" alt="obraz" src="https://github.com/user-attachments/assets/4048de84-ab62-4d34-b305-80132cbf4f02" />


## Project Status

The project is currently maintained as a personal portfolio project.

Future improvements may include:

* Improved database initialization
* Additional reporting functionality
* Improved error handling
* Additional automated tests
* Further UI improvements
