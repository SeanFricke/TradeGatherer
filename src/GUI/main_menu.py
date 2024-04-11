import os
import sys

import PyQt6.QtCore
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

import rapidfuzz as rf

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

        # --Static asset init--
        self.AF_logo = QIcon()
        self.AF_logo.addFile("../Static/Main Menu/Alecaframe_Icon.png")

        # --Core constructors--
        self.__api, self.__db = api_obj, db_obj  # Utils
        self.app = QApplication(sys.argv)
        self.NativeScreen = self.app.primaryScreen()

        # --Widget constructors--
        self.item_button_box = QWidget()  # Item button box
        self.item_button_layout = QVBoxLayout()  # Item button box (Layout)
        self.scroll_area = QScrollArea()  # Scroll Area
        self.container = QWidget()  # Container
        self.container_layout = QVBoxLayout()  # Container (Layout)
        self.input = QLineEdit()  # Search bar
        self.tool = QToolBar()  # Tool Bar
        self.af_dir_pick = QPushButton()

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

        # --AF file button settings--
        self.af_dir_pick.setIcon(self.AF_logo)
        self.af_dir_pick.clicked.connect(self.set_AF_dir)

        # --Tool bar settings--
        self.tool.addWidget(self.af_dir_pick)

        # --Search Bar completer settings
        self.completer = QCompleter(self.__db.items_df)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.setCompletionMode(QCompleter.CompletionMode.InlineCompletion)
        self.input.setCompleter(self.completer)

        # --Main container settings--
        self.container_layout.addWidget(self.tool)
        self.container_layout.addWidget(self.input)
        self.container_layout.addWidget(self.scroll_area)
        self.container.setLayout(self.container_layout)

        self.setCentralWidget(self.container)

    def update_items(self, text):

        results = self.__db.searchItems(text, scorer=rf.fuzz.token_set_ratio)

        for widget in self.item_buttons:
            if widget.objectName() in results:
                widget.show()
            else:
                widget.hide()

    def set_AF_dir(self):
        self.__db.af_path = QFileDialog.getExistingDirectory(parent=self.af_dir_pick,
                                                             caption="Select AlecaFrame export directory",
                                                             directory=os.environ.get("USERPROFILE") + "/Documents")
