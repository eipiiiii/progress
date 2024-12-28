from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QLabel, QComboBox, QPushButton

def setup_graph_display_section(app, layout):
    graph_group = QGroupBox("Display Graph")
    graph_group.setStyleSheet("QGroupBox { font-size: 16px; font-weight: bold; }")
    graph_layout = QVBoxLayout()
    app.graph_task_selector = QComboBox()
    app.update_graph_task_selector()
    show_graph_btn = QPushButton("Show Graph")
    show_graph_btn.setStyleSheet("QPushButton { font-size: 14px; }")
    show_graph_btn.clicked.connect(app.show_graph)
    graph_layout.addWidget(QLabel("Select Task"))
    graph_layout.addWidget(app.graph_task_selector)
    graph_layout.addWidget(show_graph_btn)
    graph_group.setLayout(graph_layout)
    layout.addWidget(graph_group)