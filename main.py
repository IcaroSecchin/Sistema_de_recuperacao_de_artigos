import windows
import sys
from PyQt6.QtWidgets import (
    QApplication,
)
from PyQt6.QtGui import QIcon

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('Icone/cadastre-se.png'))
    window = windows.Janela_Inicial()
    window.show()
    sys.exit(app.exec())