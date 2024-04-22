import json
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.styles import *
from pygments.token import Token
from .syntaxHighlighter import PythonSyntaxHighlighter
from .lineNumber import LineNumberArea


class AutoCompleterCodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.setFont(QFont("Helvetica", 10))
        self.keywords = self.loadKeywordsFromFile("V\M\keywords.json")
        self.highlighter = PythonSyntaxHighlighter(self.document())
        self.completer = QCompleter()
        self.model = QStringListModel(self.keywords)
        self.completer.setModel(self.model)
        self.completer.setWidget(self)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.setFilterMode(Qt.MatchContains)
        self.completer.activated.connect(self.insertCompletion)

        self.lineNumberArea = LineNumberArea(self)

        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        #self.cursorPositionChanged.connect(self.highlight_current_line)

        self.update_line_number_area_width(0)

        self.cursorPositionChanged.connect(self.update)

    def paintEvent(self, event):
        super().paintEvent(event)

        # Custom painting code
        painter = QPainter(self.viewport())
        painter.setPen(QColor(Qt.red))  # Set the color of the border
        rect = self.cursorRect()  # Get the rectangle around the current line
        
        # Modify the rectangle dimensions
        rect.setX(0)  # Start from the very left of the text area
        rect.setWidth(self.viewport().width())  # Extend to the full width of the viewport
        rect.setHeight(rect.height()+5)  # Adjust height if necessary

        # Optional: add padding
        padding = 0
        rect.adjust(padding, 0, -padding, -6)  # Shrink the rectangle by padding on all sides
        
        painter.drawRect(rect)  # Draw the border
        
    def line_number_area_width(self):
        digits = len(str(max(1, self.blockCount())))
        space = 3 + self.fontMetrics().width('9') * digits
        return space

    def update_line_number_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(cr.left(), cr.top(), self.line_number_area_width(), cr.height())

    def line_number_area_paint_event(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), Qt.lightGray)

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                painter.setPen(Qt.black)
                painter.drawText(0, int(top), self.lineNumberArea.width(), self.fontMetrics().height(),
                                 Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

    def highlight_current_line(self):
        extra_selections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()

            line_color = QColor(Qt.black).lighter(160)
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)

        self.setExtraSelections(extra_selections)

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
