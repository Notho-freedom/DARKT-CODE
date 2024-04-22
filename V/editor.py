from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from M.syntaxHighlighter import PythonSyntaxHighlighter
from M.autoCompleter import AutoCompleterCodeEditor
from pygments.styles import STYLE_MAP

class Editor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.textEdit = AutoCompleterCodeEditor()
        self.highlighter = PythonSyntaxHighlighter(self.textEdit.document())
        self.textEdit.setStyleSheet("background-color: #2b2b2b; color: #f0f0f0;")
        self.setCentralWidget(self.textEdit)
        self.statusBar()
        self.createActions()
        self.createMenus()
        self.setWindowTitle('Python Code Editor')
        self.setGeometry(300, 300, 800, 600)
        self.textEdit.installEventFilter(self)

    def eventFilter(self, source, event):
        if (event.type() == event.KeyPress and source is self.textEdit):
            if event.key() == Qt.Key_Return:
                return True  # Ignore further processing to avoid double new lines
        return super(Editor, self).eventFilter(source, event)
    
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
        self.textEdit.document().setModified(True)
        self.textEdit.document().setDefaultFont(QFont("Consolas", 12))
        self.textEdit.setStyleSheet("background-color: black; color: #f0f0f0;")
        self.highlighter.rehighlight()



    def openFile(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'Python Files (*.py)')
        if filename:
            with open(filename, 'r', encoding='utf-8') as file:
                self.textEdit.setPlainText(file.read())

    def saveFile(self):
        filename, _ = QFileDialog.getSaveFileName(self, 'Save File', '', 'Python Files (*.py)')
        if filename:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(self.textEdit.toPlainText())

# Add more class methods here
from PyQt5.Qsci import QsciScintilla, QsciLexerPython

class CodeEditor(QsciScintilla):
    def __init__(self, parent=None):
        super().__init__(parent)
        lexer = QsciLexerPython()
        self.setLexer(lexer)
        self.setUtf8(True)
        self.setMarginType(1, QsciScintilla.NumberMargin)
