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
    def __init__(self, text_document, theme_name="Monokai"):
        super().__init__(text_document)
        self.styles = {
    'keyword': QTextCharFormat(),
    'operator': QTextCharFormat(),
    'brace': QTextCharFormat(),
    'defclass': QTextCharFormat(),
    'string': QTextCharFormat(),
    'comment': QTextCharFormat(),
    'self': QTextCharFormat(),
    'numbers': QTextCharFormat(),
}
        
        

        
        # Highlight rules
       # Highlight rules
        self.rules = [
            (r'\bdef\b|\bclass\b|\bimport\b|\bfrom\b|\bas\b|\breturn\b|\bif\b|\belse\b|\btry\b|\bexcept\b|\bfinally\b|\bwhile\b|\bfor\b|\bin\b|\bis\b|\band\b|\bor\b|\bnot\b', self.styles['keyword']),
            (r'"[^"\\]*(\\.[^"\\]*)*"', self.styles['string']),
            (r"'[^'\\]*(\\.[^'\\]*)*'", self.styles['string']),  # Use 'string' for single-quoted strings too
            (r'\b\d+\b', self.styles['numbers']),
            (r'\#.*', self.styles['comment']),
            (r'\bself\b', self.styles['self']),
            (r'\b__init__\b|\b__name__\b', self.styles['defclass']),
            (r'[{}()\[\]]', self.styles['brace']),
            (r'[.,;:+-/*=<>%]', self.styles['operator']),
        ]

   
        
        self.theme = SyntaxThemes.get_theme(theme_name)  # Initialize with a default theme
        self.configure_styles()

    def configure_styles(self):
        # Apply current theme colors to the styles
        for key, format in self.styles.items():
            format.setForeground(self.theme[key])

    def set_theme(self, theme_name):
        self.theme = SyntaxThemes.get_theme(theme_name)
        self.configure_styles()
        self.rehighlight()  # Reapply the highlighting with the new theme



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
        self.keywords = self.load_keywords_from_file("Athena\speedy\V\keywords2.json")
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



class SyntaxThemes:
    themes = {
        "Monokai": {
            'keyword': QColor('#F92672'),
            'operator': QColor('#F92672'),
            'brace': QColor('#FFFFFF'),
            'defclass': QColor('#A6E22E'),
            'string': QColor('#E6DB74'),
            'comment': QColor('#75715E'),
            'self': QColor('#66D9EF'),
            'numbers': QColor('#AE81FF'),
        },
        "Dracula": {
            'keyword': QColor('#FF79C6'),
            'operator': QColor('#FF79C6'),
            'brace': QColor('#F8F8F2'),
            'defclass': QColor('#50FA7B'),
            'string': QColor('#F1FA8C'),
            'comment': QColor('#6272A4'),
            'self': QColor('#BD93F9'),
            'numbers': QColor('#BD93F9'),
        },
        "Solarized Light": {
            'keyword': QColor('#859900'),
            'operator': QColor('#859900'),
            'brace': QColor('#93A1A1'),
            'defclass': QColor('#268BD2'),
            'string': QColor('#2AA198'),
            'comment': QColor('#93A1A1'),
            'self': QColor('#D33682'),
            'numbers': QColor('#D33682'),
        },
        "Solarized Dark": {
            'keyword': QColor('#B58900'),
            'operator': QColor('#B58900'),
            'brace': QColor('#839496'),
            'defclass': QColor('#268BD2'),
            'string': QColor('#2AA198'),
            'comment': QColor('#657B83'),
            'self': QColor('#D33682'),
            'numbers': QColor('#D33682'),
        },
        "GitHub": {
            'keyword': QColor('#333'),
            'operator': QColor('#333'),
            'brace': QColor('#333'),
            'defclass': QColor('#0366d6'),
            'string': QColor('#032F62'),
            'comment': QColor('#6A737D'),
            'self': QColor('#22863A'),
            'numbers': QColor('#005CC5'),
        },
        "Nord": {
            'keyword': QColor('#81A1C1'),
            'operator': QColor('#81A1C1'),
            'brace': QColor('#ECEFF4'),
            'defclass': QColor('#8FBCBB'),
            'string': QColor('#A3BE8C'),
            'comment': QColor('#4C566A'),
            'self': QColor('#88C0D0'),
            'numbers': QColor('#B48EAD'),
        },
        "Gruvbox": {
            'keyword': QColor('#FABD2F'),
            'operator': QColor('#FABD2F'),
            'brace': QColor('#EBDBB2'),
            'defclass': QColor('#8EC07C'),
            'string': QColor('#B8BB26'),
            'comment': QColor('#928374'),
            'self': QColor('#FE8019'),
            'numbers': QColor('#D3869B'),
        },
        "Oceanic Next": {
            'keyword': QColor('#C594C5'),
            'operator': QColor('#C594C5'),
            'brace': QColor('#CDD3DE'),
            'defclass': QColor('#6699CC'),
            'string': QColor('#99C794'),
            'comment': QColor('#65737E'),
            'self': QColor('#5FB3B3'),
            'numbers': QColor('#F99157'),
        },
        "One Dark": {
            'keyword': QColor('#C678DD'),
            'operator': QColor('#C678DD'),
            'brace': QColor('#ABB2BF'),
            'defclass': QColor('#E06C75'),
            'string': QColor('#98C379'),
            'comment': QColor('#5C6370'),
            'self': QColor('#56B6C2'),
            'numbers': QColor('#D19A66'),
        },
        "Zenburn": {
            'keyword': QColor('#DCA3A3'),
            'operator': QColor('#DCA3A3'),
            'brace': QColor('#F0DFAF'),
            'defclass': QColor('#DFC47D'),
            'string': QColor('#CC9393'),
            'comment': QColor('#7F9F7F'),
            'self': QColor('#F0DFAF'),
            'numbers': QColor('#8CD0D3'),
        }
    }

    @classmethod
    def get_theme(cls, theme_name):
        return cls.themes.get(theme_name, cls.themes["Monokai"])
