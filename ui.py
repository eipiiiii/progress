from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QGroupBox, QComboBox, QFormLayout, QSpinBox, QDateEdit, QListWidget, QMessageBox
)
from PyQt5.QtCore import QDate, QTimer
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
        self.check_missed_dates()

    def init_ui(self):
        # メインウィジェットとレイアウト
        central_widget = QWidget()
        layout = QVBoxLayout()

        # タスク作成セクション
        self.setup_task_creation_section(layout)

        # タスクリストセクション
        self.setup_task_list_section(layout)

        # 進捗記録セクション
        self.setup_progress_recording_section(layout)

        # グラフ表示セクション
        self.setup_graph_display_section(layout)

        # レイアウトを中央ウィジェットに設定
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.update_task_list()

    def setup_task_creation_section(self, layout):
        task_group = QGroupBox("Create New Task")
        task_group.setStyleSheet("QGroupBox { font-size: 16px; font-weight: bold; }")
        task_layout = QVBoxLayout()
        task_form = QFormLayout()
        self.task_name_input = QLineEdit()
        self.target_amount_input = QSpinBox()  # 目標量入力
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

    def setup_task_list_section(self, layout):
        task_list_group = QGroupBox("Task List")
        task_list_group.setStyleSheet("QGroupBox { font-size: 16px; font-weight: bold; }")
        task_list_layout = QVBoxLayout()
        self.task_list = QListWidget()
        task_list_layout.addWidget(self.task_list)

        delete_task_btn = QPushButton("Delete Selected Task")
        delete_task_btn.setStyleSheet("QPushButton { font-size: 14px; }")
        delete_task_btn.clicked.connect(self.delete_task)
        task_list_layout.addWidget(delete_task_btn)

        task_list_group.setLayout(task_list_layout)
        layout.addWidget(task_list_group)

    def setup_progress_recording_section(self, layout):
        record_group = QGroupBox("Record Progress")
        record_group.setStyleSheet("QGroupBox { font-size: 16px; font-weight: bold; }")
        record_layout = QVBoxLayout()
        record_form = QFormLayout()
        self.task_selector = QComboBox()
        self.update_task_selector()
        self.record_date_input = QDateEdit()
        self.record_date_input.setDate(QDate.currentDate())
        self.record_date_input.setCalendarPopup(True)
        self.record_date_input.dateChanged.connect(self.update_progress_amount_input)  # 日付が変更されたときに呼び出す
        self.progress_amount_input = QSpinBox()  # 進捗量入力
        self.progress_amount_input.setMaximum(1000)
        record_task_btn = QPushButton("Record Progress")
        record_task_btn.setStyleSheet("QPushButton { font-size: 14px; }")
        record_task_btn.clicked.connect(self.record_progress)
        delete_progress_btn = QPushButton("Delete Progress")
        delete_progress_btn.setStyleSheet("QPushButton { font-size: 14px; }")
        delete_progress_btn.clicked.connect(self.delete_progress)

        record_form.addRow("Task", self.task_selector)
        record_form.addRow("Date", self.record_date_input)
        record_form.addRow("Progress Amount", self.progress_amount_input)
        record_layout.addLayout(record_form)
        record_layout.addWidget(record_task_btn)
        record_layout.addWidget(delete_progress_btn)
        record_group.setLayout(record_layout)
        layout.addWidget(record_group)

    def update_progress_amount_input(self):
        task_name = self.task_selector.currentText()
        date = self.record_date_input.date().toString("yyyy-MM-dd")

        if task_name in self.records:
            existing_record = next((record for record in self.records[task_name] if record["date"] == date), None)
            if existing_record:
                self.progress_amount_input.setValue(existing_record["progress_amount"])
            else:
                self.progress_amount_input.setValue(0)
        else:
            self.progress_amount_input.setValue(0)

    def setup_graph_display_section(self, layout):
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

    def create_task(self):
        task_name = self.task_name_input.text()
        target_amount = self.target_amount_input.value()  # 目標量
        start_date = self.start_date_input.date()
        end_date = self.end_date_input.date()

        start_date_obj = datetime(start_date.year(), start_date.month(), start_date.day())
        end_date_obj = datetime(end_date.year(), end_date.month(), end_date.day())
        duration = (end_date_obj - start_date_obj).days

        if task_name and target_amount > 0 and duration > 0:
            task = {
                "name": task_name, 
                "target_amount": target_amount,  # 目標量
                "duration": duration, 
                "progress_amount": 0,  # 進捗量を0で初期化
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
            self.data_manager.save_data()  # データを保存
            self.show_info_message("Task created successfully!")
        else:
            self.show_error_message("Incomplete task information!")

    def delete_task(self):
        selected_task = self.task_list.currentItem()  # 選択されたタスクを取得
        if selected_task:
            task_name = selected_task.text().split(":")[0]  # タスク名を抽出
            self.tasks = [task for task in self.tasks if task["name"] != task_name]
            if task_name in self.records:
                del self.records[task_name]
            self.update_task_list()
            self.update_task_selector()
            self.update_graph_task_selector()
            self.data_manager.save_data()  # データを保存
            self.show_info_message("Task deleted successfully!")
        else:
            self.show_error_message("Please select a task to delete!")

    def record_progress(self):
        task_name = self.task_selector.currentText()
        date = self.record_date_input.date().toString("yyyy-MM-dd")
        progress_amount = self.progress_amount_input.value()  # 新しい進捗量

        today = datetime.now().date()
        record_date = datetime.strptime(date, "%Y-%m-%d").date()

        if record_date > today:
            self.show_error_message("Cannot record progress for a future date!")
            return

        if task_name:
            if task_name not in self.records:
                self.records[task_name] = []

            existing_record = next((record for record in self.records[task_name] if record["date"] == date), None)
            if existing_record:
                existing_record["progress_amount"] = progress_amount
            else:
                self.records[task_name].append({"date": date, "progress_amount": progress_amount})

            cumulative_progress = sum(record["progress_amount"] for record in self.records[task_name])

            task = next((task for task in self.tasks if task["name"] == task_name), None)
            if task:
                task["progress_amount"] = cumulative_progress
                print(f"Cumulative progress for {task_name} updated: {cumulative_progress}")

            self.data_manager.save_data()  # データを保存
            self.show_info_message("Progress recorded successfully!")
        else:
            self.show_error_message("No task to record progress for!")

    def delete_progress(self):
        task_name = self.task_selector.currentText()
        date = self.record_date_input.date().toString("yyyy-MM-dd")

        if task_name:
            if task_name in self.records:
                self.records[task_name] = [record for record in self.records[task_name] if record["date"] != date]
                self.data_manager.save_data()  # データを保存
                self.show_info_message("Progress deleted successfully!")
        else:
            self.show_error_message("No task to delete progress for!")

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

        target_amount = task["target_amount"]  # 目標量
        start_date = datetime.strptime(task["start_date"], "%Y-%m-%d")
        end_date = datetime.strptime(task["end_date"], "%Y-%m-%d")

        try:
            record_dates = [datetime.strptime(record["date"], "%Y-%m-%d") for record in self.records[task_name]]
            record_progress_amounts = [record["progress_amount"] for record in self.records[task_name]]
        except ValueError as e:
            self.show_error_message(f"Error in date format: {e}")
            return

        if not record_dates:
            self.show_error_message("No progress records!")
            return

        record_dates = [record_dates[0] - timedelta(days=1)] + record_dates  # 前日の日付を追加

        cumulative_progress_list = []
        cumulative_progress = 0
        for progress in record_progress_amounts:
            cumulative_progress += progress
            cumulative_progress_list.append(cumulative_progress)

        remaining_amounts = [target_amount] + [target_amount - progress for progress in cumulative_progress_list]

        ideal_remaining = [target_amount - (target_amount * (i / (end_date - (start_date - timedelta(days=1))).days)) 
                           for i in range((end_date - (start_date - timedelta(days=1))).days + 1)]
        ideal_dates = [start_date - timedelta(days=1) + timedelta(days=i) 
                       for i in range((end_date - (start_date - timedelta(days=1))).days + 1)]

        sns.set(style="whitegrid")
        fig, ax = plt.subplots(figsize=(12, 8))

        img = mpimg.imread('background1.jpg')
        ax.imshow(img, extent=[mdates.date2num(start_date - timedelta(days=1)), mdates.date2num(end_date), 0, target_amount], aspect='auto', zorder=-1)

        if len(record_dates) > 1:
            ax.plot(record_dates, remaining_amounts, label="Actual Progress", color="blue", marker="o", zorder=1)

        ax.plot(ideal_dates, ideal_remaining, label="Ideal Progress", linestyle="--", color="red", zorder=1)

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

    def show_error_message(self, message):
        QMessageBox.critical(self, "Error", message)

    def show_info_message(self, message):
        QMessageBox.information(self, "Information", message)