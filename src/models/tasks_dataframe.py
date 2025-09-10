import pandas as pd
from typing import Dict
from ..utils.date_helper import get_business_days


class TasksDataframe:
    def __init__(self):
        pass

    def calculate_task_metrics(self, tasks: pd.DataFrame):
        date_columns = [
            'task_backlog_date', 'task_start_date',
            'task_done_date', 'task_delivery_date'
        ]
        for col in date_columns:
            tasks[col] = pd.to_datetime(
                tasks[col], format='%d/%m/%Y', errors='coerce'
            )

        tasks['task_reaction_time'] = tasks.apply(
            lambda row: get_business_days(
                row['task_backlog_date'].date(), row['task_start_date'].date()
            ),
            axis=1
        )
        tasks['task_cycle_time'] = tasks.apply(
            lambda row: get_business_days(
                row['task_start_date'].date(), row['task_done_date'].date()
            ),
            axis=1
        )
        tasks['task_lead_time'] = tasks.apply(
            lambda row: get_business_days(
                row['task_backlog_date'].date(),
                row['task_delivery_date'].date()
            ),
            axis=1
        )

    def get_task_count_by_tag(self, tasks: pd.DataFrame) -> Dict[str, int]:
        tags = tasks['task_tag'].unique().tolist()
        task_count_by_tag = {}

        for tag in tags:
            task_count = tasks[tasks['task_tag'] == tag].shape[0]
            task_count_by_tag[tag] = task_count

        return task_count_by_tag
