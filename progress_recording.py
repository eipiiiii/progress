from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QFormLayout, QComboBox, QDateEdit, QSpinBox, QPushButton
from PyQt5.QtCore import QDate  # QDateをインポート

def setup_progress_recording_section(app, layout):
    record_group = QGroupBox("Record Progress")
    record_group.setStyleSheet("QGroupBox { font-size: 16px; font-weight: bold; }")
    record_layout = QVBoxLayout()
    record_form = QFormLayout()
    app.task_selector = QComboBox()
    app.update_task_selector()
    app.record_date_input = QDateEdit()
    app.record_date_input.setDate(QDate.currentDate())
    app.record_date_input.setCalendarPopup(True)
    app.record_date_input.dateChanged.connect(app.update_progress_amount_input)  # 日付が変更されたときに呼び出す
    app.progress_amount_input = QSpinBox()  # 進捗量入力
    app.progress_amount_input.setMaximum(1000)
    record_task_btn = QPushButton("Record Progress")
    record_task_btn.setStyleSheet("QPushButton { font-size: 14px; }")
    record_task_btn.clicked.connect(app.record_progress)
    delete_progress_btn = QPushButton("Delete Progress")
    delete_progress_btn.setStyleSheet("QPushButton { font-size: 14px; }")
    delete_progress_btn.clicked.connect(app.delete_progress)

    record_form.addRow("Task", app.task_selector)
    record_form.addRow("Date", app.record_date_input)
    record_form.addRow("Progress Amount", app.progress_amount_input)
    record_layout.addLayout(record_form)
    record_layout.addWidget(record_task_btn)
    record_layout.addWidget(delete_progress_btn)
    record_group.setLayout(record_layout)
    layout.addWidget(record_group)