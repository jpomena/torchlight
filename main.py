from src import Database
from src import MetricsCalculator
from src import TaskFilters
from src import MainWindow
from src import Controller


def main():
    database = Database()
    metrics_calculator = MetricsCalculator()
    task_filters = TaskFilters()

    themename = 'darkly'
    main_window = MainWindow(themename)

    controller = Controller(  # noqa: F841
        database, metrics_calculator, task_filters, main_window
    )

    main_window.mainloop()


if __name__ == '__main__':
    main()
