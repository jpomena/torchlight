import dearpygui.dearpygui as dpg
from src.models.main_database import MainDatabase
from src.models.tasks_dataframe import TasksDataframe
from src.models.statistics_dataframe import StatisticsDataframe
from src.views.main_window import MainWindow
from src.controllers.controller import Controller


def main():
    dpg.create_context()
    dpg.create_viewport(title='Torchlight v0.2', width=1600, height=900)

    with dpg.font_registry():
        font_path = 'src/assets/Quicksand-Bold.otf'
        font_size = 14
        with dpg.font(font_path, font_size, tag="default_font"):
            dpg.add_font_range(0x0020, 0x00FF)
            dpg.add_font_range(0x0100, 0x017F)
            dpg.add_font_range(0x0370, 0x03FF)
            dpg.add_font_range(0x2200, 0x22FF)
    dpg.bind_font('default_font')

    with dpg.theme() as global_theme:

        with dpg.theme_component(dpg.mvAll):
            # dpg.add_theme_color(dpg.mvThemeCol_Text, (224, 211, 175))
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 12)
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 12)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 12)
            dpg.add_theme_style(dpg.mvStyleVar_PopupRounding, 12)
            dpg.add_theme_style(dpg.mvStyleVar_ScrollbarRounding, 12)
            dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 12)
            dpg.add_theme_style(dpg.mvStyleVar_TabRounding, 12)
    dpg.bind_theme(global_theme)

    dpg.setup_dearpygui()

    database = MainDatabase()
    tasks_dataframe = TasksDataframe()
    statistics_dataframe = StatisticsDataframe()

    main_window = MainWindow()

    controller = Controller(
        database=database,
        tasks_dataframe=tasks_dataframe,
        statistics_dataframe=statistics_dataframe,
        main_window=main_window
    )

    controller.initialize_view()

    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == '__main__':
    main()
