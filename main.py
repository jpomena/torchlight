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
        font_path = 'src/assets/Truetypewriter.ttf'
        font_size = 14
        with dpg.font(font_path, font_size, tag="default_font"):
            dpg.add_font_range(0x0020, 0x00FF)
            dpg.add_font_range(0x0100, 0x017F)
            dpg.add_font_range(0x0370, 0x03FF)
            dpg.add_font_range(0x2200, 0x22FF)
    dpg.bind_font('default_font')

    with dpg.theme() as global_theme:

        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(
                dpg.mvThemeCol_WindowBg, (254, 254, 254, 255)
            )
            dpg.add_theme_color(
                    dpg.mvThemeCol_ChildBg, (254, 254, 254, 255)
            )
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (254, 254, 254, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0, 255))
            dpg.add_theme_color(
                    dpg.mvThemeCol_TextDisabled, (80, 80, 80, 255)
            )

            dpg.add_theme_color(
                    dpg.mvThemeCol_Button, (235, 235, 235, 255)
            )
            dpg.add_theme_color(
                    dpg.mvThemeCol_ButtonHovered, (200, 30, 30, 255)
            )
            dpg.add_theme_color(
                    dpg.mvThemeCol_ButtonActive, (160, 0, 0, 255)
            )

            dpg.add_theme_color(
                    dpg.mvThemeCol_FrameBg, (235, 235, 235, 255)
            )
            dpg.add_theme_color(
                    dpg.mvThemeCol_FrameBgHovered, (220, 220, 220, 255)
            )
            dpg.add_theme_color(
                    dpg.mvThemeCol_FrameBgActive, (200, 30, 30, 255)
            )

            dpg.add_theme_color(
                    dpg.mvThemeCol_ScrollbarBg, (240, 240, 240, 255)
            )
            dpg.add_theme_color(
                    dpg.mvThemeCol_ScrollbarGrab, (200, 30, 30, 255)
            )
            dpg.add_theme_color(
                    dpg.mvThemeCol_ScrollbarGrabHovered, (160, 0, 0, 255)
            )

            dpg.add_theme_color(dpg.mvThemeCol_Tab, (240, 240, 240, 255))
            dpg.add_theme_color(
                    dpg.mvThemeCol_TableHeaderBg, (230, 230, 230, 255)
            )
            dpg.add_theme_color(
                    dpg.mvThemeCol_TableBorderStrong, (200, 200, 200, 255)
            )
            dpg.add_theme_color(
                    dpg.mvThemeCol_TableBorderLight, (230, 230, 230, 255)
            )
            dpg.add_theme_color(
                    dpg.mvThemeCol_TableRowBg, (254, 254, 254, 255)
            )
            dpg.add_theme_color(
                    dpg.mvThemeCol_TableRowBgAlt, (248, 248, 248, 255)
            )

            dpg.add_theme_color(
                    dpg.mvThemeCol_Header, (235, 235, 235, 255)
            )
            dpg.add_theme_color(
                    dpg.mvThemeCol_HeaderHovered, (200, 30, 30, 255)
            )
            dpg.add_theme_color(
                    dpg.mvThemeCol_HeaderActive, (160, 0, 0, 255)
            )

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
