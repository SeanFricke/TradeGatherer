from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from src.Utils import api, database


class itemButtonList(QPushButton):
    item_font = QFont("Arial Black", 20)  # Default font

    def __init__(self, button_height: int, name: str, parent=None):
        """
        Creates a button that will select an item
        """
        super().__init__(parent)

        # --Button settings--
        self.setFixedHeight(button_height)  # Button height
        self.setObjectName(name)  # Object name/ID
        self.setText(name)  # Label
        self.setFont(self.item_font)  # Font
        self.setCheckable(True)  # Set to toggleable
