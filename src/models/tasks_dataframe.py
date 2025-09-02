import pandas as pd
from datetime import datetime


class TasksDataframe:
    def __init__(self):
        pass

    def calculate_task_metrics(self, tasks: pd.DataFrame):
        tasks['reaction_time'] = datetime.strptime(
            tasks['task_start_date'], '%d/%m/%Y'
        ) - datetime.strptime(
            tasks['task_backlog_date'], '%d/%m/%Y'
        )
        tasks['cycle_time'] = datetime.strptime(
            tasks['task_done_date'], '%d/%m/%Y'
        ) - datetime.strptime(
            tasks['task_delivery_date'], '%d/%m/%Y'
        )
        tasks['lead_time'] = datetime.strptime(
            tasks['task_delivery_date'], '%d/%m/%Y'
        ) - datetime.strptime(
            tasks['task_backlog_date'], '%d/%m/%Y'
        )
