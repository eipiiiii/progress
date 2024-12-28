from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QFormLayout, QLineEdit, QSpinBox, QDateEdit, QPushButton
from PyQt5.QtCore import QDate  # QDateをインポート

def setup_task_creation_section(app, layout):
    task_group = QGroupBox("Create New Task")
    task_group.setStyleSheet("QGroupBox { font-size: 16px; font-weight: bold; }")
    task_layout = QVBoxLayout()
    task_form = QFormLayout()
    app.task_name_input = QLineEdit()
    app.target_amount_input = QSpinBox()  # 目標量入力
    app.target_amount_input.setMaximum(1000)
    app.start_date_input = QDateEdit()
    app.start_date_input.setDate(QDate.currentDate())
    app.start_date_input.setCalendarPopup(True)
    app.end_date_input = QDateEdit()
    app.end_date_input.setDate(QDate.currentDate().addDays(7))
    app.end_date_input.setCalendarPopup(True)
    create_task_btn = QPushButton("Create Task")
    create_task_btn.setStyleSheet("QPushButton { font-size: 14px; }")
    create_task_btn.clicked.connect(app.create_task)

    task_form.addRow("Task Name", app.task_name_input)
    task_form.addRow("Target Amount", app.target_amount_input)
    task_form.addRow("Start Date", app.start_date_input)
    task_form.addRow("End Date", app.end_date_input)
    task_layout.addLayout(task_form)
    task_layout.addWidget(create_task_btn)
    task_group.setLayout(task_layout)
    layout.addWidget(task_group)