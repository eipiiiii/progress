from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QListWidget, QPushButton

def setup_task_list_section(app, layout):
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