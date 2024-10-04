        selected_rows = self.package_table.selectionModel().selectedRows()
        if not selected_rows:
            self.status_label.setText("No package selected")
            return
        package = self.package_table.item(selected_rows[0].row(), 0).text()
        
        reply = QMessageBox.question(self, 'Uninstall Package', 
                                     f"Are you sure you want to uninstall '{package}'?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
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
        selected_rows = self.package_table.selectionModel().selectedRows()
        if not selected_rows:
            self.status_label.setText("No package selected")
            return
        package = self.package_table.item(selected_rows[0].row(), 0).text()
        
        reply = QMessageBox.question(self, 'Uninstall Package', 
                                     f"Are you sure you want to uninstall '{package}'?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
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

    def update_package(self):
        selected_rows = self.package_table.selectionModel().selectedRows()
        if not selected_rows:
            self.status_label.setText("No package selected")
            return
        package = self.package_table.item(selected_rows[0].row(), 0).text()
        
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
