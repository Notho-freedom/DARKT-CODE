import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QHBoxLayout, QLabel, QWidget, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QImage, QPixmap

class MiniMap(QLabel):
    def __init__(self, linked_editor):
        super().__init__()
        self.linked_editor = linked_editor
        self.setMaximumWidth(80)  # Réduire la largeur de la mini-map
        self.update_map()

    def update_map(self):
        # Capturer une image du contenu de l'éditeur
        content_image = QImage(self.linked_editor.viewport().size(), QImage.Format_ARGB32)
        content_image.fill(Qt.white)
        painter = QPainter(content_image)
        self.linked_editor.render(painter)
        painter.end()

        # Redimensionner l'image pour la mini-map
        scaled_img = content_image.scaled(self.width(), self.linked_editor.height(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(QPixmap.fromImage(scaled_img))

    def mousePressEvent(self, event):
        # Calculer la nouvelle position de scroll basé sur le clic dans la mini-map
        factor = self.linked_editor.document().size().height() / self.height()
        new_y = event.y() * factor
        self.linked_editor.verticalScrollBar().setValue(int(new_y))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.editor = QTextEdit()
        self.editor.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Rendre invisible la barre de défilement verticale
        self.editor.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # Réduire l'épaisseur de la barre horizontale si nécessaire
        self.editor.textChanged.connect(self.update_mini_map)

        self.mini_map = MiniMap(self.editor)
        self.editor.verticalScrollBar().valueChanged.connect(self.update_mini_map)

        # Configurer QHBoxLayout pour placer la mini-map à côté de l'éditeur
        layout = QHBoxLayout()
        layout.addWidget(self.editor, 1)
        layout.addWidget(self.mini_map, 0, Qt.AlignRight)  # Superposer la mini-map à l'extrême droite

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.setWindowTitle("Code Editor with MiniMap")
        self.resize(800, 600)

    def update_mini_map(self):
        self.mini_map.update_map()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
