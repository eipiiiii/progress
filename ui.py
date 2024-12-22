from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QGroupBox, QComboBox, QFormLayout, QSpinBox, QDateEdit, QListWidget
)
from PyQt5.QtCore import QDate
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates
from data_manager import DataManager

class StudyProgressApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Study Progress Tracker")
        self.setGeometry(100, 100, 600, 400)
        
        self.data_manager = DataManager()
        self.tasks = self.data_manager.tasks
        self.records = self.data_manager.records

        self.init_ui()

    def init_ui(self):
        # メインウィジェットとレイアウト
        central_widget = QWidget()
        layout = QVBoxLayout()

        # 新規タスク作成セクション
        task_group = QGroupBox("新規タスク作成")
        task_layout = QVBoxLayout()
        task_form = QFormLayout()
        self.task_name_input = QLineEdit()
        self.target_amount_input = QSpinBox()  # 目標量の入力
        self.target_amount_input.setMaximum(1000)
        self.start_date_input = QDateEdit()
        self.start_date_input.setDate(QDate.currentDate())
        self.start_date_input.setCalendarPopup(True)
        self.end_date_input = QDateEdit()
        self.end_date_input.setDate(QDate.currentDate().addDays(7))
        self.end_date_input.setCalendarPopup(True)
        create_task_btn = QPushButton("タスクを作成")
        create_task_btn.clicked.connect(self.create_task)

        task_form.addRow("タスク名", self.task_name_input)
        task_form.addRow("目標量", self.target_amount_input)
        task_form.addRow("開始日", self.start_date_input)
        task_form.addRow("目標終了日", self.end_date_input)
        task_layout.addLayout(task_form)
        task_layout.addWidget(create_task_btn)
        task_group.setLayout(task_layout)
        layout.addWidget(task_group)

        # タスクリストセクション
        task_list_group = QGroupBox("タスクリスト")
        task_list_layout = QVBoxLayout()
        self.task_list = QListWidget()
        task_list_layout.addWidget(self.task_list)

        # タスク削除ボタン
        delete_task_btn = QPushButton("選択したタスクを削除")
        delete_task_btn.clicked.connect(self.delete_task)
        task_list_layout.addWidget(delete_task_btn)

        task_list_group.setLayout(task_list_layout)
        layout.addWidget(task_list_group)

        # 進捗記録セクション
        record_group = QGroupBox("進捗記録")
        record_layout = QVBoxLayout()
        record_form = QFormLayout()
        self.task_selector = QComboBox()
        self.update_task_selector()
        self.record_date_input = QDateEdit()
        self.record_date_input.setDate(QDate.currentDate())
        self.record_date_input.setCalendarPopup(True)
        self.progress_amount_input = QSpinBox()  # 進捗量の入力
        self.progress_amount_input.setMaximum(1000)
        record_task_btn = QPushButton("進捗を記録")
        record_task_btn.clicked.connect(self.record_progress)

        record_form.addRow("タスク", self.task_selector)
        record_form.addRow("日付", self.record_date_input)
        record_form.addRow("進捗量", self.progress_amount_input)
        record_layout.addLayout(record_form)
        record_layout.addWidget(record_task_btn)
        record_group.setLayout(record_layout)
        layout.addWidget(record_group)

        # グラフ表示セクション
        graph_group = QGroupBox("グラフ表示")
        graph_layout = QVBoxLayout()
        self.graph_task_selector = QComboBox()
        self.update_graph_task_selector()
        show_graph_btn = QPushButton("グラフを表示")
        show_graph_btn.clicked.connect(self.show_graph)
        graph_layout.addWidget(QLabel("タスクを選択"))
        graph_layout.addWidget(self.graph_task_selector)
        graph_layout.addWidget(show_graph_btn)
        graph_group.setLayout(graph_layout)
        layout.addWidget(graph_group)

        # レイアウトをウィジェットにセット
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.update_task_list()

    def create_task(self):
        # タスクの新規作成
        task_name = self.task_name_input.text()
        target_amount = self.target_amount_input.value()  # 目標量
        start_date = self.start_date_input.date()
        end_date = self.end_date_input.date()

        # 日付を計算して期間を取得
        start_date_obj = datetime(start_date.year(), start_date.month(), start_date.day())
        end_date_obj = datetime(end_date.year(), end_date.month(), end_date.day())
        duration = (end_date_obj - start_date_obj).days

        if task_name and target_amount > 0 and duration > 0:
            task = {
                "name": task_name, 
                "target_amount": target_amount,  # 目標量
                "duration": duration, 
                "progress_amount": 0,  # 進捗量を0に初期化
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
        else:
            print("タスクの情報が不足しています！")

    def delete_task(self):
        selected_task = self.task_list.currentItem()  # 選択されたタスクを取得
        if selected_task:
            task_name = selected_task.text().split(":")[0]  # タスク名を抽出
            # タスクの削除
            self.tasks = [task for task in self.tasks if task["name"] != task_name]
            if task_name in self.records:
                del self.records[task_name]
            self.update_task_list()
            self.update_task_selector()
            self.update_graph_task_selector()
            self.data_manager.save_data()  # データを保存
        else:
            print("削除するタスクを選択してください！")

    def record_progress(self):
        task_name = self.task_selector.currentText()
        date = self.record_date_input.date().toString("yyyy-MM-dd")
        progress_amount = self.progress_amount_input.value()  # 新たに入力された進捗量

        if task_name and progress_amount > 0:
            if task_name not in self.records:
                self.records[task_name] = []

            # 既存の記録があるか確認
            existing_record = next((record for record in self.records[task_name] if record["date"] == date), None)
            if existing_record:
                # 同じ日に進捗が記録されていた場合は上書き
                existing_record["progress_amount"] = progress_amount
            else:
                # 新たに進捗を追加
                self.records[task_name].append({"date": date, "progress_amount": progress_amount})

            # 累積進捗量を計算
            cumulative_progress = 0
            for record in self.records[task_name]:
                cumulative_progress += record["progress_amount"]

            # 累積進捗量を更新（グラフ用）
            task = next((task for task in self.tasks if task["name"] == task_name), None)
            if task:
                task["progress_amount"] = cumulative_progress
                print(f"{task_name} の累積進捗量が更新されました: {cumulative_progress}")

            self.data_manager.save_data()  # データを保存
        else:
            print("記録するタスクがありません！")

    def update_task_list(self):
        self.task_list.clear()
        for task in self.tasks:
            self.task_list.addItem(f"{task['name']}: {task['target_amount']}（{task['start_date']} ~ {task['end_date']}）")

    def update_task_selector(self):
        self.task_selector.clear()
        for task in self.tasks:
            self.task_selector.addItem(task["name"])

    def update_graph_task_selector(self):
        self.graph_task_selector.clear()
        for task in self.tasks:
            self.graph_task_selector.addItem(task["name"])

    def show_graph(self):
        # グラフ表示処理
        task_name = self.graph_task_selector.currentText()
        if not task_name:
            print("タスクが選択されていません！")
            return

        task = next((task for task in self.tasks if task["name"] == task_name), None)
        if not task:
            print("選択されたタスクが見つかりません！")
            return

        if not self.records.get(task_name):
            print(f"{task_name} の進捗記録がありません！")
            return

        # データの準備
        target_amount = task["target_amount"]  # 目標量
        start_date = datetime.strptime(task["start_date"], "%Y-%m-%d")
        end_date = datetime.strptime(task["end_date"], "%Y-%m-%d")

        # 実際の進捗のデータ
        try:
            record_dates = [datetime.strptime(record["date"], "%Y-%m-%d") for record in self.records[task_name]]
            record_progress_amounts = [record["progress_amount"] for record in self.records[task_name]]
        except ValueError as e:
            print(f"日付形式にエラーがあります: {e}")
            return

        if not record_dates:
            print("進捗記録がありません！")
            return

        record_dates = [record_dates[0] - timedelta(days=1)] + record_dates  # 1日前の日付を追加

        # 累積進捗量を計算
        cumulative_progress = 0
        cumulative_progress_list = []
        for progress in record_progress_amounts:
            cumulative_progress += progress
            cumulative_progress_list.append(cumulative_progress)

        # 実際の残量（目標量 - 累積進捗量）
        remaining_amounts = [target_amount] + [target_amount - progress for progress in cumulative_progress_list]

        # 理想進捗度（残量として表現、初期状態は目標量）
        ideal_remaining = [target_amount] + [
            target_amount - (target_amount * (i / (end_date - (start_date - timedelta(days=1))).days)) 
            for i in range((end_date - (start_date - timedelta(days=1))).days + 1)
        ]
        ideal_dates = [start_date - timedelta(days=1)] + [
            start_date - timedelta(days=1) + timedelta(days=i) 
            for i in range((end_date - (start_date - timedelta(days=1))).days + 1)
        ]

        # グラフ描画
        plt.figure(figsize=(10, 6))

        # 実際の進捗の残量を描画
        if len(record_dates) > 1:
            plt.plot(record_dates, remaining_amounts, label="実際の進捗", color="blue", marker="o")

        # 理想進捗度を描画
        plt.plot(ideal_dates, ideal_remaining, label="理想進捗", linestyle="--", color="red")

        # グラフ設定
        plt.title(f"{task_name} の進捗グラフ")
        plt.xlabel("日付")
        plt.ylabel("残量")
        plt.xticks(rotation=45)
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.legend()
        plt.tight_layout()
        plt.grid(True)

        plt.show()