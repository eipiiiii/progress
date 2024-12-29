from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel
from data_manager import DataManager
from task_creation import setup_task_creation_section
from task_list import setup_task_list_section
from progress_recording import setup_progress_recording_section
from task_summary import setup_task_summary_section
from message_display import show_error_message, show_info_message
from graph_display import show_graph
from task_management import create_task, delete_task, update_task_list, update_task_selector, update_graph_task_selector, update_task_summary_selector, update_task_summary
from progress_management import record_progress, delete_progress, update_progress_amount_input
from datetime import datetime, timedelta

class StudyProgressApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Study Progress Tracker")
        self.setGeometry(100, 100, 800, 600)
        
        self.data_manager = DataManager(self)
        self.tasks = self.data_manager.tasks
        self.records = self.data_manager.records

        self.daily_target_label = QLabel("Daily Target: N/A")
        self.total_progress_label = QLabel("Total Progress: N/A")

        self.init_ui()
        self.check_missed_dates()

    def init_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout()

        setup_task_creation_section(self, layout)
        setup_task_list_section(self, layout)
        setup_progress_recording_section(self, layout)
        setup_task_summary_section(self, layout)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.update_task_list()

    def check_missed_dates(self):
        today = datetime.now().date()
        for task_name, records in self.records.items():
            task = next((task for task in self.tasks if task["name"] == task_name), None)
            if task:
                start_date = datetime.strptime(task["start_date"], "%Y-%m-%d").date()
                end_date = datetime.strptime(task["end_date"], "%Y-%m-%d").date()
                date_range = (end_date - start_date).days + 1
                for i in range(date_range):
                    date = start_date + timedelta(days=i)
                    if date < today and not any(record["date"] == date.strftime("%Y-%m-%d") for record in records):
                        self.records[task_name].append({"date": date.strftime("%Y-%m-%d"), "progress_amount": 0})
        self.data_manager.save_data()