import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.Qsci import QsciScintilla, QsciLexerPython
from PyQt5.Qsci import QsciScintilla, QsciLexerPython
from PyQt5.QtGui import QColor

from PyQt5.Qsci import QsciScintilla, QsciLexerPython
from PyQt5.QtGui import QColor, QFont

themes = {
    "Dark": {
        "background": "#2b2b2b",
        "foreground": "#ccc",
        "current_line": "#3c3f41",
        "selection": "#214283"
    },
    "Light": {
        "background": "#ffffff",
        "foreground": "#000000",
        "current_line": "#f0f0f0",
        "selection": "#d6d6d6"
    }
}

class CodeEditor(QsciScintilla):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lexer = QsciLexerPython()
        self.setLexer(self.lexer)
        self.setUtf8(True)
        self.setMarginsBackgroundColor(QColor("#333"))
        self.setMarginsForegroundColor(QColor("#CCC"))
        self.setAutoCompletionReplaceWord(True)
        self.setAnnotationDisplay(QsciScintilla.AnnotationAtLineEnd)
        self.setAutoIndent(True)
        self.initUI()
        
    def initUI(self):
        # Initial configurations as previously
        self.setMarginType(1, QsciScintilla.NumberMargin)
        self.setMarginWidth(1, "0000")
        self.setFolding(QsciScintilla.PlainFoldStyle)
        self.setCaretLineVisible(True)
        self.applyTheme("Dark")  # Apply default theme

    def applyTheme(self, theme_name):

        theme = themes[theme_name]
        self.setStyleSheet(f"background-color: {theme['background']}; color: {theme['foreground']};")
        self.setCaretLineBackgroundColor(QColor(theme['current_line']))
        self.setSelectionBackgroundColor(QColor(theme['selection']))

        # Optional: Adjust lexer colors based on theme
        self.lexer.setDefaultPaper(QColor(theme['background']))
        self.lexer.setDefaultColor(QColor(theme['foreground']))


from PyQt5.QtWidgets import QMainWindow, QApplication, QMenu, QAction

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.editor = CodeEditor(self)
        self.setCentralWidget(self.editor)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Python Code Editor with Themes")
        self.resize(800, 600)
        self.createMenus()

    def createMenus(self):
        menuBar = self.menuBar()
        themeMenu = menuBar.addMenu("Themes")
        
        for theme_name in themes.keys():
            action = QAction(theme_name, self)
            action.triggered.connect(lambda checked, name=theme_name: self.editor.applyTheme(name))
            themeMenu.addAction(action)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

