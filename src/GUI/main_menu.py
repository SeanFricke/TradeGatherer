import sys

import PyQt5.QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from src.Utils import api, database, utils


class mainMenu(QApplication):

    def __init__(self, api_obj: api.API, db_obj: database.Database):
        super().__init__(sys.argv)
        self.__api = api_obj
        self.__db = db_obj
        self.screen = self.primaryScreen()
        self.screen_size = self.screen.size()
        self.win = QMainWindow()

        self.__items_box = QGroupBox(self.win)
        self.__items_box_layout = QVBoxLayout()
        self.create_item_buttons()
        self.__items_box.setLayout(self.__items_box_layout)
        self.__items_box.setFixedWidth(self.screen_size.width())

        self.scroll_area = QScrollArea(self.win)
        self.scroll_area.setWidget(self.__items_box)
        self.scroll_area.setFixedSize(self.screen_size)

    def main(self, fullscreen: bool):
        self.win.setGeometry(0, 0, self.screen_size.width(), self.screen_size.height())
        self.win.setWindowTitle("Trade Gatherer")

        if fullscreen:
            self.win.showFullScreen()
        else:
            self.win.show()
        sys.exit(self.exec_())

    def create_item_buttons(self):
        button_iter = 0
        for item in self.__db.items_df.keys():
            button = QPushButton(self.win)
            button.resize(self.screen_size.width(), 200)
            button.setText(item)
            button.setCheckable(True)
            self.__items_box_layout.addWidget(button, button_iter)
            button_iter += 1
