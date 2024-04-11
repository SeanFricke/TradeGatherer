import sys

import PyQt6.QtCore
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from src.Utils import api, database, utils
from src.GUI import custom_widgets


class mainMenu(QMainWindow):
    def __init__(self, api_obj: api, db_obj: database, fullscreen: bool = False, parent=None):
        """
        Constructs the main menu.
        :param api_obj: API object from api.py
        :param db_obj: Database object from database.py
        :param fullscreen: Start in fullscreen
        """
        super().__init__(parent)

        # --Core constructors--
        self.__api, self.__db = api_obj, db_obj  # Utils
        self.app = QApplication(sys.argv)
        self.NativeScreen = self.app.primaryScreen()

        # --Widget constructors--
        self.item_button_box = QWidget()
        self.item_button_layout = QVBoxLayout()
        self.scroll_area = QScrollArea()
        self.container = QWidget()
        self.container_layout = QVBoxLayout()
        self.input = QLineEdit()

        # --Window settings--
        self.resize(self.NativeScreen.size())

        # -- Variable init--
        self.item_buttons = []

        # --Button list creation--
        for item in self.__db.items_df.keys():
            item = custom_widgets.itemButtonList(100, item)  # Create button
            self.item_button_layout.addWidget(item)
            self.item_buttons.append(item)

        # -- Item button box settings--
        spacer = QSpacerItem(1, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.item_button_layout.addItem(spacer)
        self.item_button_box.setLayout(self.item_button_layout)

        # --Scroll area settings--
        self.scroll_area.setWidget(self.item_button_box)
        self.scroll_area.setWidgetResizable(True)

        # --Search bar settings--
        self.input.setFixedHeight(50)
        self.input.setFont(QFont("Arial", 30))
        self.input.textChanged.connect(self.update_items)

        # --Search Bar completer settings
        self.completer = QCompleter(self.__db.items_df)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.input.setCompleter(self.completer)

        # --Main container settings--
        self.container_layout.addWidget(self.input)
        self.container_layout.addWidget(self.scroll_area)
        self.container.setLayout(self.container_layout)

        self.setCentralWidget(self.container)

    def update_items(self, text):

        for widget in self.item_buttons:
            if text.lower() in widget.objectName().lower():
                widget.show()
            else:
                widget.hide()
