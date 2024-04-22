import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from V.M.syntaxHighlighter import PythonSyntaxHighlighter
from V.M.autoCompleter import AutoCompleterCodeEditor
from pygments.styles import STYLE_MAP
from V.panel import Panel

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
    
    
    QHBoxLayout{
        color: white;
        padding: 0;
        margin: 0;
        text-align: center;
        background-color: red;
    }

    QTabBar::tab:!selected {
        color: white;
        background-color: rgb(30,30,30);
        border-radius: 0px;
        spacing: 10px;
        padding: 10px;
        padding-top: 0px;
    }

    QTabBar::tab:!selected:hover {
        border-top: 1px double rgb(0, 204, 255);
        color: white;
        background-color: transparent;
        border-radius: 0px;
        spacing: 10px;
        padding: 10px;
        padding-top: 0px;
        }

    QTabBar::tab:selected {
        border-top: 1px double rgb(0, 204, 255);
        color: white;
        background-color: transparent;
        border-radius: 0px;
        spacing: 10px;
        padding: 10px;
        padding-top: 0px;
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
        self.text_edit_left = AutoCompleterCodeEditor()
        self.highlighter = PythonSyntaxHighlighter(self.text_edit_left.document())
        self.text_edit_left.setStyleSheet("background-color: rgb(30,30,30); color: #f0f0f0;")
        self.text_edit_left.setMinimumWidth(1 * self.width())
        self.text_edit_left.setMinimumHeight(1 * self.height())

        middle_hbox_layout.addWidget(self.text_edit_left)

        text_edit_right = QTextEdit()
        text_edit_right.setPlaceholderText("Texte en lecture seule")
        text_edit_right.setMaximumWidth(1 * self.width())
        text_edit_right.setReadOnly(True)
        middle_hbox_layout.addWidget(text_edit_right,0)

        middle_vbox_layout.addLayout(middle_hbox_layout)
        
        self.panel = Panel()
        self.panel.setStyleSheet(u"border: none;")
        self.panel.setAutoFillBackground(True)
        self.panel.setContentsMargins(5,5,0,0)

        middle_vbox_layout.addWidget(self.panel,0,Qt.AlignBottom)
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
        self.statusBar()
        self.createActions()
        self.createMenus()
        
    def createActions(self):
        self.openAction = QAction('Open', self)
        self.openAction.triggered.connect(self.openFile)

        self.saveAction = QAction('Save', self)
        self.saveAction.triggered.connect(self.saveFile)

        # Add more actions here

    def createMenus(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)

        themeMenu = menubar.addMenu('Themes')
        themes = list(STYLE_MAP.keys())  # Ajouter tous les thèmes disponibles
        for style in sorted(themes):  # Trier les thèmes pour une meilleure organisation
            themeAction = QAction(style, self)
            themeAction.triggered.connect(lambda checked, s=style: self.changeTheme(s))
            themeMenu.addAction(themeAction)


    def changeTheme(self, style_name):
        self.highlighter.setupStyles(style_name)
        self.text_edit_left.document().setModified(True)
        self.text_edit_left.document().setDefaultFont(QFont("Consolas", 12))
        self.text_edit_left.setStyleSheet("color: #f0f0f0;")
        self.highlighter.rehighlight()



    def openFile(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'Python Files (*.py)')
        if filename:
            with open(filename, 'r', encoding='utf-8') as file:
                self.text_edit_left.setPlainText(file.read())

    def saveFile(self):
        filename, _ = QFileDialog.getSaveFileName(self, 'Save File', '', 'Python Files (*.py)')
        if filename:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(self.text_edit_left.toPlainText())



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
