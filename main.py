import sys
from PyQt5.QtWidgets import QApplication
from ui import StudyProgressApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = StudyProgressApp()
    main_window.show()
    sys.exit(app.exec_())