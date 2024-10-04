import os
import shutil
import venv
import subprocess
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QPushButton, QLabel, QInputDialog, QMessageBox, QFileDialog, QListWidgetItem, QStyle, QToolTip
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor

class VenvManagerTab(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        layout = QHBoxLayout()
        self.setLayout(layout)

        self.venv_list = QListWidget()
        layout.addWidget(self.venv_list)

        button_layout = QVBoxLayout()
        layout.addLayout(button_layout)

        self.create_button = QPushButton("Create Venv")
        self.create_button.setIcon(self.style().standardIcon(QStyle.SP_FileDialogNewFolder))
        self.create_button.setToolTip("Create a new virtual environment")
        self.create_button.clicked.connect(self.create_venv)
        button_layout.addWidget(self.create_button)

        self.activate_button = QPushButton("Activate Venv")
        self.activate_button.setIcon(self.style().standardIcon(QStyle.SP_DialogApplyButton))
        self.activate_button.setToolTip("Activate the selected virtual environment")
        self.activate_button.clicked.connect(self.activate_venv)
        button_layout.addWidget(self.activate_button)

        self.delete_button = QPushButton("Delete Venv")
        self.delete_button.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
        self.delete_button.setToolTip("Delete the selected virtual environment")
        self.delete_button.clicked.connect(self.delete_venv)
        button_layout.addWidget(self.delete_button)

        self.refresh_button = QPushButton("Refresh List")
        self.refresh_button.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
        self.refresh_button.setToolTip("Refresh the list of virtual environments")
        self.refresh_button.clicked.connect(self.refresh_venv_list)
        button_layout.addWidget(self.refresh_button)

        self.status_label = QLabel()
        button_layout.addWidget(self.status_label)

        self.venv_dir = self.config.get('General', 'venv_dir')
        self.active_venv = self.config.get('General', 'last_active_venv')
        self.refresh_venv_list()

        self.venv_list.itemEntered.connect(self.show_venv_tooltip)

    def set_venv_dir(self, path):
        self.venv_dir = path
        self.config.set('General', 'venv_dir', path)
        self.refresh_venv_list()

    def get_active_venv_path(self):
        if self.active_venv:
            return os.path.join(self.venv_dir, self.active_venv)
        return None

    def browse_venv_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Venv Directory")
        if dir_path:
            self.set_venv_dir(dir_path)

    def refresh_venv_list(self):
        self.venv_list.clear()
        if not self.venv_dir or not os.path.exists(self.venv_dir):
            return

        for venv_name in os.listdir(self.venv_dir):
            if os.path.isdir(os.path.join(self.venv_dir, venv_name)):
                item = QListWidgetItem(venv_name)
                item.setToolTip("Hover for more information")
                self.venv_list.addItem(item)
                if venv_name == self.active_venv:
                    item.setBackground(Qt.green)
                    item.setForeground(Qt.white)

    def show_venv_tooltip(self, item):
        venv_name = item.text()
        venv_info = self.get_venv_info(venv_name)
        QToolTip.showText(QCursor.pos(), venv_info)

    def get_venv_info(self, venv_name):
        venv_path = os.path.join(self.venv_dir, venv_name)
        python_path = os.path.join(venv_path, "Scripts" if os.name == "nt" else "bin", "python")

        try:
            python_version = subprocess.check_output([python_path, "--version"], text=True).strip()
            installed_packages = subprocess.check_output([python_path, "-m", "pip", "list", "--format=freeze"], text=True).strip()
            package_count = len(installed_packages.split('\n'))

            return f"Python Version: {python_version}\nPackages Installed: {package_count}\nPath: {venv_path}"
        except Exception as e:
            return f"Error getting venv info: {e}"

    def create_venv(self):
        venv_name, ok = QInputDialog.getText(self, "Create Virtual Environment", "Enter venv name:")
        if ok and venv_name:
            venv_path = os.path.join(self.venv_dir, venv_name)
            try:
                venv.create(venv_path, with_pip=True)
                self.status_label.setText(f"Created venv: {venv_name}")
                self.refresh_venv_list()
            except Exception as e:
                self.status_label.setText(f"Error creating venv: {str(e)}")

    def activate_venv(self):
        selected_items = self.venv_list.selectedItems()
        if not selected_items:
            self.status_label.setText("No venv selected")
            return
        venv_name = selected_items[0].text()
        self.active_venv = venv_name
        self.config.set('General', 'last_active_venv', venv_name)
        venv_path = os.path.join(self.venv_dir, venv_name)
        activate_script = os.path.join(venv_path, "Scripts" if os.name == "nt" else "bin", "activate")
        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(f"Virtual environment '{venv_name}' is now active.")
        msg.setInformativeText(f"To activate it in your terminal, run:\nsource {activate_script}")
        msg.setWindowTitle("Virtual Environment Activated")
        
        copy_button = msg.addButton("Copy Command", QMessageBox.ActionRole)
        msg.addButton(QMessageBox.Ok)
        
        msg.exec_()
        
        if msg.clickedButton() == copy_button:
            QApplication.clipboard().setText(f"source {activate_script}")
            self.status_label.setText("Activation command copied to clipboard")
        
        self.refresh_venv_list()

    def delete_venv(self):
        selected_items = self.venv_list.selectedItems()
        if not selected_items:
            self.status_label.setText("No venv selected")
            return
        venv_name = selected_items[0].text()
        venv_path = os.path.join(self.venv_dir, venv_name)
        
        reply = QMessageBox.question(self, 'Delete Virtual Environment', 
                                     f"Are you sure you want to delete the '{venv_name}' environment?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                shutil.rmtree(venv_path)
                self.status_label.setText(f"Deleted venv: {venv_name}")
                if self.active_venv == venv_name:
                    self.active_venv = None
                    self.config.set('General', 'last_active_venv', '')
                self.refresh_venv_list()
            except Exception as e:
                self.status_label.setText(f"Error deleting venv: {str(e)}")
