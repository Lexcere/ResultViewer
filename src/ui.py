import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QSpinBox, QCheckBox, QPushButton, QTreeWidget, QGridLayout
from PyQt5.QtWidgets import QMenuBar, QMenu, QToolBar


class Window(QMainWindow):
    """Main Window."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle("Result Viewer")

        # this will hide the title bar
        # self.setWindowFlag(Qt.FramelessWindowHint)

        self.showMaximized()
        self.centralWidget = QLabel("Hello, World")
        self.centralWidget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(self.centralWidget)
        # self._create_menu_bar()
        self._create_tool_bars()

    def _create_menu_bar(self):
        menuBar = self.menuBar()
        # Creating menus using a QMenu object
        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        # Creating menus using a title
        editMenu = menuBar.addMenu("&Edit")
        helpMenu = menuBar.addMenu("&Help")

        self.setMenuBar(menuBar)

    def _create_tool_bars(self):
        main_tool_bar = QToolBar("Toolbar", self)
        self.addToolBar(Qt.TopToolBarArea, main_tool_bar)

        # add open button
        self.open_button = QPushButton("Open")
        main_tool_bar.addWidget(self.open_button)

        # add refresh button
        self.refresh_button = QPushButton("Refresh")
        main_tool_bar.addWidget(self.refresh_button)

        # add checkbox
        self.recursive_label = QLabel("Recursive")
        main_tool_bar.addWidget(self.recursive_label)

        self.recursive_check_box = QCheckBox()
        self.recursive_check_box.setFocusPolicy(Qt.NoFocus)
        main_tool_bar.addWidget(self.recursive_check_box)

        # add spin box
        self.fontSizeSpinBox = QSpinBox()
        self.fontSizeSpinBox.setFocusPolicy(Qt.NoFocus)
        main_tool_bar.addWidget(self.fontSizeSpinBox)

        # add choose path
        self.path_label = QLabel("my/choosen/path")
        main_tool_bar.addWidget(self.path_label)

        # add generate button
        self.generate_button = QPushButton("Generate report")
        self.generate_button.setToolTip("Generate html report from current directory")
        main_tool_bar.addWidget(self.generate_button)


def main():
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
