import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from V.test2 import AutoCompleterCodeEditor
from V.vstheme import SyntaxHighlighter

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DARKT Code")
        self.setGeometry(800, 600, 1000, 800)
        qcss=u"""
    * {
        color: white;
        padding: 0;
        margin: 0;
        border-radius: 5px;
        text-align: center;
        border: 1px solid rgb(0, 204, 255);
        background-color: rgb(30,30,30);
    }

    QTabBar::tab:!selected {
        color: white;
        background-color: rgb(30,30,30)
    }

    QTabBar::tab:!selected:hover {
        border-top: 1px double rgb(0, 204, 255);
        color: white;
        background-color: transparent;}

    QTabBar::tab:selected {
        border-top: 1px double rgb(0, 204, 255);
        color: white;
        background-color: transparent;
    }
        """
        self.setStyleSheet(qcss)

        # Création des layouts
        layout = QVBoxLayout()
        header_layout = QHBoxLayout()
        middle_layout = QHBoxLayout()
        footer_layout = QHBoxLayout()
        footer_layout.setAlignment(Qt.AlignBottom)
        footer_layout.setContentsMargins(0, 0, 0, 0)

        # Header
        header_label = QLabel("Header")
        header_layout.addWidget(header_label)
        layout.addLayout(header_layout)

        # Middle
        middle_tab_widget = QTabWidget()
        middle_tab_widget.setTabPosition(QTabWidget.West)
        for i in range(6):
            tab = QListWidget()
            tab.addItems(["Athena","Speedy","Main.py"])
            middle_tab_widget.addTab(tab, f"Onglet {i+1}")

        middle_vbox_layout = QVBoxLayout()

        middle_hbox_layout = QHBoxLayout()
        text_edit_left = AutoCompleterCodeEditor()
        text_edit_left.setPlaceholderText("Texte éditable")
        text_edit_left.setMinimumWidth(0.85 * self.width())
        text_edit_left.setMinimumHeight(0.5 * self.height())

        middle_hbox_layout.addWidget(text_edit_left)

        text_edit_right = QTextEdit()
        text_edit_right.setPlaceholderText("Texte en lecture seule")
        text_edit_right.setMaximumWidth(0.15 * self.width())
        text_edit_right.setReadOnly(True)
        middle_hbox_layout.addWidget(text_edit_right,0)

        middle_vbox_layout.addLayout(middle_hbox_layout)
        
        
        middle_tab_widget_bottom = QTabWidget()
         #tab1
        tab = QListWidget()
        tab.addItems(["PROBLEME 1","PROBLEME 2","PROBLEME 3"])
        middle_tab_widget_bottom.addTab(tab,"PROBLEMES")
        
        #tab2
        tab = QListWidget()
        tab.addItems(["SORTIE 1","SORTIE 2","SORTIE 3"])
        middle_tab_widget_bottom.addTab(tab,"SORTIE")

        #tab3
        tab = QListWidget()
        tab.addItems(["CONSOLE 1","CONSOLE 2","CONSOLE 3"])
        middle_tab_widget_bottom.addTab(tab,"CONSOLE DEB")

        #tab4
        tab = QListWidget()
        tab.addItems(["CONSOLE 1","CONSOLE 2","CONSOLE 3"])
        middle_tab_widget_bottom.addTab(tab,"TERMINAL")

        #tab5
        tab = QListWidget()
        tab.addItems(["PORTS 1","PORTS 2","PORTS 3"])
        middle_tab_widget_bottom.addTab(tab,"PORTS")

        #tab6
        tab = QListWidget()
        tab.addItems(["PORTS 1","PORTS 2","PORTS 3"])
        middle_tab_widget_bottom.addTab(tab,"CODE REF")

        #tab7
        tab = QListWidget()
        tab.addItems(["PORTS 1","PORTS 2","PORTS 3"])
        middle_tab_widget_bottom.addTab(tab,"SQL CONS")

        #tab8
        tab = QListWidget()
        tab.addItems(["PORTS 1","PORTS 2","PORTS 3"])
        middle_tab_widget_bottom.addTab(tab,"LIGHTRUN")

        #tab9
        tab = QListWidget()
        tab.addItems(["PORTS 1","PORTS 2","PORTS 3"])
        middle_tab_widget_bottom.addTab(tab,"COMMENTAIRES")

        #tab10
        tab = QListWidget()
        tab.addItems(["PORTS 1","PORTS 2","PORTS 3"])
        middle_tab_widget_bottom.addTab(tab,"SEARCH ERROR")
        
        middle_vbox_layout.addWidget(middle_tab_widget_bottom,0,Qt.AlignBottom)
        middle_layout.addWidget(middle_tab_widget,0,Qt.AlignLeft)
        middle_layout.addLayout(middle_vbox_layout)
        layout.addLayout(middle_layout)

        # Footer
        footer_rmb = QPushButton("><")
        footer_rmb.setStyleSheet("background-color: transparent;border: none;border-radius: 0px;font-size: 10px;color: white;")
        footer_layout.addWidget(footer_rmb,0,Qt.AlignLeft)
        
        footer_frame = QFrame()
        footer_frame.setStyleSheet("background-color: transparent;border: none;border-radius: 0px;font-size: 10px;color: white;")
        footer_layout.addWidget(footer_frame,0,Qt.AlignLeft)
        
        layout.addLayout(footer_layout,0)

        # Widget central
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
