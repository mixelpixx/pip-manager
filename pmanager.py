import sys
import os
import subprocess
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
        self.package_list.clear()
        venv_path = self.venv_manager.get_active_venv_path()
        if venv_path:
            pip_path = os.path.join(venv_path, "Scripts" if sys.platform == "win32" else "bin", "pip")
            try:
                result = subprocess.run([pip_path, "list", "--format=freeze"], capture_output=True, text=True, check=True)
                packages = result.stdout.strip().split('\n')
                for package in packages:
                    self.package_list.addItem(package)
            except subprocess.CalledProcessError as e:
                self.status_label.setText(f"Error: {e}")
        else:
            try:
                result = subprocess.run([sys.executable, "-m", "pip", "list", "--format=freeze"], capture_output=True, text=True, check=True)
                packages = result.stdout.strip().split('\n')
                for package in packages:
                    self.package_list.addItem(package)
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
        self.create_button.clicked.connect(self.create_venv)
        button_layout.addWidget(self.create_button)

        self.activate_button = QPushButton("Activate Venv")
        self.activate_button.setIcon(self.style().standardIcon(QStyle.SP_DialogApplyButton))
        self.activate_button.clicked.connect(self.activate_venv)
        button_layout.addWidget(self.activate_button)

        self.delete_button = QPushButton("Delete Venv")
        self.delete_button.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
        self.delete_button.clicked.connect(self.delete_venv)
        button_layout.addWidget(self.delete_button)

        self.refresh_button = QPushButton("Refresh List")
        self.refresh_button.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
        self.refresh_button.clicked.connect(self.refresh_venv_list)
        button_layout.addWidget(self.refresh_button)

        self.status_label = QLabel()
        button_layout.addWidget(self.status_label)

        self.venv_dir = self.config.get('General', 'venv_dir')
        self.active_venv = self.config.get('General', 'last_active_venv')
        self.refresh_venv_list()

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
                self.venv_list.addItem(item)
                venv_info = self.get_venv_info(venv_name)
                item.setToolTip(venv_info)
                if venv_name == self.active_venv:
                    item.setBackground(Qt.yellow)

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
        activate_script = os.path.join(venv_path, "Scripts" if sys.platform == "win32" else "bin", "activate")
        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText(f"Virtual environment '{venv_name}' is now active.")
        msg.setInformativeText(f"To activate it in your terminal, run:\nsource {activate_script}")
        msg.setWindowTitle("Virtual Environment Activated")
        msg.exec()
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
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            try:
                import shutil
                shutil.rmtree(venv_path)
                self.status_label.setText(f"Deleted venv: {venv_name}")
                if self.active_venv == venv_name:
                    self.active_venv = None
                    self.config.set('General', 'last_active_venv', '')
                self.refresh_venv_list()
            except Exception as e:
                self.status_label.setText(f"Error deleting venv: {str(e)}")

    def get_venv_info(self, venv_name):
        venv_path = os.path.join(self.venv_dir, venv_name)
        python_path = os.path.join(venv_path, "Scripts" if sys.platform == "win32" else "bin", "python")

        try:
            python_version = subprocess.check_output([python_path, "--version"], text=True).strip()
            installed_packages = subprocess.check_output([python_path, "-m", "pip", "list", "--format=freeze"], text=True).strip()

            return f"Python Version: {python_version}\nInstalled Packages:\n{installed_packages}"
        except Exception as e:
            return f"Error getting venv info: {e}"

class PipPackageManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python Environment Manager")
        self.setGeometry(100, 100, 800, 600)

        self.config = Config()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Create tab widget
        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)

        self.venv_manager = VenvManagerTab(self.config)

        # Create and add tabs
        package_manager_tab = PackageManagerTab(self.venv_manager, self.config)
        venv_manager_tab = self.venv_manager

        tab_widget.addTab(package_manager_tab, "Package Manager")
        tab_widget.addTab(venv_manager_tab, "Venv Manager")

        # Add browse button
        browse_button = QPushButton("Browse")
        browse_button.setIcon(self.style().standardIcon(QStyle.SP_DirIcon))
        browse_button.clicked.connect(self.venv_manager.browse_venv_dir)
        self.venv_manager.layout().addWidget(browse_button)

        # Set the style
        self.set_style()

    def set_style(self):
        # Set a custom font
        font = QFont("Segoe UI", 10)
        QApplication.setFont(font)

        # Set the dark theme style sheet
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QPushButton {
                background-color: #3d3d3d;
                border: 1px solid #555555;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #4d4d4d;
            }
            QListWidget {
                background-color: #363636;
                border: 1px solid #555555;
                border-radius: 3px;
            }
            QTabWidget::pane {
                border: 1px solid #555555;
                border-radius: 3px;
            }
            QTabBar::tab {
                background-color: #3d3d3d;
                border: 1px solid #555555;
                padding: 5px;
                border-top-left-radius: 3px;
                border-top-right-radius: 3px;
            }
            QTabBar::tab:selected {
                background-color: #4d4d4d;
            }
            QLabel {
                color: #cccccc;
            }
        """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PipPackageManager()
    window.show()
    sys.exit(app.exec_())