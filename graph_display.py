from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QLabel, QComboBox, QPushButton
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import matplotlib.image as mpimg

def setup_graph_display_section(app, layout):
    # グラフ表示セクションのセットアップ
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

def show_graph(app):
    task_name = app.task_summary_selector.currentText()
    if not task_name:
        app.show_error_message("No task selected!")
        return

    task = next((task for task in app.tasks if task["name"] == task_name), None)
    if not task:
        app.show_error_message("Selected task not found!")
        return

    if not app.records.get(task_name):
        app.show_error_message(f"No progress records for {task_name}!")
        return

    target_amount = task["target_amount"]
    start_date = datetime.strptime(task["start_date"], "%Y-%m-%d")
    end_date = datetime.strptime(task["end_date"], "%Y-%m-%d")

    try:
        record_dates = [datetime.strptime(record["date"], "%Y-%m-%d") for record in app.records[task_name]]
        record_progress_amounts = [record["progress_amount"] for record in app.records[task_name]]
    except ValueError as e:
        app.show_error_message(f"Error in date format: {e}")
        return

    if not record_dates:
        app.show_error_message("No progress records!")
        return

    record_dates = [record_dates[0] - timedelta(days=1)] + record_dates

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