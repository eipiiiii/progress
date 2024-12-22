import json

class DataManager:
    def __init__(self):
        self.tasks = []
        self.records = {}
        self.load_data()

    def save_data(self):
        # Save data in JSON format
        data = {
            "tasks": self.tasks,
            "records": self.records
        }
        with open("study_progress_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_data(self):
        # Load data from JSON file
        try:
            with open("study_progress_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.tasks = data.get("tasks", [])
                self.records = data.get("records", {})
        except FileNotFoundError:
            # Do nothing if file not found
            pass