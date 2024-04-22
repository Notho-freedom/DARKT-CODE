import sys
import json
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, text_widget):
        super().__init__(text_widget.document())
        self.text_widget = text_widget
        
        # Styles
        self.styles = {
            'keyword': QTextCharFormat(),
            'operator': QTextCharFormat(),
            'brace': QTextCharFormat(),
            'defclass': QTextCharFormat(),
            'string': QTextCharFormat(),
            'string2': QTextCharFormat(),
            'comment': QTextCharFormat(),
            'self': QTextCharFormat(),
            'numbers': QTextCharFormat(),
        }
        
        # Configure styles
        self.configure_styles()
        
        # Highlight rules
        self.rules = [
            (r'\bdef\b|\bclass\b|\bimport\b|\bfrom\b|\bas\b|\breturn\b|\bif\b|\belse\b|\btry\b|\bexcept\b|\bfinally\b|\bwhile\b|\bfor\b|\bin\b|\bis\b|\band\b|\bor\b|\bnot\b', self.styles['keyword']),
            (r'"[^"\\]*(\\.[^"\\]*)*"', self.styles['string']),
            (r"'[^'\\]*(\\.[^'\\]*)*'", self.styles['string2']),
            (r'\b\d+\b', self.styles['numbers']),
            (r'\#.*', self.styles['comment']),
            (r'\bself\b', self.styles['self']),
            (r'\b__init__\b|\b__name__\b', self.styles['defclass']),
            (r'[{}()\[\]]', self.styles['brace']),
            (r'[.,;:+-/*=<>%]', self.styles['operator']),
        ]

    def configure_styles(self):
        base_font = QFont('Consolas', 12)
        for style in self.styles.values():
            style.setFont(base_font)
        
        self.styles['keyword'].setForeground(QColor('#FF007F'))
        self.styles['operator'].setForeground(QColor('#D60093'))
        self.styles['brace'].setForeground(QColor('#0000FF'))
        self.styles['defclass'].setForeground(QColor('#0000FF'))
        self.styles['string'].setForeground(QColor('#008000'))
        self.styles['string2'].setForeground(QColor('#008000'))
        self.styles['comment'].setForeground(QColor('#800000'))
        self.styles['self'].setForeground(QColor('#FF8000'))
        self.styles['numbers'].setForeground(QColor('#FF0000'))

    def highlightBlock(self, text):
        for pattern, fmt in self.rules:
            expression = QRegularExpression(pattern)
            matchIterator = expression.globalMatch(text)
            while matchIterator.hasNext():
                match = matchIterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)





from PyQt5.QtWidgets import QApplication, QMainWindow, QPlainTextEdit, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuration de la fenêtre principale
        self.setWindowTitle("Python Code Editor")
        self.setGeometry(100, 100, 800, 600)

        # Widget central et layout
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Éditeur de texte
        self.editor = QPlainTextEdit()
        layout.addWidget(self.editor)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Appliquer la coloration syntaxique
        self.highlighter = PythonHighlighter(self.editor)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
