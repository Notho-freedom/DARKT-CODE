from PyQt5.QtWidgets import QWidget, QTabWidget, QHBoxLayout, QTextEdit
from PyQt5.QtCore import Qt, QEvent
from C.terminalManagement import *

class Panel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUI()

    def setupUI(self):
        layout = QHBoxLayout(self)  # Set the main layout for the Panel
        self.setStyleSheet(u"border: none;background-color: transparent;")
        # Create the QTabWidget
        self.middle_tab_widget_bottom = QTabWidget()
        layout.addWidget(self.middle_tab_widget_bottom)  # Add the tab widget to the main layout

        # Define the tabs and their contents
        tabs_info = {
            "PROBLEMES": ["PROBLEME 1", "PROBLEME 2", "PROBLEME 3"],
            "SORTIE": ["SORTIE 1", "SORTIE 2", "SORTIE 3"],
            "CONSOLE DEB": ["CONSOLE 1", "CONSOLE 2", "CONSOLE 3"],
            "TERMINAL": ["CONSOLE 1", "CONSOLE 2", "CONSOLE 3"],  # Terminal
            "PORTS": ["PORTS 1", "PORTS 2", "PORTS 3"],
            "CODE REF": ["PORTS 1", "PORTS 2", "PORTS 3"],
            "SQL CONS": ["PORTS 1", "PORTS 2", "PORTS 3"],
            "LIGHTRUN": ["PORTS 1", "PORTS 2", "PORTS 3"],
            "COMMENTAIRES": ["PORTS 1", "PORTS 2", "PORTS 3"],
            "SEARCH ERROR": ["PORTS 1", "PORTS 2", "PORTS 3"]
        }

        # Add tabs dynamically based on the tabs_info dictionary
        for tab_name, items in tabs_info.items():
            if tab_name == "TERMINAL":  # Replace terminal tab with QTextEdit
                self.terminal_text_edit = QTextEdit()
                self.middle_tab_widget_bottom.addTab(self.terminal_text_edit, tab_name)
                self.terminal_text_edit.installEventFilter(self)  # Install event filter for QTextEdit# Install event filter for QTextEdit# Install event filter for QTextEdit
            else:
                tab = QTextEdit()
                tab.append("\n".join(items))
                self.middle_tab_widget_bottom.addTab(tab, tab_name)

        self.setLayout(layout)  # Set the layout for this widget
    
    def eventFilter(self, obj, event):
        if obj == self.terminal_text_edit and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Return:
                # Capture "Enter" key press event
                commande = self.terminal_text_edit.toPlainText().strip()
                default_directory = "C:/Users/SEVERIN/Desktop/ravel/1.2/"
                result = new_cmd_commande(default_directory,commande)
                self.write_to_terminal(result)
                # print("Text entered in terminal:", text)  
        return super().eventFilter(obj, event)

    def write_to_terminal(self, text):
        self.terminal_text_edit.append(text)
