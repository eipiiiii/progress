from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QFormLayout, QLineEdit, QSpinBox, QDateEdit, QPushButton
from PyQt5.QtCore import QDate
from datetime import datetime

def setup_task_creation_section(app, layout):
    # タスク作成セクションのセットアップ
    task_group = QGroupBox("Create New Task")
    task_group.setStyleSheet("QGroupBox { font-size: 16px; font-weight: bold; }")
    task_layout = QVBoxLayout()
    task_form = QFormLayout()
    app.task_name_input = QLineEdit()
    app.target_amount_input = QSpinBox()
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

def create_task(app):
    # タスクを作成する関数
    task_name = app.task_name_input.text()
    target_amount = app.target_amount_input.value()
    start_date = app.start_date_input.date()
    end_date = app.end_date_input.date()

    start_date_obj = datetime(start_date.year(), start_date.month(), start_date.day())
    end_date_obj = datetime(end_date.year(), end_date.month(), end_date.day())
    duration = (end_date_obj - start_date_obj).days

    if task_name and target_amount > 0 and duration > 0:
        task = {
            "name": task_name, 
            "target_amount": target_amount,
            "duration": duration, 
            "progress_amount": 0,
            "start_date": start_date.toString("yyyy-MM-dd"),
            "end_date": end_date.toString("yyyy-MM-dd")
        }
        app.tasks.append(task)
        app.records[task_name] = []
        app.update_task_list()
        app.update_task_selector()
        app.update_graph_task_selector()
        app.task_name_input.clear()
        app.target_amount_input.setValue(0)
        app.data_manager.save_data()
        app.show_info_message("Task created successfully!")
    else:
        app.show_error_message("Incomplete task information!")