import pandas as pd
from typing import Dict
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime


class StatisticsDataframe:
    def create_statistics_df(
        self, tasks: pd.DataFrame
    ) -> pd.DataFrame:
        columns = tasks['task_tag'].drop_duplicates().to_dict()
        rows = [
            'Demandas Abertas'
            'Demandas Fechadas',
            'μ RT (d)',
            'σ RT (d)',
            'μ LT (d)',
            'σ LT (d)',
            'μ CT (d)',
            'σ CT (d)',
            'TT (d)',
            'm RT',
            'm CT'
            'm LT',
            'RT Mín. Estimado (d)',
            'RT Máx. Estimado (d)',
            'CT Mín. Estimado (d)',
            'CT Máx. Estimado (d)',
            'LT Mín. Estimado (d)',
            'LT Máx. Estimado (d)',
            '<RT Mín. Estimado',
            '<CT Mín. Estimado',
            '<LT Mín. Estimado',
            '<=μ RT',
            '<=μ CT',
            '<=μ LT',
            '<=RT Máx. Estimado',
            '<=CT Máx. Estimado',
            '<=LT Máx. Estimado',
            'Dentro do Intervalo'
        ]
        statistics_df = pd.DataFrame(index=rows, columns=columns)

        return statistics_df

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

    def get_tags_trends(
        self, tasks: pd.DataFrame
    ) -> Dict[str, Dict[str, float]]:
        tags = tasks['task_tag'].unique().tolist()
        tags_trends = {}

        for tag in tags:
            filtered_tasks_df = tasks[tasks['task_tag'] == tag]
            tasks_delivery_dates = (
                pd.to_datetime(
                    filtered_tasks_df['task_delivery_date']
                ).tolist())
            tasks_cycle_times = filtered_tasks_df['task_lead_time'].tolist()

            X = np.array(tasks_delivery_dates).reshape(-1, 1)
            y = np.array(tasks_cycle_times)

            model = LinearRegression()

            model.fit(X, y)
            m_coefficient = model.coef_[0]
            # interception = model.intercept_

            tags_trends[tag]['lead_time_trend'] = m_coefficient

        for tag in tags:
            filtered_tasks_df = tasks[tasks['task_tag'] == tag]
            tasks_delivery_dates = (
                pd.to_datetime(
                    filtered_tasks_df['task_delivery_date']
                ).tolist())
            tasks_cycle_times = filtered_tasks_df['task_cycle_time'].tolist()

            X = np.array(tasks_delivery_dates).reshape(-1, 1)
            y = np.array(tasks_cycle_times)

            model = LinearRegression()

            model.fit(X, y)
            m_coefficient = model.coef_[0]
            # interception = model.intercept_

            tags_trends[tag]['lead_cycle_trend'] = m_coefficient

        for tag in tags:
            filtered_tasks_df = tasks[tasks['task_tag'] == tag]
            tasks_delivery_dates = (
                pd.to_datetime(
                    filtered_tasks_df['task_delivery_date']
                ).tolist())
            tasks_reaction_times = (
                filtered_tasks_df['task_reaction_time'].tolist()
            )

            X = np.array(tasks_delivery_dates).reshape(-1, 1)
            y = np.array(tasks_reaction_times)

            model = LinearRegression()

            model.fit(X, y)
            m_coefficient = model.coef_[0]
            # interception = model.intercept_

            tags_trends[tag]['lead_reaction_trend'] = m_coefficient

        return tags_trends

    def get_tasks_takt_times(
        self, tasks: pd.DataFrame, start_date: datetime, end_date: datetime
    ) -> Dict[str, float]:
        tags = tasks['task_tag'].unique().tolist()
        time_interval = end_date - start_date
        takt_times = {}
        for tag in tags:
            filtered_tasks_df = tasks[tasks['task_tag'] == tag]
            tag_task_count = filtered_tasks_df['task_name'].count()
            tag_takt_time = tag_task_count/time_interval
            takt_times[tag] = tag_takt_time

        return takt_times

    def
