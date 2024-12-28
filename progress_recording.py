from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QFormLayout, QComboBox, QDateEdit, QSpinBox, QPushButton
from PyQt5.QtCore import QDate
from datetime import datetime

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
    app.record_date_input.dateChanged.connect(app.update_progress_amount_input)
    app.progress_amount_input = QSpinBox()
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

def record_progress(app):
    task_name = app.task_selector.currentText()
    date = app.record_date_input.date().toString("yyyy-MM-dd")
    progress_amount = app.progress_amount_input.value()

    today = datetime.now().date()
    record_date = datetime.strptime(date, "%Y-%m-%d").date()

    if record_date > today:
        app.show_error_message("Cannot record progress for a future date!")
        return

    if task_name:
        if task_name not in app.records:
            app.records[task_name] = []

        existing_record = next((record for record in app.records[task_name] if record["date"] == date), None)
        if existing_record:
            existing_record["progress_amount"] = progress_amount
        else:
            app.records[task_name].append({"date": date, "progress_amount": progress_amount})

        cumulative_progress = sum(record["progress_amount"] for record in app.records[task_name])

        task = next((task for task in app.tasks if task["name"] == task_name), None)
        if task:
            task["progress_amount"] = cumulative_progress
            print(f"Cumulative progress for {task_name} updated: {cumulative_progress}")

        app.data_manager.save_data()
        app.show_info_message("Progress recorded successfully!")
    else:
        app.show_error_message("No task to record progress for!")

def delete_progress(app):
    task_name = app.task_selector.currentText()
    date = app.record_date_input.date().toString("yyyy-MM-dd")

    if task_name:
        if task_name in app.records:
            app.records[task_name] = [record for record in app.records[task_name] if record["date"] != date]
            app.data_manager.save_data()
            app.show_info_message("Progress deleted successfully!")
    else:
        app.show_error_message("No task to delete progress for!")