#-*- coding: utf-8 -*-

import os
import sys

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

CUR_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(CUR_DIR, "assets")
IMAGE_DIR = os.path.join(DATA_DIR, "images")
ICON_FILE = os.path.join(CUR_DIR, "logo.ico")

def infoMessageDisplay(message):
    msg = QMessageBox()
    msg.setWindowTitle("SoigneMoi")
    msg.setWindowIcon(QIcon(ICON_FILE))
    msg.setIcon(QMessageBox.Icon.Information)
    msg.setText("Info :")
    msg.setInformativeText(message)
    msg.exec()

def errorMessageDisplay(message):
    msg = QMessageBox()
    msg.setWindowTitle("SoigneMoi")
    msg.setWindowIcon(QIcon(ICON_FILE))
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setText("Erreur :")
    msg.setInformativeText(message)
    sys.exit(msg.exec())