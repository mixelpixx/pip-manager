import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from pmanager import PackageManagerTab
from vmanager import VenvManagerTab
import configparser

class PipPackageManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pip Package Manager")
        self.setGeometry(100, 100, 800, 600)

        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)

        self.venv_manager = VenvManagerTab(self.config)
        self.package_manager = PackageManagerTab(self.venv_manager)

        tab_widget.addTab(self.venv_manager, "Virtual Environments")
        tab_widget.addTab(self.package_manager, "Packages")

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
            QTableWidget {
                background-color: #363636;
                border: 1px solid #555555;
                border-radius: 3px;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #2b2b2b;
                padding: 5px;
                border: 1px solid #555555;
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
        app.setStyle("Fusion")  # Use Fusion style for a more modern look
        window = PipPackageManager()
        window.show()
        sys.exit(app.exec_())