import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import datetime
from typing import List, Dict


class MetricsCalculator:
    def __init__(self):
        pass

    def get_tags_means(
        self, tasks: pd.DataFrame
    ) -> Dict[str, Dict[str, float]]:
        tags = tasks['task_tag'].unique().tolist()
        tags_means = {}
        for tag in tags:
            filtered_tasks_df = tasks[tasks['task_tag'] == tag]
            tags_means[tag]['reaction_time_mean'] = (
                filtered_tasks_df['task_reaction_time'].mean()
            )
            tags_means[tag]['cycle_time_mean'] = (
                filtered_tasks_df['task_cycle_time'].mean()
            )
            tags_means[tag]['lead_time_mean'] = (
                filtered_tasks_df['task_lead_time'].mean()
            )
        return tags_means

    def get_tags_stdevs(
        self, tasks: pd.DataFrame
    ) -> Dict[str, Dict[str, float]]:
        tags = tasks['task_tag'].unique().tolist()
        tags_stdevs = {}
        for tag in tags:
            filtered_tasks_df = tasks[tasks['task_tag'] == tag]
            tags_stdevs[tag]['reaction_time_stdev'] = (
                filtered_tasks_df['task_reaction_time'].std()
            )
            tags_stdevs[tag]['cycle_time_stdev'] = (
                filtered_tasks_df['task_cycle_time'].std()
            )
            tags_stdevs[tag]['lead_time_stdev'] = (
                filtered_tasks_df['task_lead_time'].std()
            )
        return tags_stdevs

    def lead_time_trend(
        self, filtered_tasks: List[Dict[str, str | int]]
    ) -> float:
        tasks_delivery_dates = []
        tasks_lead_times = []
        for task in filtered_tasks:
            task_delivery_date_obj = datetime.strptime(
                task['task_delivery_date'], '%d/%m/%Y'
            )
            tasks_delivery_dates.append(task_delivery_date_obj.timestamp())
            tasks_lead_times.append(task['task_lead_time'])
        X = np.array(tasks_delivery_dates).reshape(-1, 1)
        y = np.array(tasks_lead_times)

        model = LinearRegression()

        model.fit(X, y)
        m_coefficient = model.coef_[0]
        # interception = model.intercept_

        return m_coefficient
