from PyQt5.QtWidgets import QPlainTextEdit, QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt

class MyEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
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

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    editor = MyEditor()
    mainWindow.setCentralWidget(editor)
    mainWindow.show()
    sys.exit(app.exec_())
