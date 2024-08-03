from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QFileDialog, QLineEdit, QDialogButtonBox


class ShortcutDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Add Shortcut')
        self.setGeometry(300, 300, 400, 200)

        layout = QVBoxLayout()

        self.path_label = QLabel("Select folder or application:")
        layout.addWidget(self.path_label)

        self.path_input = QLineEdit(self)
        layout.addWidget(self.path_input)

        self.browse_button = QPushButton("Browse...")
        self.browse_button.clicked.connect(self.browse)
        layout.addWidget(self.browse_button)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def browse(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.AnyFile)
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            self.path_input.setText(file_path)

    def get_path(self):
        return self.path_input.text()
