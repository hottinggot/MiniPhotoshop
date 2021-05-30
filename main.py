import sys
import window
from PySide2.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    ex = window.Window()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
