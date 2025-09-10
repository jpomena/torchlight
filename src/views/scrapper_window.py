import dearpygui.dearpygui as dpg
from typing import Callable, Dict


class ScrapperWindow:
    def __init__(self):
        self.window_tag = "import_tasks_window"
        self.username_tag = "import_username"
        self.password_tag = "import_password"
        self.list_name_tag = "import_list_name"
        self.driver_path_tag = "import_driver_path"
        self.log_window_tag = "import_log_window"
        self.start_extraction_tag = 'start_extraction_button'
        self.stop_extraction_tag = 'stop_extraction_button'
        self.edit_db_window_tag = 'scrapper_edit_db_window'
        self.edit_db_table_tag = 'scrapper_edit_db_table'
        self.edit_db_table_container_tag = 'scrapper_edit_db_table_container'

    def create_window(
        self,
        start_callback: Callable,
        stop_callback: Callable,
        edit_db_window_callback: Callable,
        save_callback: Callable,
        import_callback: Callable,
    ):
        with dpg.window(
            label='Importar Atividades do ClickUp',
            tag=self.window_tag,
            modal=True,
            show=False,
            width=800,
            height=600
        ):
            with dpg.group():
                dpg.add_text('*Usuário:')
                dpg.add_input_text(tag=self.username_tag, width=-1)
                dpg.add_text('*Senha:')
                dpg.add_input_text(
                    tag=self.password_tag, password=True, width=-1
                )
                dpg.add_text('*Lista:')
                dpg.add_input_text(
                    tag=self.list_name_tag, width=-1
                )
                dpg.add_text('Caminho do Driver:')
                dpg.add_input_text(
                    tag=self.driver_path_tag, width=-1
                )

            dpg.add_spacer(height=10)

            dpg.add_input_text(
                tag=self.log_window_tag,
                multiline=True,
                readonly=True,
                width=-1,
                height=-100
            )

            dpg.add_spacer(height=10)

            with dpg.group(horizontal=True):
                dpg.add_button(
                    label="Iniciar Extração",
                    callback=start_callback,
                    tag=self.start_extraction_tag
                )
                dpg.add_button(
                    label="Parar Extração",
                    callback=stop_callback,
                    tag=self.stop_extraction_tag
                )
                dpg.add_button(
                    label='Ver Atividades Extraídas',
                    callback=lambda: self._toggle_edit_db_window(
                        edit_db_window_callback
                    )
                )
                dpg.add_button(
                    label="Fechar",
                    callback=lambda: dpg.configure_item(
                        self.window_tag, show=False
                    ))

            self._create_edit_db_window(save_callback, import_callback)

    def get_input_values(self) -> Dict[str, str]:
        return {
            "username": dpg.get_value(self.username_tag),
            "password": dpg.get_value(self.password_tag),
            "list_name": dpg.get_value(self.list_name_tag),
            "driver_path": dpg.get_value(self.driver_path_tag)
        }

    def _create_edit_db_window(
        self,
        save_callback: Callable,
        import_callback: Callable
    ):
        with dpg.window(
            label='Editar Atividades',
            tag=self.edit_db_window_tag,
            show=False,
            modal=True,
            width=1280,
            height=720
        ):
            with dpg.group(horizontal=True):
                dpg.add_button(
                    label='Salvar Alterações Manuais',
                    callback=save_callback
                )
                dpg.add_button(
                    label='Exportar Atividades Extraídas',
                    callback=import_callback
                )
                dpg.add_button(
                    label='Fechar',
                    callback=self._close_edit_and_show_scrapper
                )

            with dpg.group(tag=self.edit_db_table_container_tag):
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
                    tag=self.edit_db_table_tag
                )

    def _toggle_edit_db_window(self, edit_db_window_callback: Callable):
        dpg.configure_item(self.window_tag, show=False)
        dpg.split_frame()
        edit_db_window_callback()
        dpg.configure_item(self.edit_db_window_tag, show=True)

    def _close_edit_and_show_scrapper(self):
        dpg.configure_item(self.edit_db_window_tag, show=False)
        dpg.split_frame()
        dpg.configure_item(self.window_tag, show=True)
