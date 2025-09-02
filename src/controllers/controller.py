from ..models.metrics_calculator import MetricsCalculator
from ..views.main_window import MainWindow
from ..views.overview_tab import OverviewTab
from ..models.database import Database
from ..models.tasks_dataframe import TasksDataframe
from ..models.statistics_dataframe import StatisticsDataframe


class Controller:
    def __init__(
        self,
        database: Database,
        metrics_calculator: MetricsCalculator,
        tasks_dataframe: TasksDataframe,
        statistics_dataframe: StatisticsDataframe,
        main_window: MainWindow
    ):
        self.db = database
        self.mc = metrics_calculator
        self.mw = main_window
        self.tdf = tasks_dataframe
        self.sdf = statistics_dataframe

        self.create_dataframes()
        self.create_overview_tab()

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
        self.overview_metrics_treeview = (  # noqa: F841
            self.overview_tab.create_metrics_treeview_widget()
        )
        self.overview_task_list_treeview = (
            self.overview_tab.create_tasks_treeview_widget()
        )
        self.overview_tab.create_controls_frame()
        self.overview_tab.create_date_filters_entries()
        self.overview_tab.create_tag_filter(self.tags)
        self.overview_tab.create_assignee_filter(self.assignees)
        self.overview_tab.create_btns()

    def fill_overview_tab(self):
        self.overview_tab.fill_task_list_treeview(
            self.overview_task_list_treeview, self.tasks_df
        )
        tags_means = self.sdf.get_tags_means(self.tasks_df)
        tags_stdevs = self.sdf.get_tags_stdevs(self.tasks_df)
        tags_trends = self.sdf.get_tags_trends(self.tasks_df)
        tags_takt_times = self.sdf.get_tasks_takt_times(self.tasks_df)
        self.sdf.feed_statistics_df(
            self.statistics_df,
            tags_means,
            tags_stdevs,
            tags_trends,
            tags_takt_times,
        )
