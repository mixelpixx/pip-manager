import sys
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
    window = PipPackageManager()
    window.show()
    sys.exit(app.exec_())