import sys

from PyQt5.QtWidgets import QApplication
import authentication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = authentication.Authentication()
    sys.exit(app.exec_())
