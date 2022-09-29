import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QSpinBox, QCheckBox, QPushButton, QTreeWidget, QAction, \
    QFileDialog
from PyQt5.QtWidgets import QMenuBar, QMenu, QToolBar
import ResultsParser


class Window(QMainWindow):
    """Main Window."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle("Result Viewer")

        # this will hide the title bar
        # self.setWindowFlag(Qt.FramelessWindowHint)

        self.showMaximized()

        # self._create_menu_bar()
        self._create_actions()
        self._create_tool_bars()

        self.tree = QTreeWidget()
        self.tree.setColumnCount(3)
        self.tree.setHeaderLabels(['#', 'TC', 'Status'])
        # self.tree.show()

        self.setCentralWidget(self.tree)

    def _create_actions(self):
        self.open_action = QAction("Open button", self)
        self.open_action.setStatusTip("this is my button")
        self.open_action.triggered.connect(self.open_folder)

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

        self.open_button = QPushButton(self)
        self.open_button.setText("Open")
        self.refresh_button = QPushButton("Refresh")
        self.recursive_label = QLabel("Recursive")
        self.recursive_check_box = QCheckBox()
        self.recursive_check_box.setFocusPolicy(Qt.NoFocus)
        self.fontSizeSpinBox = QSpinBox()
        self.fontSizeSpinBox.setFocusPolicy(Qt.NoFocus)
        self.path_label = QLabel("my/choosen/path")
        self.generate_button = QPushButton("Generate report")
        self.generate_button.setToolTip("Generate html report from current directory")

        self.open_button.clicked.connect(self.open_folder)
        self.refresh_button.clicked.connect(self.refresh)
        self.generate_button.clicked.connect(self.generate_report)

        main_tool_bar.addWidget(self.open_button)
        main_tool_bar.addWidget(self.refresh_button)
        main_tool_bar.addWidget(self.recursive_label)
        main_tool_bar.addWidget(self.recursive_check_box)
        main_tool_bar.addWidget(self.fontSizeSpinBox)
        main_tool_bar.addWidget(self.path_label)
        main_tool_bar.addWidget(self.generate_button)

    def open_folder(self):
        folder_path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.path_label.setText(folder_path)

    def refresh(self):
        print("refresh")

    def generate_report(self):
        print("generate report")

def main():
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
