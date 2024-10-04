import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QPushButton, QStyle
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from pmanager import PackageManagerTab, Config
from vmanager import VenvManagerTab

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