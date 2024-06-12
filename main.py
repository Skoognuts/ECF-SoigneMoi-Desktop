#-*- coding: utf-8 -*-

import os
import sys
import mysql.connector

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

        ### DATABASE CONNEXION ###
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

        ### LAYOUT ###
        central_widget = QWidget()
        central_widget.setObjectName("central_widget")
        grid_layout = QGridLayout()
        central_widget.setLayout(grid_layout)
        central_widget.setStyleSheet("QWidget#central_widget { background-color: qlineargradient(x1: 0.5, y1: 0.5 x2: 0.5, y2: 1, stop: 0 #FFFFFF, stop: 0.7 #AACCFF ) }")

        ### LAYOUT DEBUG ONLY ###
        # central_widget.setStyleSheet("border: 1px solid red")
        ### LAYOUT DEBUG ONLY ###

        title = QWidget()
        title_layout = QGridLayout()
        title.setLayout(title_layout)

        logo = QLabel()
        pixmap = QPixmap(os.path.join(IMAGE_DIR, "logo.png"))
        logo.setPixmap(pixmap)
        logo.setStyleSheet("margin-top: 40px")

        main_title = QLabel("SoigneMoi")
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
        ### HANDLING USER EMPTY INPUTS ###
        if self.input_widget.text() == "":
            infoMessageDisplay("Le nom d'utilisateur est obligatoire pour se connecter.")
            self.resetLoginForm()
        elif self.password_widget.text() == "":
            infoMessageDisplay("Le mot de passe est obligatoire pour se connecter.")
            self.resetLoginForm()
        else:
            result = checkCredentials(self.input_widget.text(), self.password_widget.text())
            if result[0] == True:
                print(result[1][4] + " " + result[1][5] + " est connecté")
                self.close()
                self.window = MainWindow()
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
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("SoigneMoi Pro | v1.0")
        self.setWindowIcon(QIcon(ICON_FILE))
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)

if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = LoginWindow()
    sys.exit(App.exec())