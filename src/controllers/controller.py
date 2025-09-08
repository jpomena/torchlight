from ..views.main_window import MainWindow
from ..views.overview_tab import OverviewTab
from ..models.database import Database
from ..models.tasks_dataframe import TasksDataframe
from ..models.statistics_dataframe import StatisticsDataframe
import pandas as pd
from datetime import datetime


class Controller:
    def __init__(
        self,
        database: Database,
        tasks_dataframe: TasksDataframe,
        statistics_dataframe: StatisticsDataframe,
        main_window: MainWindow
    ):
        self.db = database
        self.mw = main_window
        self.tdf = tasks_dataframe
        self.sdf = statistics_dataframe

        self.create_dataframes()
        self.create_overview_tab()
        self.fill_overview_tab()

    def create_dataframes(self):
        self.tasks_df = self.db.create_tasks_df()
        self.tdf.calculate_task_metrics(self.tasks_df)
        self.statistics_df = self.sdf.create_statistics_df(self.tasks_df)

    def create_overview_tab(self):
        overview_tab_parent_frame = self.mw.create_overview_parent_frame()
        self.overview_tab = OverviewTab(overview_tab_parent_frame)
        self.tags = self.tasks_df['task_tag'].unique().tolist()
        self.assignees = self.tasks_df['task_assignee'].unique().tolist()
        self.overview_tab.create_paned_windows()
        self.overview_tab.create_controls_frame()
        self.overview_metrics_treeview = (
            self.overview_tab.create_metrics_treeview_widget(
                self.statistics_df
            ))
        self.overview_task_list_treeview = (
            self.overview_tab.create_tasks_treeview_widget(self.tasks_df)
        )

        self.overview_tab.create_date_filters_entries()
        self.overview_tab.create_tag_filter(self.tags)
        self.overview_tab.create_assignee_filter(self.assignees)
        self.overview_tab.create_btns(self.apply_filters)

    def _update_overview_data(self, tasks_df: pd.DataFrame):
        if tasks_df.empty:
            self.overview_tab.fill_task_list_treeview(tasks_df)
            self.overview_tab.fill_metrics_treeview(
                self.statistics_df,
                self.overview_metrics_treeview
            )
            return

        self.overview_tab.fill_task_list_treeview(
            self.overview_task_list_treeview, tasks_df
        )

        statistics_df = self.sdf.create_statistics_df(tasks_df)

        tags_means = self.sdf.get_tags_means(tasks_df)
        tags_stdevs = self.sdf.get_tags_stdevs(tasks_df)
        tags_trends = self.sdf.get_tags_trends(tasks_df)

        start_date_str = self.overview_tab.start_date_entry.entry.get()
        end_date_str = self.overview_tab.end_date_entry.entry.get()
        start_date = datetime.strptime(start_date_str, '%d/%m/%Y')
        end_date = datetime.strptime(end_date_str, '%d/%m/%Y')

        tags_takt_times = self.sdf.get_tasks_takt_times(
            tasks_df, start_date, end_date
        )
        task_count_by_tag = self.tdf.get_task_count_by_tag(tasks_df)

        self.sdf.fill_task_count(statistics_df, task_count_by_tag)
        self.sdf.fill_base_statistics(
            statistics_df,
            tags_means,
            tags_stdevs,
            tags_trends,
            tags_takt_times,
        )
        self.sdf.fill_min_max_times(statistics_df)
        self.sdf.fill_percentages(tasks_df, statistics_df)
        self.sdf.format_numbers(statistics_df)

        self.overview_tab.fill_metrics_treeview(
            statistics_df, self.overview_metrics_treeview
        )

    def fill_overview_tab(self):
        self._update_overview_data(self.tasks_df)

    def apply_filters(self):
        filtered_df = self.tasks_df.copy()

        start_date_str = self.overview_tab.start_date_entry.entry.get()
        end_date_str = self.overview_tab.end_date_entry.entry.get()
        start_date = datetime.strptime(start_date_str, '%d/%m/%Y')
        end_date = datetime.strptime(end_date_str, '%d/%m/%Y')

        delivery_dates = pd.to_datetime(
            filtered_df['task_delivery_date'],
            format='%d/%m/%Y',
            errors='coerce'
        )

        valid_dates_mask = delivery_dates.notna()
        filtered_df = filtered_df[valid_dates_mask]
        delivery_dates = delivery_dates[valid_dates_mask]

        filtered_df = filtered_df[
            (delivery_dates >= start_date) & (delivery_dates <= end_date)
        ]

        selected_tag = self.overview_tab.tag_filter_combobox.get()
        if selected_tag != 'Todos':
            filtered_df = filtered_df[filtered_df['task_tag'] == selected_tag]

        selected_assignee = self.overview_tab.assignees_filter_combobox.get()
        if selected_assignee != 'Todos':
            filtered_df = filtered_df[
                filtered_df['task_assignee'] == selected_assignee
            ]

        self._update_overview_data(filtered_df)
