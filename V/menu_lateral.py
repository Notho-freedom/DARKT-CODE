import sys
import json
import asyncio
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
        self.keywords = {}
        self.highlighter = SyntaxHighlighter(self.document(), self.keywords)
        self.completer = QCompleter()
        self.model = QStringListModel()
        self.completer.setModel(self.model)
        self.completer.setWidget(self)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.setFilterMode(Qt.MatchContains)
        self.completer.activated.connect(self.insertCompletion)
        asyncio.run(self.loadKeywordsFromFile("Athena/speedy/V/keywords.json"))

    async def loadKeywordsFromFile(self, filename):
        file = QFile(filename)
        if not file.open(QIODevice.ReadOnly):
            print(f"Impossible d'ouvrir le fichier {filename}")
            return

        data = await file.readAll()
        keywords = json.loads(str(data, 'utf-8'))
        self.keywords = keywords
        self.model.setStringList(sum(keywords.values(), []))

    def insertCompletion(self, text):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.StartOfWord, QTextCursor.KeepAnchor)
        cursor.removeSelectedText()
        cursor.insertText(text)

    def processPastedText(self):
        pasted_text = self.toPlainText()
        asyncio.run(self.loadKeywordsFromFile("Athena/speedy/V/keywords.json"))

    def pasteEvent(self, event):
        QTimer.singleShot(0, self.processPastedText)
        super().pasteEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = AutoCompleterCodeEditor()
    editor.show()
    sys.exit(app.exec_())
