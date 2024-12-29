from datetime import datetime

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
        app.update_task_summary()
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
            app.update_task_summary()
            app.show_info_message("Progress deleted successfully!")
    else:
        app.show_error_message("No task to delete progress for!")

def update_progress_amount_input(app):
    task_name = app.task_selector.currentText()
    date = app.record_date_input.date().toString("yyyy-MM-dd")

    if task_name in app.records:
        existing_record = next((record for record in app.records[task_name] if record["date"] == date), None)
        if existing_record:
            app.progress_amount_input.setValue(existing_record["progress_amount"])
        else:
            app.progress_amount_input.setValue(0)
    else:
        app.progress_amount_input.setValue(0)