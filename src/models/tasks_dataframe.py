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

        def calculate_reaction_time(row):
            backlog_date = row['task_backlog_date']
            start_date = row['task_start_date']
            if pd.isna(backlog_date) is False and pd.isna(start_date) is False:
                return get_business_days(
                    backlog_date.date(), start_date.date()
                                         )
            return pd.NA

        def calculate_cycle_time(row):
            start_date = row['task_start_date']
            done_date = row['task_done_date']
            if pd.isna(start_date) is False and pd.isna(done_date) is False:
                return get_business_days(start_date.date(), done_date.date())
            return pd.NA

        def calculate_lead_time(row):
            backlog_date = row['task_backlog_date']
            delivery_date = row['task_delivery_date']
            if pd.isna(backlog_date) is False and pd.isna(delivery_date) is False:  # noqa: E501
                return get_business_days(
                    backlog_date.date(), delivery_date.date()
                                         )
            return pd.NA

        tasks['task_reaction_time'] = (
            tasks.apply(calculate_reaction_time, axis=1)
                                       )
        tasks['task_cycle_time'] = tasks.apply(calculate_cycle_time, axis=1)
        tasks['task_lead_time'] = tasks.apply(calculate_lead_time, axis=1)

    def get_task_count_by_tag(self, tasks: pd.DataFrame) -> Dict[str, int]:
        tags = tasks['task_tag'].unique().tolist()
        task_count_by_tag = {}

        for tag in tags:
            task_count = tasks[tasks['task_tag'] == tag].shape[0]
            task_count_by_tag[tag] = task_count

        return task_count_by_tag
