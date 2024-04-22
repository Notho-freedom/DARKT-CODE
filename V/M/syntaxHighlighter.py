import json
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.styles import *
from pygments.token import Token


class PythonSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.background_color = QColor('#2b2b2b')  # Définir une couleur par défaut claire
        self.styles = {}
        self.setupStyles()

    def setupStyles(self, style_name='monokai'):
        self.styles = {}
        style = get_style_by_name(style_name)
        for token, style_opts in style:
            fmt = QTextCharFormat()
            if 'color' in style_opts and style_opts['color']:
                fmt.setForeground(QColor(f'#{style_opts["color"]}'))
            if 'bgcolor' in style_opts and style_opts['bgcolor']:
                fmt.setBackground(QColor(f'#{style_opts["bgcolor"]}'))
                if token is Token.Text.Whitespace or token is Token:  # Assurer l'application de la couleur de fond
                    self.background_color = QColor(f'#{style_opts["bgcolor"]}')
            if 'bold' in style_opts and style_opts['bold']:
                fmt.setFontWeight(QFont.Bold)
            if 'italic' in style_opts and style_opts['italic']:
                fmt.setFontItalic(True)
            self.styles[token] = fmt


    def highlightBlock(self, text):
        """Applique la coloration syntaxique pour chaque bloc de texte."""
        # Position actuelle dans le texte
        current_pos = 0

        # Tokenisation du texte avec Pygments et PythonLexer
        tokens = lex(text, PythonLexer())
        for token_type, value in tokens:
            length = len(value)
            fmt = self.styles.get(token_type, QTextCharFormat())
            self.setFormat(current_pos, length, fmt)
            current_pos += length
