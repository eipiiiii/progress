from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QGroupBox, QComboBox, QFormLayout, QSpinBox, QDateEdit, QListWidget, QCheckBox, QMessageBox
)
from PyQt5.QtCore import QDate
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import matplotlib.dates as mdates
from data_manager import DataManager
import matplotlib.image as mpimg  # 画像を読み込むためのモジュール

class StudyProgressApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Study Progress Tracker")
        self.setGeometry(100, 100, 800, 600)
        
        self.data_manager = DataManager(self)
        self.tasks = self.data_manager.tasks
        self.records = self.data_manager.records

        self.init_ui()

    def init_ui(self):
        # Main widget and layout
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Task creation section
        task_group = QGroupBox("Create New Task")
        task_group.setStyleSheet("QGroupBox { font-size: 16px; font-weight: bold; }")
        task_layout = QVBoxLayout()
        task_form = QFormLayout()
        self.task_name_input = QLineEdit()
        self.target_amount_input = QSpinBox()  # Target amount input
        self.target_amount_input.setMaximum(1000)
        self.start_date_input = QDateEdit()
        self.start_date_input.setDate(QDate.currentDate())
        self.start_date_input.setCalendarPopup(True)
        self.end_date_input = QDateEdit()
        self.end_date_input.setDate(QDate.currentDate().addDays(7))
        self.end_date_input.setCalendarPopup(True)
        create_task_btn = QPushButton("Create Task")
        create_task_btn.setStyleSheet("QPushButton { font-size: 14px; }")
        create_task_btn.clicked.connect(self.create_task)

        task_form.addRow("Task Name", self.task_name_input)
        task_form.addRow("Target Amount", self.target_amount_input)
        task_form.addRow("Start Date", self.start_date_input)
        task_form.addRow("End Date", self.end_date_input)
        task_layout.addLayout(task_form)
        task_layout.addWidget(create_task_btn)
        task_group.setLayout(task_layout)
        layout.addWidget(task_group)

        # Task list section
        task_list_group = QGroupBox("Task List")
        task_list_group.setStyleSheet("QGroupBox { font-size: 16px; font-weight: bold; }")
        task_list_layout = QVBoxLayout()
        self.task_list = QListWidget()
        task_list_layout.addWidget(self.task_list)

        # Task deletion button
        delete_task_btn = QPushButton("Delete Selected Task")
        delete_task_btn.setStyleSheet("QPushButton { font-size: 14px; }")
        delete_task_btn.clicked.connect(self.delete_task)
        task_list_layout.addWidget(delete_task_btn)

        task_list_group.setLayout(task_list_layout)
        layout.addWidget(task_list_group)

        # Progress recording section
        record_group = QGroupBox("Record Progress")
        record_group.setStyleSheet("QGroupBox { font-size: 16px; font-weight: bold; }")
        record_layout = QVBoxLayout()
        record_form = QFormLayout()
        self.task_selector = QComboBox()
        self.update_task_selector()
        self.record_date_input = QDateEdit()
        self.record_date_input.setDate(QDate.currentDate())
        self.record_date_input.setCalendarPopup(True)
        self.progress_amount_input = QSpinBox()  # Progress amount input
        self.progress_amount_input.setMaximum(1000)
        self.delete_checkbox = QCheckBox("Delete Progress")
        record_task_btn = QPushButton("Record Progress")
        record_task_btn.setStyleSheet("QPushButton { font-size: 14px; }")
        record_task_btn.clicked.connect(self.record_progress)

        record_form.addRow("Task", self.task_selector)
        record_form.addRow("Date", self.record_date_input)
        record_form.addRow("Progress Amount", self.progress_amount_input)
        record_form.addRow(self.delete_checkbox)
        record_layout.addLayout(record_form)
        record_layout.addWidget(record_task_btn)
        record_group.setLayout(record_layout)
        layout.addWidget(record_group)

        # Graph display section
        graph_group = QGroupBox("Display Graph")
        graph_group.setStyleSheet("QGroupBox { font-size: 16px; font-weight: bold; }")
        graph_layout = QVBoxLayout()
        self.graph_task_selector = QComboBox()
        self.update_graph_task_selector()
        show_graph_btn = QPushButton("Show Graph")
        show_graph_btn.setStyleSheet("QPushButton { font-size: 14px; }")
        show_graph_btn.clicked.connect(self.show_graph)
        graph_layout.addWidget(QLabel("Select Task"))
        graph_layout.addWidget(self.graph_task_selector)
        graph_layout.addWidget(show_graph_btn)
        graph_group.setLayout(graph_layout)
        layout.addWidget(graph_group)

        # Set layout to central widget
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.update_task_list()

    def create_task(self):
        # Create new task
        task_name = self.task_name_input.text()
        target_amount = self.target_amount_input.value()  # Target amount
        start_date = self.start_date_input.date()
        end_date = self.end_date_input.date()

        # Calculate duration
        start_date_obj = datetime(start_date.year(), start_date.month(), start_date.day())
        end_date_obj = datetime(end_date.year(), end_date.month(), end_date.day())
        duration = (end_date_obj - start_date_obj).days

        if task_name and target_amount > 0 and duration > 0:
            task = {
                "name": task_name, 
                "target_amount": target_amount,  # Target amount
                "duration": duration, 
                "progress_amount": 0,  # Initialize progress amount to 0
                "start_date": start_date.toString("yyyy-MM-dd"),
                "end_date": end_date.toString("yyyy-MM-dd")
            }
            self.tasks.append(task)
            self.records[task_name] = []
            self.update_task_list()
            self.update_task_selector()
            self.update_graph_task_selector()
            self.task_name_input.clear()
            self.target_amount_input.setValue(0)
            self.data_manager.save_data()  # Save data
        else:
            self.show_error_message("Incomplete task information!")

    def delete_task(self):
        selected_task = self.task_list.currentItem()  # Get selected task
        if selected_task:
            task_name = selected_task.text().split(":")[0]  # Extract task name
            # Delete task
            self.tasks = [task for task in self.tasks if task["name"] != task_name]
            if task_name in self.records:
                del self.records[task_name]
            self.update_task_list()
            self.update_task_selector()
            self.update_graph_task_selector()
            self.data_manager.save_data()  # Save data
        else:
            self.show_error_message("Please select a task to delete!")

    def record_progress(self):
        task_name = self.task_selector.currentText()
        date = self.record_date_input.date().toString("yyyy-MM-dd")
        progress_amount = self.progress_amount_input.value()  # New progress amount

        if task_name:
            if self.delete_checkbox.isChecked():
                # Delete the record for the specified date
                if task_name in self.records:
                    self.records[task_name] = [record for record in self.records[task_name] if record["date"] != date]
                    print(f"Progress for {task_name} on {date} deleted.")
            else:
                if task_name not in self.records:
                    self.records[task_name] = []

                # Check for existing record
                existing_record = next((record for record in self.records[task_name] if record["date"] == date), None)
                if existing_record:
                    # Overwrite if progress is already recorded for the same date
                    existing_record["progress_amount"] = progress_amount
                else:
                    # Add new progress
                    self.records[task_name].append({"date": date, "progress_amount": progress_amount})

            # Calculate cumulative progress
            cumulative_progress = sum(record["progress_amount"] for record in self.records[task_name])

            # Update cumulative progress (for graph)
            task = next((task for task in self.tasks if task["name"] == task_name), None)
            if task:
                task["progress_amount"] = cumulative_progress
                print(f"Cumulative progress for {task_name} updated: {cumulative_progress}")

            self.data_manager.save_data()  # Save data
        else:
            self.show_error_message("No task to record progress for!")

    def update_task_list(self):
        self.task_list.clear()
        for task in self.tasks:
            self.task_list.addItem(f"{task['name']}: {task['target_amount']} ({task['start_date']} ~ {task['end_date']})")

    def update_task_selector(self):
        self.task_selector.clear()
        for task in self.tasks:
            self.task_selector.addItem(task["name"])

    def update_graph_task_selector(self):
        self.graph_task_selector.clear()
        for task in self.tasks:
            self.graph_task_selector.addItem(task["name"])

    def show_graph(self):
        # Graph display processing
        task_name = self.graph_task_selector.currentText()
        if not task_name:
            self.show_error_message("No task selected!")
            return

        task = next((task for task in self.tasks if task["name"] == task_name), None)
        if not task:
            self.show_error_message("Selected task not found!")
            return

        if not self.records.get(task_name):
            self.show_error_message(f"No progress records for {task_name}!")
            return

        # Prepare data
        target_amount = task["target_amount"]  # Target amount
        start_date = datetime.strptime(task["start_date"], "%Y-%m-%d")
        end_date = datetime.strptime(task["end_date"], "%Y-%m-%d")

        # Actual progress data
        try:
            record_dates = [datetime.strptime(record["date"], "%Y-%m-%d") for record in self.records[task_name]]
            record_progress_amounts = [record["progress_amount"] for record in self.records[task_name]]
        except ValueError as e:
            self.show_error_message(f"Error in date format: {e}")
            return

        if not record_dates:
            self.show_error_message("No progress records!")
            return

        record_dates = [record_dates[0] - timedelta(days=1)] + record_dates  # Add date one day before

        # Calculate cumulative progress
        cumulative_progress_list = []
        cumulative_progress = 0
        for progress in record_progress_amounts:
            cumulative_progress += progress
            cumulative_progress_list.append(cumulative_progress)

        # Actual remaining amount (target amount - cumulative progress)
        remaining_amounts = [target_amount] + [target_amount - progress for progress in cumulative_progress_list]

        # Ideal progress (expressed as remaining amount, initial state is target amount)
        ideal_remaining = [target_amount - (target_amount * (i / (end_date - (start_date - timedelta(days=1))).days)) 
                           for i in range((end_date - (start_date - timedelta(days=1))).days + 1)]
        ideal_dates = [start_date - timedelta(days=1) + timedelta(days=i) 
                       for i in range((end_date - (start_date - timedelta(days=1))).days + 1)]

        # Plot graph with seaborn style
        sns.set(style="whitegrid")
        fig, ax = plt.subplots(figsize=(12, 8))

        # Load background image
        img = mpimg.imread('background1.jpg')
        ax.imshow(img, extent=[mdates.date2num(start_date - timedelta(days=1)), mdates.date2num(end_date), 0, target_amount], aspect='auto', zorder=-1)

        # Plot actual progress remaining amount
        if len(record_dates) > 1:
            ax.plot(record_dates, remaining_amounts, label="Actual Progress", color="blue", marker="o", zorder=1)

        # Plot ideal progress
        ax.plot(ideal_dates, ideal_remaining, label="Ideal Progress", linestyle="--", color="red", zorder=1)

        # Graph settings
        ax.set_title(f"Progress Graph for {task_name}", fontsize=16)
        ax.set_xlabel("Date", fontsize=14)
        ax.set_ylabel("Remaining Amount", fontsize=14)
        plt.xticks(rotation=45)
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.legend()
        plt.tight_layout()
        plt.grid(True)

        plt.show()

    def show_error_message(self, message):
        QMessageBox.critical(self, "Error", message)