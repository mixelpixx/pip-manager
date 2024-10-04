import sys
import os
import subprocess
import json
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLabel, QInputDialog, QMessageBox
from PyQt5.QtCore import Qt
from package_icons import get_package_icon

class PackageManagerTab(QWidget):
    def __init__(self, venv_manager):
        super().__init__()
        self.venv_manager = venv_manager
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.package_table = QTableWidget()
        self.package_table.setColumnCount(3)
        self.package_table.setHorizontalHeaderLabels(["Package", "Version", "Description"])
        self.package_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.package_table)

        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        self.install_button = QPushButton("Install Package")
        self.install_button.clicked.connect(self.install_package)
        button_layout.addWidget(self.install_button)

        self.uninstall_button = QPushButton("Uninstall Package")
        self.uninstall_button.clicked.connect(self.uninstall_package)
        button_layout.addWidget(self.uninstall_button)

        self.refresh_button = QPushButton("Refresh List")
        self.refresh_button.clicked.connect(self.refresh_package_list)
        button_layout.addWidget(self.refresh_button)

        self.status_label = QLabel()
        layout.addWidget(self.status_label)

        self.refresh_package_list()

    def refresh_package_list(self):
        self.package_table.setRowCount(0)
        try:
            venv_path = self.venv_manager.get_active_venv_path()
            if venv_path:
                pip_path = os.path.join(venv_path, "Scripts" if sys.platform == "win32" else "bin", "pip")
                result = subprocess.run([pip_path, "list", "--format=json"], capture_output=True, text=True, check=True)
            else:
                result = subprocess.run([sys.executable, "-m", "pip", "list", "--format=json"], capture_output=True, text=True, check=True)
            packages = json.loads(result.stdout)
            self.package_table.setRowCount(len(packages))
            for row, package in enumerate(packages):
                name_item = QTableWidgetItem(package['name'])
                name_item.setIcon(get_package_icon(package['name']))
                self.package_table.setItem(row, 0, name_item)
                self.package_table.setItem(row, 1, QTableWidgetItem(package['version']))
                # You might want to add a description column here if available
            self.package_table.resizeColumnsToContents()
            self.status_label.setText("Package list refreshed")
        except subprocess.CalledProcessError as e:
            self.status_label.setText(f"Error refreshing package list: {e}")

    def uninstall_package(self):