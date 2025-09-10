import dearpygui.dearpygui as dpg
import pandas as pd
from datetime import datetime
from typing import List, Callable, Dict
from datetime import date


class OverviewTab:
    def __init__(self):
        self._tasks_table_column_map = {}
        self.headers_map = {
            'task_name': 'Atividade',
            'task_tag': 'Tipo',
            'task_assignee': 'Responsável',
            'task_backlog_date': 'Criação',
            'task_start_date': 'Início',
            'task_done_date': 'Conclusão',
            'task_delivery_date': 'Entrega',
            'task_reaction_time': 'Reaction Time',
            'task_cycle_time': 'Cycle Time',
            'task_lead_time': 'Lead Time'
        }

    def create_tab(
        self,
        tags: List[str],
        assignees: List[str],
        apply_filters_callback: Callable,
        sort_tasks_callback: Callable,
        edit_db_window_callback: Callable
    ):
        with dpg.tab(label="Visão Geral"):
            with dpg.group(horizontal=True):
                with dpg.child_window(width=700, tag="left_pane"):
                    self._create_controls_section(
                        tags, assignees,
                        apply_filters_callback, edit_db_window_callback
                    )
                    self._create_metrics_table()
                with dpg.child_window(tag="right_pane"):
                    self._create_tasks_table(sort_tasks_callback)

    def get_filter_values(self) -> Dict:
        start_date_dict = dpg.get_value("start_date_picker")
        end_date_dict = dpg.get_value("end_date_picker")

        return {
            "start_date": datetime(
                start_date_dict['year'] + 1900,
                start_date_dict['month'] + 1,
                start_date_dict['month_day']
            ),
            "end_date": datetime(
                end_date_dict['year'] + 1900,
                end_date_dict['month'] + 1,
                end_date_dict['month_day']
            ),
            "tag": dpg.get_value("tag_filter_combo"),
            "assignee": dpg.get_value("assignee_filter_combo")
        }

    def update_metrics_table(self, statistics_df: pd.DataFrame):
        dpg.delete_item("metrics_table", children_only=True)

        if statistics_df.empty:
            dpg.add_table_column(
                label="Métrica", parent="metrics_table"
            )
            return

        dpg.add_table_column(label="Métrica", parent="metrics_table")
        for col in statistics_df.columns:
            dpg.add_table_column(label=str(col), parent="metrics_table")

        for index, row in statistics_df.iterrows():
            with dpg.table_row(parent="metrics_table"):
                dpg.add_text(index)
                for value in row:
                    if pd.isna(value):
                        formatted_value = ''
                    elif isinstance(value, (int, float)) and value == int(value):  # noqa: E501
                        formatted_value = f'{int(value)}'
                    elif isinstance(value, float):
                        formatted_value = f'{value:.2f}'
                    else:
                        formatted_value = str(value)
                    dpg.add_text(formatted_value)

    def update_tasks_table(self, tasks_df: pd.DataFrame):
        for item in dpg.get_item_children("tasks_table", 1):
            dpg.delete_item(item)
        if tasks_df.empty:
            return

        for task in tasks_df.itertuples(index=False):
            with dpg.table_row(parent="tasks_table"):
                for item in task:
                    if isinstance(item, (pd.Timestamp, date)):
                        dpg.add_text(item.strftime('%d/%m/%Y'))
                    else:
                        dpg.add_text(str(item))

    def get_tasks_table_column_map(self) -> Dict[int, str]:
        return self._tasks_table_column_map

    def _create_controls_section(
        self,
        tags: List[str],
        assignees: List[str],
        apply_filters_callback: Callable,
        edit_db_window_callback: Callable
    ):
        with dpg.group(horizontal=True, parent="left_pane"):
            current_year = datetime.now().year
            start_date = datetime(current_year, 1, 1)
            end_date = datetime.now()

            start_date_dict = {
                'month_day': start_date.day, 'year': start_date.year - 1900,
                'month': start_date.month - 1
            }
            end_date_dict = {
                'month_day': end_date.day, 'year': end_date.year - 1900,
                'month': end_date.month - 1
            }

            dpg.add_date_picker(
                label="Início", tag="start_date_picker",
                default_value=start_date_dict
            )

            dpg.add_date_picker(
                label="Fim", tag="end_date_picker",
                default_value=end_date_dict
            )

            with dpg.group():
                dpg.add_combo(
                    label="Tag", items=['Todos'] + tags,
                    tag="tag_filter_combo", default_value='Todos', width=200
                )
                dpg.add_combo(
                    label="Responsável", items=['Todos'] + assignees,
                    tag="assignee_filter_combo", default_value='Todos',
                    width=200
                )

                dpg.add_spacer(height=5)

                dpg.add_button(
                    label="Aplicar Filtros",
                    callback=lambda: apply_filters_callback(),
                    width=200
                )
                dpg.add_button(
                    label="Editar Atividades",
                    callback=lambda: edit_db_window_callback(),
                    width=200
                )

    def _create_metrics_table(self):
        dpg.add_table(
            header_row=True, resizable=True,
            policy=dpg.mvTable_SizingFixedFit,
            scrollX=True, scrollY=True, row_background=True,
            freeze_columns=1, freeze_rows=1,
            borders_outerH=True, borders_innerV=True,
            borders_innerH=True, borders_outerV=True,
            tag="metrics_table"
        )

    def _create_tasks_table(self, sort_callback: Callable):
        with dpg.table(
            header_row=True, resizable=True,
            policy=dpg.mvTable_SizingFixedFit,
            scrollX=True, scrollY=True, row_background=True,
            freeze_columns=1, freeze_rows=1,
            borders_outerH=True, borders_innerV=True,
            borders_innerH=True, borders_outerV=True,
            sortable=True, tag="tasks_table",
            callback=sort_callback
        ):
            for col_name, header in self.headers_map.items():
                col_id = dpg.add_table_column(label=header)
                self._tasks_table_column_map[col_id] = col_name
