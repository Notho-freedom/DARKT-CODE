import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtGui import QFont, QTextCursor
from PyQt5.QtCore import Qt, QTimer
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import jedi

class CodeEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dark Code Editor")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.layout = QVBoxLayout()

        self.editor = QTextEdit()
        self.editor.setStyleSheet("background-color: #2b2b2b; color: #f0f0f0;")
        self.editor.setFont(QFont("Consolas", 12))

        self.layout.addWidget(self.editor)

        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.timer = QTimer()
        self.timer.setInterval(500)  # Set the interval to 500 ms
        #self.timer.timeout.connect(self.handle_text_changed)
        self.editor.textChanged.connect(self.timer.start)

    def handle_text_changed(self):
        self.timer.stop()
        code = self.editor.toPlainText()
        cursor = self.editor.textCursor()
        position = cursor.position()

        highlighted_code = self.highlight_code(code)
        self.editor.setHtml(highlighted_code)
        self.restore_cursor(position)

        line, column = self.get_line_column(position)
        completions = self.get_completions(code, line, column)
        print(completions)  # Temporarily print completions

    def highlight_code(self, code):
        lexer = PythonLexer()
        formatter = HtmlFormatter(style='monokai', nowrap=True)
        return highlight(code, lexer, formatter)

    def get_line_column(self, position):
        cursor = self.editor.textCursor()
        cursor.setPosition(position)
        return cursor.blockNumber() + 1, cursor.columnNumber()

    def restore_cursor(self, position):
        cursor = self.editor.textCursor()
        cursor.setPosition(position)
        self.editor.setTextCursor(cursor)

    def get_completions(self, code, line, column):
        try:
            # Vous pouvez également spécifier un chemin fictif si vous ne travaillez pas avec des fichiers réels
            script = jedi.Script(code=code, path='terminal.py')
            completions = script.complete(line=line, column=column)
            return [c.name for c in completions]
        except Exception as e:
            print("Error getting completions:", e)
            return []


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = CodeEditor()
    editor.show()
    sys.exit(app.exec_())
