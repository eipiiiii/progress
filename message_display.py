from PyQt5.QtWidgets import QMessageBox

def show_error_message(app, message):
    QMessageBox.critical(app, "Error", message)

def show_info_message(app, message):
    QMessageBox.information(app, "Information", message)