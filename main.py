#ver 1.1.0

import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from qt import *

if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setWindowIcon(QIcon('icon.jpg'))
    p = LoginWindow()
    p.initUI()

    p.show()
    sys.exit(app.exec_())
