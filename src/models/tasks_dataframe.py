import pandas as pd
from typing import Dict


class TasksDataframe:
    def __init__(self):
        pass

    def calculate_task_metrics(self, tasks: pd.DataFrame):
        tasks['task_reaction_time'] = ((pd.to_datetime(
            tasks['task_start_date'], format='%d/%m/%Y'
        ) - pd.to_datetime(
            tasks['task_backlog_date'], format='%d/%m/%Y'
        )) / pd.Timedelta(days=1)).astype(int).clip(lower=1)
        tasks['task_cycle_time'] = ((pd.to_datetime(
            tasks['task_done_date'], format='%d/%m/%Y'
        ) - pd.to_datetime(
            tasks['task_start_date'], format='%d/%m/%Y'
        )) / pd.Timedelta(days=1)).astype(int).clip(lower=1)
        tasks['task_lead_time'] = ((pd.to_datetime(
            tasks['task_delivery_date'], format='%d/%m/%Y'
        ) - pd.to_datetime(
            tasks['task_backlog_date'], format='%d/%m/%Y'
        )) / pd.Timedelta(days=1)).astype(int).clip(lower=1)

    def get_task_count_by_tag(self, tasks: pd.DataFrame) -> Dict[str, int]:
        tags = tasks['task_tag'].unique().tolist()
        task_count_by_tag = {}

        for tag in tags:
            task_count = tasks[tasks['task_tag'] == tag].shape[0]
            task_count_by_tag[tag] = task_count

        return task_count_by_tag
