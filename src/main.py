import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QVBoxLayout, QHBoxLayout, QWidget, QTreeView, \
    QTableView, QToolBar, QStatusBar, QDialog, QListWidget, QDialogButtonBox, QProgressDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from shortcut_dialog import ShortcutDialog
import platform


def load_stylesheet(filename):
    path = os.path.join(os.path.dirname(__file__), "..", "themes", filename)
    with open(path, "r") as file:
        return file.read()


class ScanDialog(QDialog):

    def __init__(self, applications, stylesheet, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Scan for Applications')
        self.setGeometry(300, 300, 400, 400)

        layout = QVBoxLayout()

        self.list_widget = QListWidget(self)
        for app in applications:
            self.list_widget.addItem(app)
        layout.addWidget(self.list_widget)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

        # Apply the stylesheet
        self.setStyleSheet(stylesheet)

    def get_selected_applications(self):
        return [self.list_widget.item(i).text() for i in range(self.list_widget.count()) if
                self.list_widget.item(i).isSelected()]


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

        # Create a model for the sidebar
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Shortcuts'])
        sidebar.setModel(self.model)

        # Add groups to the model
        self.applications_group = QStandardItem("Applications")
        self.files_group = QStandardItem("Files")
        self.model.appendRow(self.applications_group)
        self.model.appendRow(self.files_group)

        # Create a central area
        central_area = QTableView()
        main_layout.addWidget(central_area)

        # Create a toolbar
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        # Add actions to the toolbar
        add_shortcut_action = QAction("Add Shortcut", self)
        add_shortcut_action.triggered.connect(self.show_add_shortcut_dialog)
        toolbar.addAction(add_shortcut_action)

        scan_apps_action = QAction("Scan for Applications", self)
        scan_apps_action.triggered.connect(self.scan_for_applications)
        toolbar.addAction(scan_apps_action)

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
        file_menu.addAction(scan_apps_action)
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

    def show_add_shortcut_dialog(self):
        dialog = ShortcutDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            shortcut_path = dialog.get_path()
            self.add_shortcut(shortcut_path)

    def add_shortcut(self, path):
        if os.path.isdir(path):
            item = QStandardItem(path)
            self.files_group.appendRow(item)
        elif os.path.isfile(path):
            item = QStandardItem(path)
            self.applications_group.appendRow(item)

    def scan_for_applications(self):
        applications = self.find_applications()
        dialog = ScanDialog(applications, self.current_stylesheet, self)
        if dialog.exec_() == QDialog.Accepted:
            selected_apps = dialog.get_selected_applications()
            for app in selected_apps:
                self.add_shortcut(app)

    def find_applications(self):
        system = platform.system()
        applications = []

        if system == 'Windows':
            common_dirs = [r"C:\Program Files", r"C:\Program Files (x86)"]
        elif system == 'Darwin':
            common_dirs = ["/Applications"]
        elif system == 'Linux':
            common_dirs = ["/usr/share/applications"]
        else:
            return applications

        # Create a progress dialog
        progress = QProgressDialog("Scanning for applications...", "Cancel", 0, 100, self)
        progress.setWindowModality(Qt.WindowModal)
        progress.setValue(0)

        # Apply the current stylesheet to the progress dialog
        progress.setStyleSheet(self.current_stylesheet)

        # Calculate total files to be scanned
        total_files = 0
        for directory in common_dirs:
            for root, dirs, files in os.walk(directory):
                total_files += len(files)

        files_scanned = 0

        for directory in common_dirs:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if system == 'Windows' and file.endswith(".exe"):
                        applications.append(os.path.join(root, file))
                    elif system == 'Darwin' and file.endswith(".app"):
                        applications.append(os.path.join(root, file))
                    elif system == 'Linux' and file.endswith(".desktop"):
                        applications.append(os.path.join(root, file))

                    files_scanned += 1
                    progress.setValue(int((files_scanned / total_files) * 100))
                    QApplication.processEvents()
                    if progress.wasCanceled():
                        progress.close()
                        return applications  # Return the applications found so far
                if progress.wasCanceled():
                    progress.close()
                    return applications  # Return the applications found so far
            if progress.wasCanceled():
                progress.close()
                return applications  # Return the applications found so far

        progress.setValue(100)
        progress.close()
        return applications

    def apply_theme(self, stylesheet_path):
        self.current_stylesheet = load_stylesheet(stylesheet_path)
        self.setStyleSheet(self.current_stylesheet)
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
