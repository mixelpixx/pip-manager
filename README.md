# Python Package Manager with Virtual Environment Support

This project is a graphical user interface (GUI) application for managing Python packages and virtual environments. It provides an easy-to-use interface for creating, activating, and deleting virtual environments, as well as installing, uninstalling, and updating Python packages within these environments.

## Features


## Requirements


## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/python-package-manager.git
   cd python-package-manager
   ```

2. Install the required dependencies:
   ```
   pip install PyQt5
   ```

## Usage

Run the application by executing the `gui.py` file:

python gui.py

### Virtual Environment Management

- Click "Create Venv" to create a new virtual environment
- Select a virtual environment and click "Activate Venv" to set it as the active environment
- Click "Delete Venv" to remove a virtual environment
- Use "Refresh List" to update the list of virtual environments

### Package Management

- The package list shows installed packages in the active virtual environment
- Click "Install Package" to add a new package
- Select a package and click "Uninstall Package" to remove it
- Use "Refresh List" to update the list of installed packages

## Project Structure

- `gui.py`: Main application file containing the GUI setup and styling
- `package_icons.py`: Handles package icons for common Python packages
- `pmanager.py`: Manages package installation, uninstallation, and listing
- `vmanager.py`: Handles virtual environment creation, activation, and deletion

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).
