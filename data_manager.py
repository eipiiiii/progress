import json
from PyQt5.QtWidgets import QMessageBox

class DataManager:
    def __init__(self, parent=None):
        self.parent = parent
        self.tasks = []
        self.records = {}
        self.load_data()  # データを読み込む

    def save_data(self):
        # タスクと記録をJSON形式で保存
        data = {
            "tasks": self.tasks,
            "records": self.records
        }
        try:
            with open("study_progress_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            self.show_error_message(f"Failed to save data: {e}")

    def load_data(self):
        # JSONファイルからデータを読み込む
        try:
            with open("study_progress_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.tasks = data.get("tasks", [])
                self.records = data.get("records", {})
        except FileNotFoundError:
            pass
        except Exception as e:
            self.show_error_message(f"Failed to load data: {e}")

    def show_error_message(self, message):
        # エラーメッセージを表示
        if self.parent:
            QMessageBox.critical(self.parent, "Error", message)