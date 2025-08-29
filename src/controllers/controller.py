from ..models.metrics_calculator import MetricsCalculator
from ..models.tasks_filters import TaskFilters
from ..views.main_window import MainWindow
from ..views.overview_tab import OverviewTab
from ..models.database import Database


class Controller:
    def __init__(
        self,
        database: Database,
        metrics_calculator: MetricsCalculator,
        task_filters: TaskFilters,
        main_window: MainWindow
    ):
        self.db = database
        self.mc = metrics_calculator
        self.tf = task_filters
        self.mw = main_window

        self.get_tasks_data()
        self.create_overview_tab()

    def get_tasks_data(self):
        self.tasks = self.db.get_db_tasks_data()
        self.mc.calculate_task_metrics(self.tasks)

    def create_overview_tab(self):
        overview_tab_parent_frame = self.mw.create_overview_parent_frame()
        self.overview_tab = OverviewTab(overview_tab_parent_frame)
        tags = [
            'Compliance',
            'Consultivo',
            'Contencioso',
            'Contratos',
            'Convênios',
            'Docs. Corporativos',
            'Edital',
            'Imunidades',
            'Locação',
            'Ofício'
        ]
        assignees = ['Lara Magela', 'Débora Rodrigues']
        self.overview_tab.create_paned_windows()
        overview_metrics_treeview = (  # noqa: F841
            self.overview_tab.create_metrics_treeview_widget()
        )
        overview_task_list_treeview = (
            self.overview_tab.create_tasks_treeview_widget()
        )
        self.overview_tab.fill_task_list_treeview(
            overview_task_list_treeview, self.tasks
        )
        self.overview_tab.create_controls_frame()
        self.overview_tab.create_date_filters_entries()
        self.overview_tab.create_tag_filter(tags)
        self.overview_tab.create_assignee_filter(assignees)
        self.overview_tab.create_btns()
