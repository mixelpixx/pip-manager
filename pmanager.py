import sys
import os
import subprocess
import shutil
import venv
import configparser
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QListWidget, QPushButton, QLabel, QTabWidget, QInputDialog, 
                             QMessageBox, QFileDialog, QListWidgetItem, QStyle)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

import logging
logging.basicConfig(filename='pmanager_debug.log', level=logging.DEBUG)
logging.debug("Program started")

CONFIG_FILE = 'settings.ini'

class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config_file = CONFIG_FILE
        self.load()

    def load(self):
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)
        else:
            self.set_defaults()

    def save(self):
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    def set_defaults(self):
        self.config['General'] = {
            'venv_dir': os.path.join(os.path.expanduser("~"), "venvs"),
            'last_active_venv': ''
        }
        self.save()

    def get(self, section, key, fallback=None):
        return self.config.get(section, key, fallback=fallback)

    def set(self, section, key, value):
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, value)
        self.save()

class PackageManagerTab(QWidget):
    def __init__(self, venv_manager, config):
        super().__init__()
        self.venv_manager = venv_manager
        self.config = config
        layout = QHBoxLayout()
        self.setLayout(layout)

        # Package list
        self.package_list = QListWidget()
        layout.addWidget(self.package_list)

        # Buttons
        button_layout = QVBoxLayout()
        layout.addLayout(button_layout)

        self.update_button = QPushButton("Update")
        self.update_button.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
        self.update_button.clicked.connect(self.update_package)
        button_layout.addWidget(self.update_button)

        self.uninstall_button = QPushButton("Uninstall")
        self.uninstall_button.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
        self.uninstall_button.clicked.connect(self.uninstall_package)
        button_layout.addWidget(self.uninstall_button)

        self.install_button = QPushButton("Install")
        self.install_button.setIcon(self.style().standardIcon(QStyle.SP_FileIcon))
        self.install_button.clicked.connect(self.install_package)
        button_layout.addWidget(self.install_button)

        self.refresh_button = QPushButton("Refresh List")
        self.refresh_button.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
        self.refresh_button.clicked.connect(self.refresh_package_list)
        button_layout.addWidget(self.refresh_button)

        self.status_label = QLabel()
        button_layout.addWidget(self.status_label)

        self.refresh_package_list()

    def refresh_package_list(self):
        logging.debug("Refreshing package list")
        self.package_list.clear()
        venv_path = self.venv_manager.get_active_venv_path()
        if venv_path:
            pip_path = os.path.join(venv_path, "Scripts" if sys.platform == "win32" else "bin", "pip")
            try:
                result = subprocess.run([pip_path, "list", "--format=freeze"], capture_output=True, text=True, check=True)
                packages = result.stdout.strip().split('\n')
                for package in packages:
                    self.package_list.addItem(package)
                logging.debug(f"Packages in venv {venv_path}: {packages}")
            except subprocess.CalledProcessError as e:
                self.status_label.setText(f"Error: {e}")
        else:
            try:
                result = subprocess.run([sys.executable, "-m", "pip", "list", "--format=freeze"], capture_output=True, text=True, check=True)
                packages = result.stdout.strip().split('\n')
                for package in packages:
                    self.package_list.addItem(package)
                logging.debug(f"Global packages: {packages}")
            except subprocess.CalledProcessError as e:
                self.status_label.setText(f"Error: {e}")

    def update_package(self):
        selected_items = self.package_list.selectedItems()
        if not selected_items:
            self.status_label.setText("No package selected")
            return
        package = selected_items[0].text().split('==')[0]
        try:
            venv_path = self.venv_manager.get_active_venv_path()
            if venv_path:
                pip_path = os.path.join(venv_path, "Scripts" if sys.platform == "win32" else "bin", "pip")
                subprocess.run([pip_path, "install", "--upgrade", package], check=True)
            else:
                subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", package], check=True)
            self.status_label.setText(f"Updated {package}")
            self.refresh_package_list()
        except subprocess.CalledProcessError as e:
            self.status_label.setText(f"Error updating {package}: {e}")

    def uninstall_package(self):
        selected_items = self.package_list.selectedItems()
        if not selected_items:
            self.status_label.setText("No package selected")
            return
        package = selected_items[0].text().split('==')[0]
        try:
            venv_path = self.venv_manager.get_active_venv_path()
            if venv_path:
                pip_path = os.path.join(venv_path, "Scripts" if sys.platform == "win32" else "bin", "pip")
                subprocess.run([pip_path, "uninstall", "-y", package], check=True)
            else:
                subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", package], check=True)
            self.status_label.setText(f"Uninstalled {package}")
            self.refresh_package_list()
        except subprocess.CalledProcessError as e:
            self.status_label.setText(f"Error uninstalling {package}: {e}")

    def install_package(self):
        package, ok = QInputDialog.getText(self, "Install Package", "Enter package name:")
        if ok and package:
            try:
                venv_path = self.venv_manager.get_active_venv_path()
                if venv_path:
                    pip_path = os.path.join(venv_path, "Scripts" if sys.platform == "win32" else "bin", "pip")
                    subprocess.run([pip_path, "install", package], check=True)
                else:
                    subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
                self.status_label.setText(f"Installed {package}")
                self.refresh_package_list()
            except subprocess.CalledProcessError as e:
                self.status_label.setText(f"Error installing {package}: {e}")
