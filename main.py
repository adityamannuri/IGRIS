import sys
from PySide6.QtWidgets import QApplication
from interface import IgrisInterface

app = QApplication(sys.argv)

window = IgrisInterface()
window.show()

sys.exit(app.exec())