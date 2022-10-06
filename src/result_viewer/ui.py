import sys
import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QSpinBox, QCheckBox, QPushButton, QTreeWidget, QAction, \
    QFileDialog, QTreeWidgetItem, QMessageBox, QStatusBar
from PyQt5.QtWidgets import QMenu, QToolBar
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
        self.tree.setAlternatingRowColors(True)
        columns_count = 4
        self.tree.setColumnCount(columns_count)
        self.tree.setHeaderLabels(["#", "TC", "Status", "path"])
        self.tree.hideColumn(columns_count-1)
        self.tree.setSelectionMode(3)  # enum come from https://doc.qt.io/qt-5/qabstractitemview.html#SelectionMode-enum
        self.setCentralWidget(self.tree)
        self.status_bar = QStatusBar()

        self.setStatusBar(self.status_bar)

        self.working_directory = "my/choosen/path"

    def _create_actions(self):
        self.open_action = QAction("Open button", self)
        self.open_action.setStatusTip("this is my button")
        self.open_action.triggered.connect(self.open_folder)

    def _create_menu_bar(self):
        menu_bar = self.menuBar()
        # Creating menus using a QMenu object
        file_menu = QMenu("&File", self)
        menu_bar.addMenu(file_menu)
        # Creating menus using a title
        # editMenu = menu_bar.addMenu("&Edit")
        # helpMenu = menu_bar.addMenu("&Help")

        self.setMenuBar(menu_bar)

    def _create_tool_bars(self):
        main_tool_bar = QToolBar("Toolbar", self)
        self.addToolBar(Qt.TopToolBarArea, main_tool_bar)

        self.open_button = QPushButton(self)
        self.open_button.setText("Open")
        self.refresh_button = QPushButton("Refresh")
        self.recursive_label = QLabel("Recursive")
        self.recursive_check_box = QCheckBox()
        self.recursive_check_box.setFocusPolicy(Qt.NoFocus)
        self.recursive_check_box.setChecked(True)
        self.fontSizeSpinBox = QSpinBox()
        self.fontSizeSpinBox.setMaximum(100000000)
        self.fontSizeSpinBox.setValue(10000)
        self.fontSizeSpinBox.setFocusPolicy(Qt.NoFocus)
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
        main_tool_bar.addWidget(self.generate_button)

    def open_folder(self):
        folder_path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.setWindowTitle(folder_path)
        self.working_directory = folder_path
        self.refresh()

    def refresh(self):
        if not os.path.isdir(self.working_directory):
            error_dialog = QMessageBox(self)
            error_dialog.setIcon(QMessageBox.Warning)
            error_dialog.setWindowTitle("Wrong directory")
            error_dialog.setText(f"selected directory {self.working_directory} does not exist")
            error_dialog.show()
            return
        parser = ResultsParser.TestResultParser(folder_path=self.working_directory, recursive=self.recursive_check_box.isChecked())
        diz, _ = parser.get_dictionary()
        self._populate_tree(diz)

        status_msg = f'{parser.metrics()["total"]} Total, ' \
                     f'{parser.metrics()["pass"]} Passed, ' \
                     f'{parser.metrics()["fail"]} Failed, ' \
                     f'{parser.metrics()["skip"]} Skipped' \
                     f', {parser.metrics()["other"]} Other in .. day/s'
        self.status_bar.showMessage(status_msg)

    def generate_report(self):
        print("generate report")

    def _populate_tree(self, results_dict):
        self.tree.clear()
        for idx in results_dict:
            QTreeWidgetItem(self.tree, [
                                        str(idx),
                                        str(results_dict[idx]["GENERIC"]["test case number"]),
                                        str(results_dict[idx]["GENERIC"]["result"]),
                                        str(results_dict[idx]["GENERIC"]["path"]),
                                        ]
                            )


def main():
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
