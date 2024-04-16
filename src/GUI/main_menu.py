import os
import sys

from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon, QPixmap, QFont

import rapidfuzz as rf

from src.Utils import api, database, utils
from src.GUI import custom_widgets


class MainWindow(QMainWindow):
    def __init__(self, api_obj: api, db_obj: database, parent=None):
        """
        Constructs the main menu.
        :param api_obj: API object from api.py
        :param db_obj: Database object from database.py
        """
        super(MainWindow, self).__init__(parent)

        # --Core constructors--
        self.__api, self.__db = api_obj, db_obj  # Utils
        self.app = QApplication(sys.argv)  # Main Application
        self.NativeScreen = self.app.primaryScreen()  # Native screen info

        # --Widget constructors--
        self.title_label = QLabel()
        self.af_dir_pick = QPushButton()  # AF directory selector button
        self.tool = QToolBar()  # Tool Bar
        self.input = QLineEdit()  # Search bar
        self.completer = QCompleter(self.__db.items_df)  # Search bar autocompleter
        self.item_buttons_group = QButtonGroup()
        self.item_button_box = QWidget()  # Item button box
        self.item_button_layout = QVBoxLayout()  # Item button box (Layout)
        self.scroll_area = QScrollArea()  # Scroll Area
        self.container = QWidget()  # Container
        self.container_layout = QVBoxLayout()  # Container (Layout)
        self.search_button = QPushButton()
        self.exit_button = QPushButton()
        self.bottom_section_box = QWidget()
        self.bottom_section_layout = QHBoxLayout()

        # --Static asset init--
        self.AF_logo = QIcon("../Static/Main Menu/Alecaframe_Icon.png")  # Alecaframe logo
        self.title_pixmap = QPixmap("../Static/Main Menu/TradGathererLogo_Wide_XL.png").scaledToHeight(100)

        # -- Stylesheets--
        self.TITLE_STYLE = """
        QLabel { background-color: #0537ac }
        """

        # --Variable init--
        self.item_buttons = []
        self.selected_items = []

        # --Constants init--
        self.TITLE_SIZE = QSize(self.NativeScreen.size().width(), self.title_pixmap.size().height())
        self.AF_LOGO_SIZE = QSize(25, 25)


        # --Window settings--
        self.resize(self.NativeScreen.size())
        self.setWindowTitle("TradeGatherer")

        # --Title bar settings--
        self.title_label.setPixmap(self.title_pixmap)
        self.title_label.setFixedSize(self.TITLE_SIZE)
        self.title_label.setStyleSheet(self.TITLE_STYLE)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)


        # --AF file button settings--
        self.af_dir_pick.setIcon(self.AF_logo)  # Set button icon to AF logo
        self.af_dir_pick.setIconSize(self.AF_LOGO_SIZE)
        self.af_dir_pick.clicked.connect(self.set_AF_dir)  # Connect file dialog prompt to click signal

        # --Tool bar settings--
        self.tool.addWidget(self.af_dir_pick)  # Add AF dir select button to toolbar

        # --Search bar settings--
        self.input.setFixedHeight(50)  # Set height size of searchbar
        self.input.setFont(QFont("Arial", 30))  # Set font of searchbar
        self.input.textChanged.connect(self.update_items)  # Connect button list updater to text change signal

        # --Search Bar completer settings
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)  # Make completion case-insensitive
        self.input.setCompleter(self.completer)  # Attach completer to searchbar

        # --Button group settings--
        self.item_buttons_group.setExclusive(False)
        self.item_buttons_group.buttonToggled.connect(
            lambda button, isToggled: self.selectItemButton(isToggled, button.objectName()))

        # --Button list creation--
        for item in self.__db.items_df.keys():
            item_obj = custom_widgets.itemButtonList(100, item)  # Create button
            self.item_buttons_group.addButton(item_obj)
            self.item_button_layout.addWidget(item_obj)  # Add button to layout
            self.item_buttons.append(item_obj)  # Append button object to list

        # -- Button settings--
        spacer = QSpacerItem(1, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.item_button_layout.addItem(spacer)  # Add spacer to button list layout
        self.item_button_box.setLayout(self.item_button_layout)  # Set button list to use corresponding layout
        self.search_button.setText("Search")
        self.search_button.setFixedSize(400, 25)
        self.exit_button.setText("Exit")
        self.exit_button.setFixedSize(50, 25)
        self.exit_button.clicked.connect(lambda x: sys.exit())
        self.bottom_section_layout.addSpacing(round(self.NativeScreen.size().width() * 0.35))
        self.bottom_section_layout.addWidget(self.search_button)
        self.bottom_section_layout.addSpacing(round(self.NativeScreen.size().width() * 0.3))
        self.bottom_section_layout.addWidget(self.exit_button)

        # --Scroll area settings--
        self.scroll_area.setWidget(self.item_button_box)  # Add button list to scroll area
        self.scroll_area.setWidgetResizable(True)  # Make scroll area resizable

        # self.bottom_section_layout.insertItem(1, spacer)
        self.bottom_section_box.setLayout(self.bottom_section_layout)

        # --Main container settings--
        self.container_layout.addWidget(self.title_label)
        self.container_layout.addWidget(self.tool)  # Add toolbar to layout
        self.container_layout.addWidget(self.input)  # Add searchbar to layout
        self.container_layout.addWidget(self.scroll_area)  # Add button scroll area to layout
        self.container_layout.addWidget(self.bottom_section_box)
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
