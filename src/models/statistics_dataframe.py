import pandas as pd
from typing import Dict, Tuple, List
from sklearn.linear_model import LinearRegression
from datetime import datetime
from ..utils.date_helper import get_business_days
import statsmodels.api as sm


class StatisticsDataframe:
    def create_statistics_df(
        self, tasks: pd.DataFrame
    ) -> pd.DataFrame:
        columns = tasks['task_tag'].drop_duplicates().tolist()
        rows = [
            'Demandas Fechadas',
            'Média RT (d)',
            'Desv. Pad. RT (d)',
            'RT Mín. (d)',
            'RT Máx. (d)',
            '< RT Mín.',
            '<= Média RT',
            '<= RT Máx.',
            'm RT',
            'Média CT (d)',
            'Desv. Pad. CT (d)',
            'CT Mín. (d)',
            'CT Máx. (d)',
            '< CT Mín.',
            '<= Média CT',
            '<= CT Máx.',
            'm CT',
            'Média LT (d)',
            'Desv. Pad. LT (d)',
            'LT Mín. (d)',
            'LT Máx. (d)',
            '< LT Mín.',
            '<= Média LT',
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

        time_interval = get_business_days(start_date.date(), end_date.date())

        for tag in tags:
            filtered_tasks_df = tasks[tasks['task_tag'] == tag]
            tag_task_count = filtered_tasks_df['task_name'].count()

            if time_interval > 0:
                tag_takt_time = tag_task_count / time_interval
            else:
                tag_takt_time = 0

            takt_times[tag] = tag_takt_time

        return takt_times

    def get_loess_fit(
        self,
        tasks: pd.DataFrame,
        time_metric: str,
        date_column: str = 'task_delivery_date',
        frac: float = 0.5
    ) -> Tuple[List[datetime], List[float]]:

        if tasks.empty or tasks[time_metric].isnull().all():
            return [], []

        df = tasks.dropna(subset=[time_metric, date_column]).copy()
        if df.shape[0] < 2:
            return [], []

        df_sorted = df.sort_values(by=date_column)

        x_data = pd.to_numeric(df_sorted[date_column])
        y_data = df_sorted[time_metric]

        loess_results = sm.nonparametric.lowess(
            y_data, x_data, frac=frac, it=0
        )

        x_fit = [pd.to_datetime(val) for val in loess_results[:, 0]]
        y_fit = loess_results[:, 1]

        return x_fit, y_fit

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

            statistics.loc[f'Média {key} (d)'] = {
                tag: means[tag][f'{value}_mean'] for tag in tags
            }
            statistics.loc[f'Desv. Pad. {key} (d)'] = {
                tag: stdevs[tag][f'{value}_stdev'] for tag in tags
            }
            statistics.loc[f'm {key}'] = {
                tag: trends[tag][f'{value}_trend'] for tag in tags
            }

        statistics.loc['TT (d)'] = takt_times

    def fill_min_max_times(self, statistics: pd.DataFrame):
        for metric in ['RT', 'CT', 'LT']:
            statistics.loc[f'{metric} Mín. (d)'] = (
                statistics.loc[f'Média {metric} (d)'] - statistics.loc[f'Desv. Pad. {metric} (d)']  # noqa: E501
            ).clip(lower=1)
            statistics.loc[f'{metric} Máx. (d)'] = (
                statistics.loc[f'Média {metric} (d)'] + statistics.loc[f'Desv. Pad. {metric} (d)']  # noqa: E501
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
        under_mean_rows = ['<= Média RT', '<= Média CT', '<= Média LT']
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
                    f'Média {metric_short} (d)', tag
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
