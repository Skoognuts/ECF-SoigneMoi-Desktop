#-*- coding: utf-8 -*-

import os
import sys
import mysql.connector

from datetime import date

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from _login import *
from _message import *

CUR_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(CUR_DIR, "assets")
IMAGE_DIR = os.path.join(DATA_DIR, "images")
ICON_FILE = os.path.join(CUR_DIR, "logo.ico")

class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        
        self.setWindowTitle("SoigneMoi Pro | v1.0")
        self.setWindowIcon(QIcon(ICON_FILE))
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)

        try:
            mydb = mysql.connector.connect(
                host = "localhost",
                database = "soigne_moi",
                user = "root",
                password = ""
            )
            mydb.close()
        except:
            errorMessageDisplay("La connexion à la base de données a échoué. Veuillez vérifier votre connexion et réessayer.")

        central_widget = QWidget()
        central_widget.setObjectName("central_widget")
        grid_layout = QGridLayout()
        central_widget.setLayout(grid_layout)
        central_widget.setStyleSheet(
            "QWidget#central_widget { background-color: qlineargradient(x1: 0.5, y1: 0.5 x2: 0.5, y2: 1, stop: 0 #FFFFFF, stop: 0.7 #AACCFF ) }"
        )

        title = QWidget()
        title_layout = QGridLayout()
        title.setLayout(title_layout)

        logo = QLabel()
        pixmap = QPixmap(os.path.join(IMAGE_DIR, "logo.png"))
        logo.setPixmap(pixmap)
        logo.setStyleSheet("margin-top: 40px")

        main_title = QLabel("Soigne Moi")
        main_title.setStyleSheet("font-size: 60px")
        sub_title = QLabel("Version Pro 1.0")
        sub_title.setStyleSheet("font-size: 20px")

        title_layout.addWidget(logo, 0, 0, 1, 1,  Qt.AlignmentFlag.AlignCenter)
        title_layout.addWidget(main_title, 1, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)
        title_layout.addWidget(sub_title, 2, 0, 1, 1, Qt.AlignmentFlag.AlignCenter)

        grid_layout.addWidget(title, 0, 0, Qt.AlignmentFlag.AlignCenter)

        form = QWidget()
        form_layout = QGridLayout()
        form.setLayout(form_layout)

        input_label = QLabel("Nom d'utilisateur ")
        self.input_widget = QLineEdit()
        self.input_widget.setStyleSheet(
            "QLineEdit { border: 4px outset white; border-radius: 8px; width: 250px }"
        )
        form_layout.addWidget(input_label, 0, 0)
        form_layout.addWidget(self.input_widget, 0, 1)

        password_label = QLabel("Mot de passe ")
        self.password_widget = QLineEdit(echoMode=QLineEdit.EchoMode.Password)
        self.password_widget.setStyleSheet(
            "QLineEdit { border: 4px outset white; border-radius: 8px; width: 250px }"
        )
        form_layout.addWidget(password_label, 1, 0)
        form_layout.addWidget(self.password_widget, 1, 1)

        login_button = QPushButton("Se Connecter")
        login_button.setStyleSheet(
            "QPushButton { margin-top: 20px; background-color: #319997; color: white; font-weight: bold; border-radius: 8px; height: 30px }"
            "QPushButton:hover { background-color: #61B9B7 }"
        )
        login_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        login_button.clicked.connect(self.login)
        form_layout.addWidget(login_button, 2, 0, 1, 2)

        grid_layout.addWidget(form, 1, 0, Qt.AlignmentFlag.AlignCenter)

        self.setCentralWidget(central_widget)
        self.show()

    def login(self):
        if self.input_widget.text() == "":
            infoMessageDisplay("Le nom d'utilisateur est obligatoire pour se connecter.")
            self.resetLoginForm()
        elif self.password_widget.text() == "":
            infoMessageDisplay("Le mot de passe est obligatoire pour se connecter.")
            self.resetLoginForm()
        else:
            result = checkCredentials(self.input_widget.text(), self.password_widget.text())
            if result[0] == True:
                self.close()
                self.window = MainWindow(result[1])
                self.window.show()
            elif result[0] == False and result[1] == True:
                infoMessageDisplay("Vos identifiants sont incorrects, veuillez réessayer.")
                self.resetLoginForm()
            elif result[0] == False and result[0] == False:
                infoMessageDisplay("Un problème est survenu, veuillez réessayer plus tard")

    def resetLoginForm(self):
        self.input_widget.setText("")
        self.password_widget.setText("")

