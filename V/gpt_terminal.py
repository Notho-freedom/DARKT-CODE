import sys
import json
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent, keywords):
        super().__init__(parent)
        self.parent = parent
        self.keywords = keywords
        self.highlight_rules = []

        # Couleurs pour chaque groupe de mots-clés
        self.colors = {
            "magenta": Qt.magenta,
            "blue": Qt.cyan,
            "cyan": Qt.blue,
            "yellow": Qt.yellow,
            "darkgreen": Qt.darkGreen
        }

        # Créer une règle de mise en évidence pour chaque mot-clé
        for group, color in self.colors.items():
            char_format = QTextCharFormat()
            char_format.setForeground(color)
            char_format.setFontWeight(QFont.Bold)
            if group in keywords:
                self.highlight_rules.extend([(r'\b%s\b' % keyword, char_format) for keyword in keywords[group]])

        # Créer une règle de mise en évidence pour les mots suivant un point
        dot_format = QTextCharFormat()
        dot_format.setForeground(QColor(0, 204, 255))
        self.highlight_rules.append((r'\.([a-zA-Z_]\w*)\b', dot_format))

        # Règle pour les mots entre guillemets
        quotation_format = QTextCharFormat()
        quotation_format.setForeground(QColor(255, 165, 0))
        self.highlight_rules.append((r'(\".*?\"|\'.*?\')', quotation_format))

        # Règle pour les mots suivant 'def' et 'class'
        function_class_format = QTextCharFormat()
        function_class_format.setForeground(Qt.cyan)
        self.highlight_rules.extend([(r'\b(def|class)\b\s*(\w+)', function_class_format)])



    def highlightBlock(self, text):
        for pattern, char_format in self.highlight_rules:
            expression = QRegularExpression(pattern)
            it = expression.globalMatch(text)
            while it.hasNext():
                match = it.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), char_format)


class AutoCompleterCodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.setFont(QFont("Helvetica", 10))
        self.keywords = self.loadKeywordsFromFile("Athena\speedy\V\keywords.json")
        self.highlighter = SyntaxHighlighter(self.document(), self.keywords)
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


class AutoCompleter(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QFont("Consolas", 12))
        self.keywords = self.load_keywords_from_file("path_to_keywords.json")
        self.completer = self.setup_completer(self.keywords)

    def load_keywords_from_file(self, filepath):
        try:
            with open(filepath, "r") as file:
                data = json.load(file)
                keywords = [word for sublist in data.values() for word in sublist]
                return keywords
        except FileNotFoundError:
            print("File not found.")
            return []

    def setup_completer(self, keywords):
        completer = QCompleter(keywords, self)
        completer.setWidget(self)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.activated.connect(self.insert_completion)
        return completer

    def insert_completion(self, completion):
        cursor = self.textCursor()
        extra = len(completion) - len(self.completer.completionPrefix())
        cursor.movePosition(QTextCursor.Left)
        cursor.movePosition(QTextCursor.EndOfWord)
        cursor.insertText(completion[-extra:])
        self.setTextCursor(cursor)

    def keyPressEvent(self, event):
        if self.completer and self.completer.popup().isVisible():
            if event.key() in (Qt.Key_Enter, Qt.Key_Return):
                event.ignore()
                return
            elif event.key() in (Qt.Key_Escape):
                event.ignore()
                self.completer.popup().hide()
                return
        super().keyPressEvent(event)

        if not self.completer:
            return

        # Affichage du popup si le texte actuel est un préfixe valide
        completion_prefix = self.text_under_cursor()
        if len(completion_prefix) < 1 or len(completion_prefix) > 50:
            self.completer.popup().hide()
            return

        self.completer.setCompletionPrefix(completion_prefix)
        self.completer.popup().setCurrentIndex(self.completer.completionModel().index(0, 0))
        cursor_rect = self.cursorRect()
        cursor_rect.setWidth(self.completer.popup().sizeHintForColumn(0) + self.completer.popup().verticalScrollBar().sizeHint().width())
        self.completer.complete(cursor_rect)

    def text_under_cursor(self):
        cursor = self.textCursor()
        cursor.select(QTextCursor.WordUnderCursor)
        return cursor.selectedText()
