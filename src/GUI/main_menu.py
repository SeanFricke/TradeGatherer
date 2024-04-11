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
        self.AF_logo = QIcon()  # Alecaframe logo declaration
        self.AF_logo.addFile("../Static/Main Menu/Alecaframe_Icon.png")  # AlecaFrame logo assignment

        # --Core constructors--
        self.__api, self.__db = api_obj, db_obj  # Utils
        self.app = QApplication(sys.argv)  # Main Application
        self.NativeScreen = self.app.primaryScreen()  # Native screen info

        # --Widget constructors--
        self.item_buttons_group = QButtonGroup(self)
        self.item_button_box = QWidget()  # Item button box
        self.item_button_layout = QVBoxLayout()  # Item button box (Layout)
        self.scroll_area = QScrollArea()  # Scroll Area
        self.container = QWidget()  # Container
        self.container_layout = QVBoxLayout()  # Container (Layout)
        self.input = QLineEdit()  # Search bar
        self.completer = QCompleter(self.__db.items_df)  # Search bar autocompleter
        self.tool = QToolBar()  # Tool Bar
        self.af_dir_pick = QPushButton()  # AF directory selector button

        # --Window settings--
        self.resize(self.NativeScreen.size())

        # -- Variable init--
        self.item_buttons = []
        self.selected_items = []

        # --Button group settings--
        self.item_buttons_group.setExclusive(False)
        self.item_buttons_group.buttonToggled.connect(lambda button, isToggled: self.selectItemButton(isToggled, button.objectName()))

        # --Button list creation--
        for item in self.__db.items_df.keys():
            item_obj = custom_widgets.itemButtonList(100, item)  # Create button
            self.item_buttons_group.addButton(item_obj)
            self.item_button_layout.addWidget(item_obj)  # Add button to layout
            self.item_buttons.append(item_obj)  # Append button object to list

        # -- Item button box settings--
        spacer = QSpacerItem(1, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.item_button_layout.addItem(spacer)  # Add spacer to button list layout
        self.item_button_box.setLayout(self.item_button_layout)  # Set button list to use corresponding layout

        # --Scroll area settings--
        self.scroll_area.setWidget(self.item_button_box)  # Add button list to scroll area
        self.scroll_area.setWidgetResizable(True)  # Make scroll area resizable

        # --Search bar settings--
        self.input.setFixedHeight(50)  # Set height size of searchbar
        self.input.setFont(QFont("Arial", 30))  # Set font of searchbar
        self.input.textChanged.connect(self.update_items)  # Connect button list updater to text change signal

        # --AF file button settings--
        self.af_dir_pick.setIcon(self.AF_logo)  # Set button icon to AF logo
        self.af_dir_pick.clicked.connect(self.set_AF_dir)  # Connect file dialog prompt to click signal

        # --Tool bar settings--
        self.tool.addWidget(self.af_dir_pick)  # Add AF dir select button to toolbar

        # --Search Bar completer settings
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)  # Make completion case-insensitive
        self.completer.setCompletionMode(QCompleter.CompletionMode.InlineCompletion)  # Set completion to be inline
        self.input.setCompleter(self.completer)  # Attach completer to searchbar

        # --Main container settings--
        self.container_layout.addWidget(self.tool)  # Add toolbar to layout
        self.container_layout.addWidget(self.input)  # Add searchbar to layout
        self.container_layout.addWidget(self.scroll_area)  # Add button scroll area to layout
        self.container.setLayout(self.container_layout)  # Set container to use layout

        self.setCentralWidget(self.container)  # Attach container to main window

    def update_items(self, text: str):
        """
        Updater function for item searchbar. Will only show relevant item buttons.
        :param text: String to filter by
        """
        # Collect relevant results from search string
        results = self.__db.searchItems(text, scorer=rf.fuzz.token_set_ratio)

        # If iterated item name is in search results, show corresponding button
        # Else hide button
        for widget in self.item_buttons:
            if widget.objectName() in results:
                widget.show()
            else:
                widget.hide()

    def set_AF_dir(self):
        """
        Prompts user to select AF export directory, and save to the database attribute for it
        """
        self.__db.af_path = QFileDialog.getExistingDirectory(parent=self.af_dir_pick,
                                                             caption="Select AlecaFrame export directory",
                                                             directory=os.environ.get("USERPROFILE") + "/Documents")

    def selectItemButton(self, isChecked, name: custom_widgets.itemButtonList):

        if isChecked:
            self.selected_items.append(name)
        else:
            self.selected_items.remove(name)
