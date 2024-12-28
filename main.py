import sys
from PyQt5.QtWidgets import QApplication
from ui import StudyProgressApp

if __name__ == "__main__":
    # アプリケーションのインスタンスを作成
    app = QApplication(sys.argv)
    # メインウィンドウのインスタンスを作成
    main_window = StudyProgressApp()
    # メインウィンドウを表示
    main_window.show()
    # アプリケーションのイベントループを開始
    sys.exit(app.exec_())