class MainWindow(QMainWindow):
    def __init__(self, user):
        super(MainWindow, self).__init__()

        self.setWindowTitle("SoigneMoi Pro | v1.0")
        self.setWindowIcon(QIcon(ICON_FILE))
        self.setMinimumWidth(1400)
        self.setMinimumHeight(900)

        self.user = user

        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        self.tab_dashboard = QWidget()
        self.tab_entries = QWidget()
        self.tab_patients = QWidget()

        self.tab_widget.addTab(self.tab_dashboard," TABLEAU DE BORD ")
        self.tab_widget.addTab(self.tab_entries," ADMISSIONS ")
        self.tab_widget.addTab(self.tab_patients," PATIENTS ")

        self.tabDashboardUI()
        self.tabEntriesUI()
        self.tabPatientsUI()

    def tabDashboardUI(self):
        grid_layout = QGridLayout()
        grid_layout.setSpacing(0)

        ########################################## NAVIGATION LATERALE ##########################################
        nav_tab = QWidget()
        nav_tab.setObjectName("nav_tab")
        nav_tab.setStyleSheet(
            "QWidget#nav_tab { background-color: #000000 }"
        )
        nav_tab.setFixedWidth(300)
        nav_grid_layout = QGridLayout()
        nav_tab.setLayout(nav_grid_layout)

        nav_brand = QWidget()
        nav_brand_layout = QGridLayout()
        nav_brand.setLayout(nav_brand_layout)

        logo = QLabel()
        pixmap = QPixmap(os.path.join(IMAGE_DIR, "logo.png"))
        logo.setPixmap(pixmap)
        main_title = QLabel("Soigne Moi")
        main_title.setStyleSheet("color: white; font-size: 40px; font-weight: bold")
        sub_title = QLabel("Version Pro 1.0")
        sub_title.setStyleSheet("color: #319997; font-size: 15px; font-weight: bold")

        nav_brand_layout.addWidget(logo, 0, 0, 1, 1,  Qt.AlignmentFlag.AlignCenter)
        nav_brand_layout.addWidget(main_title, 1, 0, 1, 1,  Qt.AlignmentFlag.AlignCenter)
        nav_brand_layout.addWidget(sub_title, 2, 0, 1, 1,  Qt.AlignmentFlag.AlignCenter)

        nav_buttons = QWidget()
        nav_buttons_layout = QVBoxLayout()
        nav_buttons_layout.setSpacing(0)
        nav_buttons_layout.setContentsMargins(0, 0, 0, 0)
        nav_buttons_layout.addStretch(1)
        nav_buttons.setLayout(nav_buttons_layout)

        button1 = QPushButton("Tableau de bord", self)
        button1.clicked.connect(self.gotoTabDashboard)
        button1.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        button1.setStyleSheet(
            "QPushButton { background-color: #000000; color: #7289DA; font-size: 30px; font-weight: bold; text-align: left }"
            "QPushButton:hover { color: #319997 }"
        )
        button2 = QPushButton("Admissions", self)
        button2.clicked.connect(self.gotoTabEntries)
        button2.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        button2.setStyleSheet(
            "QPushButton { background-color: #000000; color: white; font-size: 30px; font-weight: bold; text-align: left }"
            "QPushButton:hover { color: #319997 }"
        )
        button3 = QPushButton("Patients", self)
        button3.clicked.connect(self.gotoTabPatients)
        button3.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        button3.setStyleSheet(
            "QPushButton { background-color: #000000; color: white; font-size: 30px; font-weight: bold; text-align: left }"
            "QPushButton:hover { color: #319997 }"
        )
        button4 = QPushButton("Déconnexion", self)
        button4.clicked.connect(self.disconnect)
        button4.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        button4.setStyleSheet(
            "QPushButton { background-color: #000000; color: white; font-size: 30px; font-weight: bold; text-align: left }"
            "QPushButton:hover { color: #FFA500 }"
        )

        nav_buttons_layout.addWidget(button1)
        nav_buttons_layout.addWidget(button2)
        nav_buttons_layout.addWidget(button3)
        nav_buttons_layout.addWidget(button4)

        nav_user = QWidget()
        nav_user_layout = QHBoxLayout()
        nav_user_layout.setSpacing(0)
        nav_user.setLayout(nav_user_layout)

        user_logo = QLabel()
        pixmap = QPixmap(os.path.join(IMAGE_DIR, "user.png"))
        user_logo.setPixmap(pixmap)

        user_name = QLabel(self.user[3] + " " + self.user[4])
        user_name.setStyleSheet("color: white; font-size: 20px")

        nav_user_layout.addWidget(user_logo, Qt.AlignmentFlag.AlignLeft)
        nav_user_layout.addWidget(user_name, Qt.AlignmentFlag.AlignLeft)
        nav_user_layout.addStretch(1)

        nav_grid_layout.addWidget(nav_brand, 0, 0, 1, 1)
        nav_grid_layout.addWidget(nav_buttons, 1, 0, 1, 1,  Qt.AlignmentFlag.AlignCenter)
        nav_grid_layout.addWidget(nav_user, 2, 0, 1, 1,  Qt.AlignmentFlag.AlignBottom)

        ########################################## HEADER ##########################################
        header = QWidget()
        header.setObjectName("header")
        header.setStyleSheet(
            "QWidget#header { background-color: qlineargradient(x1: 0.5, y1: 0.5 x2: 0.5, y2: 1, stop: 0 #AACCFF, stop: 0.7 #CCEEFF ) }"
        )
        header.setFixedHeight(200)
        header_layout = QVBoxLayout()
        header.setLayout(header_layout)

        shadow1 = QGraphicsDropShadowEffect()
        shadow1.setOffset(0, 0)
        shadow1.setBlurRadius(10)
        shadow1.setColor(QColor("#000000"))

        header_title = QLabel("TABLEAU DE BORD")
        header_title.setStyleSheet("color: white; font-size: 50px; font-weight: bold")
        header_title.setGraphicsEffect(shadow1)

        shadow2 = QGraphicsDropShadowEffect()
        shadow2.setOffset(0, 0)
        shadow2.setBlurRadius(5)
        shadow2.setColor(QColor("#000000"))

        today_date = date.today().strftime("%d/%m/%Y")
        header_date = QLabel("> " + today_date)
        header_date.setStyleSheet("color: white; font-size: 30px")
        header_date.setGraphicsEffect(shadow2)

        header_layout.addWidget(header_title)
        header_layout.addWidget(header_date)
        header_layout.addStretch(1)

        ########################################## MAIN ##########################################
        main = QWidget()
        main.setStyleSheet(
            "QWidget { background-color: #FFFFFF }"
        )

        grid_layout.addWidget(nav_tab, 0, 0, 2, 1)
        grid_layout.addWidget(header, 0, 1, 1, 1)
        grid_layout.addWidget(main, 1, 1, 1, 1)

        self.tab_dashboard.setLayout(grid_layout)

    def tabEntriesUI(self):
        grid_layout = QGridLayout()
        grid_layout.setSpacing(0)

        ########################################## NAVIGATION LATERALE ##########################################
        nav_tab = QWidget()
        nav_tab.setObjectName("nav_tab")
        nav_tab.setStyleSheet(
            "QWidget#nav_tab { background-color: #000000 }"
        )
        nav_tab.setFixedWidth(300)
        nav_grid_layout = QGridLayout()
        nav_tab.setLayout(nav_grid_layout)

        nav_brand = QWidget()
        nav_brand_layout = QGridLayout()
        nav_brand.setLayout(nav_brand_layout)

        logo = QLabel()
        pixmap = QPixmap(os.path.join(IMAGE_DIR, "logo.png"))
        logo.setPixmap(pixmap)
        main_title = QLabel("Soigne Moi")
        main_title.setStyleSheet("color: white; font-size: 40px; font-weight: bold")
        sub_title = QLabel("Version Pro 1.0")
        sub_title.setStyleSheet("color: #319997; font-size: 15px; font-weight: bold")

        nav_brand_layout.addWidget(logo, 0, 0, 1, 1,  Qt.AlignmentFlag.AlignCenter)
        nav_brand_layout.addWidget(main_title, 1, 0, 1, 1,  Qt.AlignmentFlag.AlignCenter)
        nav_brand_layout.addWidget(sub_title, 2, 0, 1, 1,  Qt.AlignmentFlag.AlignCenter)

        nav_buttons = QWidget()
        nav_buttons_layout = QVBoxLayout()
        nav_buttons_layout.setSpacing(0)
        nav_buttons_layout.setContentsMargins(0, 0, 0, 0)
        nav_buttons_layout.addStretch(1)
        nav_buttons.setLayout(nav_buttons_layout)

        button1 = QPushButton("Tableau de bord", self)
        button1.clicked.connect(self.gotoTabDashboard)
        button1.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        button1.setStyleSheet(
            "QPushButton { background-color: #000000; color: white; font-size: 30px; font-weight: bold; text-align: left }"
            "QPushButton:hover { color: #319997 }"
        )
        button2 = QPushButton("Admissions", self)
        button2.clicked.connect(self.gotoTabEntries)
        button2.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        button2.setStyleSheet(
            "QPushButton { background-color: #000000; color: #7289DA; font-size: 30px; font-weight: bold; text-align: left }"
            "QPushButton:hover { color: #319997 }"
        )
        button3 = QPushButton("Patients", self)
        button3.clicked.connect(self.gotoTabPatients)
        button3.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        button3.setStyleSheet(
            "QPushButton { background-color: #000000; color: white; font-size: 30px; font-weight: bold; text-align: left }"
            "QPushButton:hover { color: #319997 }"
        )
        button4 = QPushButton("Déconnexion", self)
        button4.clicked.connect(self.disconnect)
        button4.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        button4.setStyleSheet(
            "QPushButton { background-color: #000000; color: white; font-size: 30px; font-weight: bold; text-align: left }"
            "QPushButton:hover { color: #FFA500 }"
        )

        nav_buttons_layout.addWidget(button1)
        nav_buttons_layout.addWidget(button2)
        nav_buttons_layout.addWidget(button3)
        nav_buttons_layout.addWidget(button4)

        nav_user = QWidget()
        nav_user_layout = QHBoxLayout()
        nav_user_layout.setSpacing(0)
        nav_user.setLayout(nav_user_layout)

        user_logo = QLabel()
        pixmap = QPixmap(os.path.join(IMAGE_DIR, "user.png"))
        user_logo.setPixmap(pixmap)

        user_name = QLabel(self.user[3] + " " + self.user[4])
        user_name.setStyleSheet("color: white; font-size: 20px")

        nav_user_layout.addWidget(user_logo, Qt.AlignmentFlag.AlignLeft)
        nav_user_layout.addWidget(user_name, Qt.AlignmentFlag.AlignLeft)
        nav_user_layout.addStretch(1)

        nav_grid_layout.addWidget(nav_brand, 0, 0, 1, 1)
        nav_grid_layout.addWidget(nav_buttons, 1, 0, 1, 1,  Qt.AlignmentFlag.AlignCenter)
        nav_grid_layout.addWidget(nav_user, 2, 0, 1, 1,  Qt.AlignmentFlag.AlignBottom)

        ########################################## HEADER ##########################################
        header = QWidget()
        header.setObjectName("header")
        header.setStyleSheet(
            "QWidget#header { background-color: qlineargradient(x1: 0.5, y1: 0.5 x2: 0.5, y2: 1, stop: 0 #AACCFF, stop: 0.7 #CCEEFF ) }"
        )
        header.setFixedHeight(200)
        header_layout = QVBoxLayout()
        header.setLayout(header_layout)

        shadow1 = QGraphicsDropShadowEffect()
        shadow1.setOffset(0, 0)
        shadow1.setBlurRadius(10)
        shadow1.setColor(QColor("#000000"))

        header_title = QLabel("ADMISSIONS")
        header_title.setStyleSheet("color: white; font-size: 50px; font-weight: bold")
        header_title.setGraphicsEffect(shadow1)

        shadow2 = QGraphicsDropShadowEffect()
        shadow2.setOffset(0, 0)
        shadow2.setBlurRadius(5)
        shadow2.setColor(QColor("#000000"))

        today_date = date.today().strftime("%d/%m/%Y")
        header_date = QLabel("> " + today_date)
        header_date.setStyleSheet("color: white; font-size: 30px")
        header_date.setGraphicsEffect(shadow2)

        header_layout.addWidget(header_title)
        header_layout.addWidget(header_date)
        header_layout.addStretch(1)

        ########################################## MAIN ##########################################
        main = QWidget()
        main.setStyleSheet(
            "QWidget { background-color: #FFFFFF }"
        )

        grid_layout.addWidget(nav_tab, 0, 0, 2, 1)
        grid_layout.addWidget(header, 0, 1, 1, 1)
        grid_layout.addWidget(main, 1, 1, 1, 1)

        self.tab_entries.setLayout(grid_layout)

    def tabPatientsUI(self):
        grid_layout = QGridLayout()
        grid_layout.setSpacing(0)

        ########################################## NAVIGATION LATERALE ##########################################
        nav_tab = QWidget()
        nav_tab.setObjectName("nav_tab")
        nav_tab.setStyleSheet(
            "QWidget#nav_tab { background-color: #000000 }"
        )
        nav_tab.setFixedWidth(300)
        nav_grid_layout = QGridLayout()
        nav_tab.setLayout(nav_grid_layout)

        nav_brand = QWidget()
        nav_brand_layout = QGridLayout()
        nav_brand.setLayout(nav_brand_layout)

        logo = QLabel()
        pixmap = QPixmap(os.path.join(IMAGE_DIR, "logo.png"))
        logo.setPixmap(pixmap)
        main_title = QLabel("Soigne Moi")
        main_title.setStyleSheet("color: white; font-size: 40px; font-weight: bold")
        sub_title = QLabel("Version Pro 1.0")
        sub_title.setStyleSheet("color: #319997; font-size: 15px; font-weight: bold")

        nav_brand_layout.addWidget(logo, 0, 0, 1, 1,  Qt.AlignmentFlag.AlignCenter)
        nav_brand_layout.addWidget(main_title, 1, 0, 1, 1,  Qt.AlignmentFlag.AlignCenter)
        nav_brand_layout.addWidget(sub_title, 2, 0, 1, 1,  Qt.AlignmentFlag.AlignCenter)

        nav_buttons = QWidget()
        nav_buttons_layout = QVBoxLayout()
        nav_buttons_layout.setSpacing(0)
        nav_buttons_layout.setContentsMargins(0, 0, 0, 0)
        nav_buttons_layout.addStretch(1)
        nav_buttons.setLayout(nav_buttons_layout)

        button1 = QPushButton("Tableau de bord", self)
        button1.clicked.connect(self.gotoTabDashboard)
        button1.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        button1.setStyleSheet(
            "QPushButton { background-color: #000000; color: white; font-size: 30px; font-weight: bold; text-align: left }"
            "QPushButton:hover { color: #319997 }"
        )
        button2 = QPushButton("Admissions", self)
        button2.clicked.connect(self.gotoTabEntries)
        button2.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        button2.setStyleSheet(
            "QPushButton { background-color: #000000; color: white; font-size: 30px; font-weight: bold; text-align: left }"
            "QPushButton:hover { color: #319997 }"
        )
        button3 = QPushButton("Patients", self)
        button3.clicked.connect(self.gotoTabPatients)
        button3.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        button3.setStyleSheet(
            "QPushButton { background-color: #000000; color: #7289DA; font-size: 30px; font-weight: bold; text-align: left }"
            "QPushButton:hover { color: #319997 }"
        )
        button4 = QPushButton("Déconnexion", self)
        button4.clicked.connect(self.disconnect)
        button4.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        button4.setStyleSheet(
            "QPushButton { background-color: #000000; color: white; font-size: 30px; font-weight: bold; text-align: left }"
            "QPushButton:hover { color: #FFA500 }"
        )

        nav_buttons_layout.addWidget(button1)
        nav_buttons_layout.addWidget(button2)
        nav_buttons_layout.addWidget(button3)
        nav_buttons_layout.addWidget(button4)

        nav_user = QWidget()
        nav_user_layout = QHBoxLayout()
        nav_user_layout.setSpacing(0)
        nav_user.setLayout(nav_user_layout)

        user_logo = QLabel()
        pixmap = QPixmap(os.path.join(IMAGE_DIR, "user.png"))
        user_logo.setPixmap(pixmap)

        user_name = QLabel(self.user[3] + " " + self.user[4])
        user_name.setStyleSheet("color: white; font-size: 20px")

        nav_user_layout.addWidget(user_logo, Qt.AlignmentFlag.AlignLeft)
        nav_user_layout.addWidget(user_name, Qt.AlignmentFlag.AlignLeft)
        nav_user_layout.addStretch(1)

        nav_grid_layout.addWidget(nav_brand, 0, 0, 1, 1)
        nav_grid_layout.addWidget(nav_buttons, 1, 0, 1, 1,  Qt.AlignmentFlag.AlignCenter)
        nav_grid_layout.addWidget(nav_user, 2, 0, 1, 1,  Qt.AlignmentFlag.AlignBottom)

        ########################################## HEADER ##########################################
        header = QWidget()
        header.setObjectName("header")
        header.setStyleSheet(
            "QWidget#header { background-color: qlineargradient(x1: 0.5, y1: 0.5 x2: 0.5, y2: 1, stop: 0 #AACCFF, stop: 0.7 #CCEEFF ) }"
        )
        header.setFixedHeight(200)
        header_layout = QVBoxLayout()
        header.setLayout(header_layout)

        shadow1 = QGraphicsDropShadowEffect()
        shadow1.setOffset(0, 0)
        shadow1.setBlurRadius(10)
        shadow1.setColor(QColor("#000000"))

        header_title = QLabel("PATIENTS")
        header_title.setStyleSheet("color: white; font-size: 50px; font-weight: bold")
        header_title.setGraphicsEffect(shadow1)

        shadow2 = QGraphicsDropShadowEffect()
        shadow2.setOffset(0, 0)
        shadow2.setBlurRadius(5)
        shadow2.setColor(QColor("#000000"))

        today_date = date.today().strftime("%d/%m/%Y")
        header_date = QLabel("> " + today_date)
        header_date.setStyleSheet("color: white; font-size: 30px")
        header_date.setGraphicsEffect(shadow2)

        header_layout.addWidget(header_title)
        header_layout.addWidget(header_date)
        header_layout.addStretch(1)

        ########################################## MAIN ##########################################
        main = QWidget()
        main.setStyleSheet(
            "QWidget { background-color: #FFFFFF }"
        )

        grid_layout.addWidget(nav_tab, 0, 0, 2, 1)
        grid_layout.addWidget(header, 0, 1, 1, 1)
        grid_layout.addWidget(main, 1, 1, 1, 1)

        self.tab_patients.setLayout(grid_layout)

    def gotoTabDashboard(self):
        self.tab_widget.setCurrentIndex(0)

    def gotoTabEntries(self):
        self.tab_widget.setCurrentIndex(1)

    def gotoTabPatients(self):
        self.tab_widget.setCurrentIndex(2)

    def disconnect(self):
        sys.exit()

if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = LoginWindow()
    sys.exit(App.exec())