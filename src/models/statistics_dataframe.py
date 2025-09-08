import pandas as pd
from typing import Dict
from sklearn.linear_model import LinearRegression
from datetime import datetime


class StatisticsDataframe:
    def create_statistics_df(
        self, tasks: pd.DataFrame
    ) -> pd.DataFrame:
        columns = tasks['task_tag'].drop_duplicates().tolist()
        rows = [
            'Demandas Fechadas',
            'μ RT (d)',
            'σ RT (d)',
            'RT Mín. (d)',
            'RT Máx. (d)',
            '< RT Mín.',
            '<= μ RT',
            '<= RT Máx.',
            'm RT',
            'μ CT (d)',
            'σ CT (d)',
            'CT Mín. (d)',
            'CT Máx. (d)',
            '< CT Mín.',
            '<= μ CT',
            '<= CT Máx.',
            'm CT',
            'μ LT (d)',
            'σ LT (d)',
            'LT Mín. (d)',
            'LT Máx. (d)',
            '< LT Mín.',
            '<= μ LT',
            '<= LT Máx.',
            'm LT',
            'TT (d)',
        ]
        statistics_df = pd.DataFrame(index=rows, columns=columns)

        return statistics_df

    def get_tags_means(
        self, tasks: pd.DataFrame
    ) -> Dict[str, Dict[str, float]]:
        tags = tasks['task_tag'].unique().tolist()
        tags_means = {}
        for tag in tags:
            tags_means[tag] = {}

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
            tags_stdevs[tag] = {}

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
            tags_trends[tag] = {}
            filtered_tasks_df = tasks[tasks['task_tag'] == tag].copy()

            delivery_dates = pd.to_datetime(
                filtered_tasks_df['task_delivery_date'], format='%d/%m/%Y'
            )
            min_date = delivery_dates.min()
            X = (delivery_dates - min_date).dt.days.values.reshape(-1, 1)

            for metric in ['reaction', 'cycle', 'lead']:
                model = LinearRegression()
                y = filtered_tasks_df[f'task_{metric}_time'].values

                if len(X) > 1:
                    model.fit(X, y)
                    m_coefficient = 10*model.coef_[0]
                else:
                    m_coefficient = 0

                tags_trends[tag][f'{metric}_time_trend'] = m_coefficient

        return tags_trends

    def get_tasks_takt_times(
        self, tasks: pd.DataFrame, start_date: datetime, end_date: datetime
    ) -> Dict[str, float]:
        tags = tasks['task_tag'].unique().tolist()
        takt_times = {}

        time_interval = (end_date - start_date).days

        for tag in tags:
            filtered_tasks_df = tasks[tasks['task_tag'] == tag]
            tag_task_count = filtered_tasks_df['task_name'].count()

            if time_interval > 0:
                tag_takt_time = tag_task_count / time_interval
            else:
                tag_takt_time = 0

            takt_times[tag] = tag_takt_time

        return takt_times

    def fill_task_count(
        self,
        statistics: pd.DataFrame,
        task_count: Dict[str, int]
    ):
        statistics.loc['Demandas Fechadas'] = task_count

    def fill_base_statistics(
        self,
        statistics: pd.DataFrame,
        means: Dict[str, Dict[str, float]],
        stdevs: Dict[str, Dict[str, float]],
        trends: Dict[str, Dict[str, float]],
        takt_times: Dict[str, float]
    ):
        tags = statistics.columns.tolist()
        metrics_names = {
            'RT': 'reaction_time',
            'CT': 'cycle_time',
            'LT': 'lead_time'
        }

        for key, value in metrics_names.items():

            statistics.loc[f'μ {key} (d)'] = {
                tag: means[tag][f'{value}_mean'] for tag in tags
            }
            statistics.loc[f'σ {key} (d)'] = {
                tag: stdevs[tag][f'{value}_stdev'] for tag in tags
            }
            statistics.loc[f'm {key}'] = {
                tag: trends[tag][f'{value}_trend'] for tag in tags
            }

        statistics.loc['TT (d)'] = takt_times

    def fill_min_max_times(self, statistics: pd.DataFrame):
        for metric in ['RT', 'CT', 'LT']:
            statistics.loc[f'{metric} Mín. (d)'] = (
                statistics.loc[f'μ {metric} (d)'] - statistics.loc[f'σ {metric} (d)']  # noqa: E501
            ).clip(lower=1)
            statistics.loc[f'{metric} Máx. (d)'] = (
                statistics.loc[f'μ {metric} (d)'] + statistics.loc[f'σ {metric} (d)']  # noqa: E501
            )

    def format_numbers(self, statistics: pd.DataFrame):
        def round_row(row):
            numeric_row = pd.to_numeric(row, errors='coerce')

            if row.name in ['m RT', 'm CT', 'm LT']:
                return numeric_row.round(2)
            elif row.name == 'Demandas Fechadas':
                filled_row = numeric_row.fillna(0)
                return filled_row.astype(int)
            else:
                return numeric_row.round(1)

        statistics.loc[:, :] = statistics.apply(round_row, axis=1)

    def fill_percentages(
        self,
        tasks: pd. DataFrame,
        statistics: pd.DataFrame
    ):
        tags = tasks['task_tag'].unique().tolist()
        times = ['reaction', 'cycle', 'lead']
        metrics_short = ['RT', 'CT', 'LT']
        under_min_rows = ['< RT Mín.', '< CT Mín.', '< LT Mín.']
        under_mean_rows = ['<= μ RT', '<= μ CT', '<= μ LT']
        under_max_rows = ['<= RT Máx.', '<= CT Máx.', '<= LT Máx.']

        for tag in tags:
            for percentage, metric, metric_short in zip(under_min_rows, times, metrics_short):  # noqa: E501
                min_value = statistics.loc[
                    f'{metric_short} Mín. (d)', tag
                ]

                tag_mask = tasks['task_tag'] == tag
                value_mask = tasks[f'task_{metric}_time'] < min_value

                tag_task_count = tasks[tag_mask].shape[0]
                filtered_tag_task_count = tasks[tag_mask & value_mask].shape[0]

                if tag_task_count > 0:
                    statistics.loc[percentage, tag] = 100*(
                        filtered_tag_task_count / tag_task_count
                    )
                else:
                    statistics.loc[percentage, tag] = 0

        for tag in tags:
            for percentage, metric, metric_short in zip(under_mean_rows, times, metrics_short):  # noqa: E501
                min_value = statistics.loc[
                    f'μ {metric_short} (d)', tag
                ]

                tag_mask = tasks['task_tag'] == tag
                value_mask = tasks[f'task_{metric}_time'] <= min_value

                tag_task_count = tasks[tag_mask].shape[0]
                filtered_tag_task_count = tasks[tag_mask & value_mask].shape[0]

                if tag_task_count > 0:
                    statistics.loc[percentage, tag] = 100*(
                        filtered_tag_task_count / tag_task_count
                    )
                else:
                    statistics.loc[percentage, tag] = 0

        for tag in tags:
            for percentage, metric, metric_short in zip(under_max_rows, times, metrics_short):  # noqa: E501
                min_value = statistics.loc[
                    f'{metric_short} Máx. (d)', tag
                ]

                tag_mask = tasks['task_tag'] == tag
                value_mask = tasks[f'task_{metric}_time'] <= min_value

                tag_task_count = tasks[tag_mask].shape[0]
                filtered_tag_task_count = tasks[tag_mask & value_mask].shape[0]

                if tag_task_count > 0:
                    statistics.loc[percentage, tag] = 100*(
                        filtered_tag_task_count / tag_task_count
                    )
                else:
                    statistics.loc[percentage, tag] = 0
