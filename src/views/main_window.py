import dearpygui.dearpygui as dpg
from typing import List, Callable
from .overview_tab import OverviewTab
from .scrapper_window import ScrapperWindow
from .tag_tab import TagTab


class MainWindow:
    def __init__(self):
        self.overview_tab = OverviewTab()
        self.edit_db_window_tag = 'edit_db_window'
        self.scrapper_window = ScrapperWindow()
        self.tag_tabs = {}

    def create_main_window(
        self,
        tags: List[str],
        assignees: List[str],
        apply_filters_callback: Callable,
        sort_tasks_callback: Callable,
        edit_db_window_callback: Callable,
        open_import_window_callback: Callable
    ):
        with dpg.window(
            tag="primary_window",
            no_title_bar=True,
            no_resize=True,
            no_move=True
        ):
            with dpg.tab_bar():
                self.overview_tab.create_tab(
                    tags=tags,
                    assignees=assignees,
                    apply_filters_callback=apply_filters_callback,
                    sort_tasks_callback=sort_tasks_callback,
                    edit_db_window_callback=edit_db_window_callback
                )
                for tag in tags:
                    if tag != 'Todos':
                        tag_tab = TagTab()
                        tag_tab.create_tab(tag, assignees)
                        self.tag_tabs[tag] = tag_tab

        dpg.set_primary_window("primary_window", True)

        self._create_edit_db_window(
            open_import_window_callback=open_import_window_callback
        )

    def _create_edit_db_window(self, open_import_window_callback: Callable):
        with dpg.window(
            label='Editar Atividades',
            tag=self.edit_db_window_tag,
            show=False,
            modal=True,
            width=1280,
            height=720
        ):
            with dpg.group(horizontal=True):
                dpg.add_button(label='Salvar Alterações')
                dpg.add_button(
                    label='Importar Atividades do ClickUp',
                    callback=open_import_window_callback
                    )
                dpg.add_button(
                    label='Fechar',
                    callback=lambda: dpg.configure_item(
                        self.edit_db_window_tag, show=False
                    ))

            with dpg.group(tag='edit_db_table_container'):
                dpg.table(
                    header_row=True,
                    resizable=True,
                    policy=dpg.mvTable_SizingStretchSame,
                    freeze_rows=1,
                    scrollY=True,
                    row_background=True,
                    borders_outerH=True,
                    borders_innerV=True,
                    borders_innerH=True,
                    borders_outerV=True,
                    tag="edit_db_table"
                )
