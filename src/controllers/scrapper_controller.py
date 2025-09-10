import dearpygui.dearpygui as dpg
import threading
from ..views.scrapper_window import ScrapperWindow
from ..utils.aux_functions import log, subscribe
from ..models.puppet_browser import PuppetBrowser
from ..models.html_parser import HTMLParser
from ..models.regex_engine import RegexEngine
from ..models.scrapper_database import ScrapperDatabase


class ScrapperController:
    def __init__(self, view: ScrapperWindow):
        self.view = view
        self.db = ScrapperDatabase()
        self.db.create_tables()
        self.re = RegexEngine()
        self.extracting_data = False
        self.scrapper_df = None
        self.driver = None
        self.headers_map = {
            "task_name": "Nome da Atividade",
            "task_tag": "Etiqueta",
            "task_assignee": "Responsável",
            "task_backlog_date": "Data de Backlog",
            "task_start_date": "Data de Início",
            "task_done_date": "Data de Conclusão",
            "task_delivery_date": "Data de Entrega",
        }

        subscribe("log", self._update_log_window)

    def _update_log_window(self, message: str):
        if dpg.does_item_exist(self.view.log_window_tag):
            current_log = dpg.get_value(self.view.log_window_tag)
            new_log = f"{current_log}{message}\n"
            dpg.set_value(self.view.log_window_tag, new_log)
        else:
            print(message)

    def start_extraction(self):
        dpg.set_value(self.view.log_window_tag, "")
        self.extracting_data = True

        dpg.configure_item(self.view.start_extraction_tag, enabled=False)
        dpg.configure_item(self.view.stop_extraction_tag, enabled=True)

        thread = threading.Thread(target=self._extraction_loop)
        thread.start()

    def stop_extraction(self):
        log("Comando de parada recebido...")
        self.extracting_data = False

    def _extraction_loop(self):
        try:
            credentials = self.view.get_input_values()
            if not all(
                [
                    credentials['username'],
                    credentials['password'],
                    credentials['list_name']
                ]
            ):
                log(
                    "ERRO: Usuário, senha e nome da lista são obrigatórios."
                    )
                return

            log("Iniciando browser...")
            pb = PuppetBrowser(
                username=credentials['username'],
                password=credentials['password'],
                driver_path=credentials['driver_path'] or None,
            )
            self.driver = pb.get_driver()

            log("Acessando ClickUp e fazendo login...")
            pb.access_site()
            pb.login()

            log(f"Buscando a lista '{credentials['list_name']}'...")
            pb.open_list(credentials['list_name'])
            pb.open_list_kanban()
            pb.config_columns()
            target_column = pb.select_column()

            while self.extracting_data:
                log("Procurando próximo card...")
                card_found = pb.open_card(target_column)
                if not card_found:
                    log(
                        "Nenhum card encontrado na coluna de extração."
                    )
                    break

                if not self.extracting_data:
                    break

                html_elements = self._get_task_html_elements(pb)
                soups = self._get_task_soups(html_elements)
                task_data = self._get_task_data(soups)

                self.db.save_task_data(task_data)
                log(f"Atividade '{task_data.get('task_name')}' salva no banco de dados.")  # noqa: E501

                pb.archive_card()

            log("Loop de extração finalizado.")

        except Exception as e:
            log(f"ERRO: {e}")
        finally:
            if self.driver:
                log("Fechando o browser...")
                self.driver.quit()

            self.extracting_data = False
            dpg.configure_item(self.view.start_extraction_tag, enabled=True)
            dpg.configure_item(self.view.stop_extraction_tag, enabled=False)
            log("Processo encerrado.")

    def save_edited_tasks(self):
        if self.scrapper_df is None:
            return

        new_df = self.scrapper_df.copy()

        for i, row in new_df.iterrows():
            for col_name in new_df.columns:
                if col_name == 'task_id':
                    continue
                new_value = dpg.get_value(f"scrapper_cell_{i}_{col_name}")
                new_df.at[i, col_name] = new_value

        self.db.update_tasks_from_df(new_df)
        log("Alterações salvas no banco de dados.")
        self._populate_edit_db_window()

    def _populate_edit_db_window(self):
        table_tag = self.view.edit_db_table_tag
        container_tag = self.view.edit_db_table_container_tag
        self.scrapper_df = self.db.create_tasks_df()

        if dpg.does_item_exist(table_tag):
            dpg.delete_item(table_tag)

        with dpg.table(
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
            tag=table_tag,
            parent=container_tag
        ):
            for col in self.scrapper_df.columns:
                if col == 'task_id':
                    continue
                dpg.add_table_column(label=self.headers_map.get(col, col))

            for i, row in self.scrapper_df.iterrows():
                with dpg.table_row():
                    for col_name, item in row.items():
                        if col_name == 'task_id':
                            continue
                        dpg.add_input_text(
                            default_value=str(item),
                            tag=f'scrapper_cell_{i}_{col_name}'
                        )

    def _get_task_html_elements(self, puppet_browser: PuppetBrowser) -> dict:
        task_html_elements = {
            'task_name': puppet_browser.get_task_name_html_element(),
            'task_tag': puppet_browser.get_task_tag_html_element(),
            'task_assignee': puppet_browser.get_task_assignee_html_element(),
            'task_history': puppet_browser.get_task_history_html_element(),
        }
        return task_html_elements

    def _get_task_soups(self, task_html_elements: dict) -> dict:
        parser = HTMLParser()
        task_soups = {
            key: parser.soupfy_html_element(html)
            for key, html in task_html_elements.items()
        }
        return task_soups

    def _get_task_data(self, task_soups: dict) -> dict:
        task_data = {
            'task_name': self.re.get_task_name(task_soups['task_name']),
            'task_tag': self.re.get_task_tag(task_soups['task_tag']),
            'task_assignee': self.re.get_task_assignee(task_soups['task_assignee']),  # noqa: E501
            'backlog_date': self.re.get_task_backlog(task_soups['task_history']),  # noqa: E501
            'start_date': self.re.get_task_start(task_soups['task_history']),
            'done_date': self.re.get_task_done(task_soups['task_history']),
            'delivery_date': self.re.get_task_delivery(task_soups['task_history']),  # noqa: E501
        }
        if task_data['done_date'] is None:
            task_data['done_date'] = task_data['delivery_date']
        return task_data

    def get_scrapper_df(self):
        return self.db.create_tasks_df()

    def empty_database(self):
        self.db.empty_database()
