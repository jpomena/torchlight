from src import Database
from src import MetricsCalculator
from src import MainWindow
from src import Controller
from src import TasksDataframe
from src import StatisticsDataframe


def main():
    database = Database()
    metrics_calculator = MetricsCalculator()
    tasks_dataframe = TasksDataframe()
    statistics_dataframe = StatisticsDataframe()

    themename = 'darkly'
    main_window = MainWindow(themename)

    controller = Controller(  # noqa: F841
        database,
        metrics_calculator,
        tasks_dataframe,
        statistics_dataframe
        main_window
    )

    main_window.mainloop()


if __name__ == '__main__':
    main()
