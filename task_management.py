from datetime import datetime

def create_task(app):
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
        app.update_task_summary_selector()
        app.update_task_summary()
        app.task_name_input.clear()
        app.target_amount_input.setValue(0)
        app.data_manager.save_data()
        app.show_info_message("Task created successfully!")
    else:
        app.show_error_message("Incomplete task information!")

def delete_task(app):
    selected_task = app.task_list.currentItem()
    if selected_task:
        task_name = selected_task.text().split(":")[0]
        app.tasks = [task for task in app.tasks if task["name"] != task_name]
        if task_name in app.records:
            del app.records[task_name]
        app.update_task_list()
        app.update_task_selector()
        app.update_task_summary_selector()
        app.update_task_summary()
        app.data_manager.save_data()
        app.show_info_message("Task deleted successfully!")
    else:
        app.show_error_message("Please select a task to delete!")

def update_task_list(app):
    app.task_list.clear()
    for task in app.tasks:
        app.task_list.addItem(f"{task['name']}: {task['target_amount']} ({task['start_date']} ~ {task['end_date']})")

def update_task_selector(app):
    app.task_selector.clear()
    for task in app.tasks:
        app.task_selector.addItem(task["name"])

def update_graph_task_selector(app):
    app.graph_task_selector.clear()
    for task in app.tasks:
        app.graph_task_selector.addItem(task["name"])

def update_task_summary_selector(app):
    app.task_summary_selector.clear()
    for task in app.tasks:
        app.task_summary_selector.addItem(task["name"])

def update_task_summary(app):
    task_name = app.task_summary_selector.currentText()
    if task_name:
        task = next((task for task in app.tasks if task["name"] == task_name), None)
        if task:
            total_target_amount = task["target_amount"]
            total_progress_amount = task["progress_amount"]
            remaining_amount = total_target_amount - total_progress_amount

            today = datetime.now().date()
            end_date = datetime.strptime(task["end_date"], "%Y-%m-%d").date()
            remaining_days = (end_date - today).days

            if remaining_days > 0:
                daily_target = remaining_amount / remaining_days
            else:
                daily_target = 0

            app.daily_target_label.setText(f"Daily Target: {daily_target:.2f}")
            app.total_progress_label.setText(f"Total Progress: {total_progress_amount} / {total_target_amount}")
        else:
            app.daily_target_label.setText("Daily Target: N/A")
            app.total_progress_label.setText("Total Progress: N/A")
    else:
        app.daily_target_label.setText("Daily Target: N/A")
        app.total_progress_label.setText("Total Progress: N/A")