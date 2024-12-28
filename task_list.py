from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QListWidget, QPushButton

def setup_task_list_section(app, layout):
    # タスクリストセクションのセットアップ
    task_list_group = QGroupBox("Task List")
    task_list_group.setStyleSheet("QGroupBox { font-size: 16px; font-weight: bold; }")
    task_list_layout = QVBoxLayout()
    app.task_list = QListWidget()
    task_list_layout.addWidget(app.task_list)

    delete_task_btn = QPushButton("Delete Selected Task")
    delete_task_btn.setStyleSheet("QPushButton { font-size: 14px; }")
    delete_task_btn.clicked.connect(app.delete_task)
    task_list_layout.addWidget(delete_task_btn)

    task_list_group.setLayout(task_list_layout)
    layout.addWidget(task_list_group)

def delete_task(app):
    # タスクを削除する関数
    selected_task = app.task_list.currentItem()
    if selected_task:
        task_name = selected_task.text().split(":")[0]
        app.tasks = [task for task in app.tasks if task["name"] != task_name]
        if task_name in app.records:
            del app.records[task_name]
        app.update_task_list()
        app.update_task_selector()
        app.update_graph_task_selector()
        app.data_manager.save_data()
        app.show_info_message("Task deleted successfully!")
    else:
        app.show_error_message("Please select a task to delete!")