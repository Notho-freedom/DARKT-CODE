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



class AutoCompleterCodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.setFont(QFont("Helvetica", 10))
        self.keywords = self.loadKeywordsFromFile("Athena\speedy\V\keywords.json")
        self.highlighter = PythonSyntaxHighlighter(self.document())
        self.completer = QCompleter()
        self.model = QStringListModel(self.keywords)
        self.completer.setModel(self.model)
        self.completer.setWidget(self)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.setFilterMode(Qt.MatchContains)
        self.completer.activated.connect(self.insertCompletion)

    def insertCompletion(self, text):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.StartOfWord, QTextCursor.KeepAnchor)
        cursor.removeSelectedText()
        cursor.insertText(text)

    def keyPressEvent(self, event):
        if self.completer.popup().isVisible():
            if event.key() in (Qt.Key_Enter, Qt.Key_Return):
                event.ignore()
                completion = self.completer.currentCompletion()
                if completion:
                    self.insertCompletion(completion)
                return
            elif event.key() in (Qt.Key_Escape, Qt.Key_Tab, Qt.Key_Backtab):
                self.completer.popup().hide()
                return

        super().keyPressEvent(event)

        cursor_pos = self.cursorRect().bottomRight()
        cursor_pos.setY(cursor_pos.y() + 2)

        # Coloration des lettres concordantes dans les suggestions d'autocomplétion
        completion_prefix = self.textUnderCursor()
        if len(completion_prefix) < 1:
            self.completer.popup().hide()
            return

        # Filtrer les suggestions qui correspondent au préfixe
        filtered_keywords = [word for group, words in self.keywords.items() for word in words if self.matchPercentage(completion_prefix, word) >= 0.8]

        # Créer un format de texte pour les lettres concordantes
        match_format = QTextCharFormat()
        match_format.setForeground(QColor(255, 165, 0))  # Couleur orange pour les lettres concordantes

        # Mettre en surbrillance les lettres concordantes dans les suggestions
        for item in self.completer.popup().findChildren(QListWidgetItem):
            item_text = item.text()
            match_start = item_text.lower().find(completion_prefix.lower())
            if match_start != -1:
                item.setText("")
                item_text = item_text[:match_start] + "<font color=\"orange\">" + item_text[match_start:match_start + len(completion_prefix)] + "</font>" + item_text[match_start + len(completion_prefix):]
                item.setText(item_text)

        # Afficher les suggestions filtrées
        self.model.setStringList(sorted(filtered_keywords, key=lambda x: self.matchPercentage(completion_prefix, x), reverse=True))
        self.completer.complete()
        self.completer.popup().move(self.mapToGlobal(cursor_pos))

    def textUnderCursor(self):
        cursor = self.textCursor()
        cursor.select(QTextCursor.WordUnderCursor)
        return cursor.selectedText()

    def matchPercentage(self, prefix, word):
        if len(prefix) == 0:
            return 0.0
        return sum(c1 == c2 for c1, c2 in zip(prefix.lower(), word.lower())) / len(prefix)

    def loadKeywordsFromFile(self, filename):
        try:
            with open(filename, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print("Fichier de mots-clés introuvable.")
            return []

import parso

class AutoIndenter:
    def __init__(self, text_edit):
        self.text_edit = text_edit

    def handle_new_line(self):
        cursor = self.text_edit.textCursor()
        position = cursor.position()
        code_before_cursor = self.text_edit.toPlainText()[:position]

        # Analyse du code
        grammar = parso.load_grammar()
        module = grammar.parse(code_before_cursor)
        new_indent = self.get_indentation_level(module, position)

        # Insérer une nouvelle ligne avec l'indentation calculée
        cursor.insertText('\n' + '    ' * new_indent)

    def get_indentation_level(self, module, pos):
        """
        Cette fonction analyse le module Python pour déterminer le niveau d'indentation
        approprié pour la nouvelle ligne. Retourne un nombre d'espaces à insérer.
        """
        last_leaf = module.get_last_leaf()
        indentation_level = last_leaf.start_pos[1]

        if last_leaf.type == 'operator' and last_leaf.value == ':':
            indentation_level += 1  # Augmenter l'indentation après les structures de contrôle

        return indentation_level
