from PyQt5.QtWidgets import QWidget, QTabWidget, QListWidget, QHBoxLayout, QLayout

class Panel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUI()

    def setupUI(self):
        layout = QHBoxLayout(self)  # Set the main layout for the Panel
        self.setStyleSheet(u"border: none;background-color: transparent;")
        # Create the QTabWidget
        middle_tab_widget_bottom = QTabWidget()
        layout.addWidget(middle_tab_widget_bottom)  # Add the tab widget to the main layout

        # Define the tabs and their contents
        tabs_info = {
            "PROBLEMES": ["PROBLEME 1", "PROBLEME 2", "PROBLEME 3"],
            "SORTIE": ["SORTIE 1", "SORTIE 2", "SORTIE 3"],
            "CONSOLE DEB": ["CONSOLE 1", "CONSOLE 2", "CONSOLE 3"],
            "TERMINAL": ["CONSOLE 1", "CONSOLE 2", "CONSOLE 3"],
            "PORTS": ["PORTS 1", "PORTS 2", "PORTS 3"],
            "CODE REF": ["PORTS 1", "PORTS 2", "PORTS 3"],
            "SQL CONS": ["PORTS 1", "PORTS 2", "PORTS 3"],
            "LIGHTRUN": ["PORTS 1", "PORTS 2", "PORTS 3"],
            "COMMENTAIRES": ["PORTS 1", "PORTS 2", "PORTS 3"],
            "SEARCH ERROR": ["PORTS 1", "PORTS 2", "PORTS 3"]
        }

        # Add tabs dynamically based on the tabs_info dictionary
        for tab_name, items in tabs_info.items():
            tab = QListWidget()
            tab.addItems(items)
            middle_tab_widget_bottom.addTab(tab, tab_name)

        self.setLayout(layout)  # Set the layout for this widget
