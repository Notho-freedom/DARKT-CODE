import sys
from PyQt5.QtWidgets import QApplication
from editor import *

def main():
    app = QApplication(sys.argv)
    editor = Editor()
    editor.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
