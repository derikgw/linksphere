import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QVBoxLayout, QHBoxLayout, QWidget, QTreeView, QTableView, QToolBar, QStatusBar


def load_stylesheet(filename):
    path = os.path.join(os.path.dirname(__file__), "..", "themes", filename)
    with open(path, "r") as file:
        return file.read()


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('LinkSphere')
        self.setGeometry(100, 100, 1200, 800)

        # Create a central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create the main layout
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # Create a sidebar
        sidebar = QTreeView()
        sidebar.setFixedWidth(250)
        main_layout.addWidget(sidebar)

        # Create a central area
        central_area = QTableView()
        main_layout.addWidget(central_area)

        # Create a toolbar
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        # Add actions to the toolbar
        add_shortcut_action = QAction("Add Shortcut", self)
        toolbar.addAction(add_shortcut_action)

        add_note_action = QAction("Add Note", self)
        toolbar.addAction(add_note_action)

        # Create a status bar
        self.setStatusBar(QStatusBar(self))

        # Create a menu bar
        menu_bar = self.menuBar()

        # Add menus to the menu bar
        file_menu = menu_bar.addMenu("File")
        edit_menu = menu_bar.addMenu("Edit")
        view_menu = menu_bar.addMenu("View")
        help_menu = menu_bar.addMenu("Help")

        # Add actions to the file menu
        file_menu.addAction(add_shortcut_action)
        file_menu.addAction(add_note_action)
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close)

        # Add theme actions
        self.light_theme_action = QAction("Light Theme", self, checkable=True)
        self.dark_theme_action = QAction("Dark Theme", self, checkable=True)

        theme_menu = menu_bar.addMenu("Theme")
        theme_menu.addAction(self.light_theme_action)
        theme_menu.addAction(self.dark_theme_action)

        # Connect theme actions
        self.light_theme_action.triggered.connect(lambda: self.apply_theme("light_theme.qss"))
        self.dark_theme_action.triggered.connect(lambda: self.apply_theme("dark_theme.qss"))

        # Set initial theme
        self.apply_theme("light_theme.qss")

    def apply_theme(self, stylesheet_path):
        stylesheet = load_stylesheet(stylesheet_path)
        self.setStyleSheet(stylesheet)
        if "light" in stylesheet_path:
            self.light_theme_action.setChecked(True)
            self.dark_theme_action.setChecked(False)
        else:
            self.light_theme_action.setChecked(False)
            self.dark_theme_action.setChecked(True)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
