import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class mainMenu:
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    screen_size = screen.size()

    win = QMainWindow()

    def main(self, fullscreen: bool):

        self.win.setGeometry(0, 0, self.screen_size.width(), self.screen_size.height())
        self.win.setWindowTitle("Trade Gatherer")

        if fullscreen:
            self.win.showFullScreen()
        else:
            self.win.show()
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    menu = mainMenu()
    menu.main(False)
