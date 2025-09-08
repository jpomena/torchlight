from datetime import datetime
import pandas as pd
import tkinter as tk
import ttkbootstrap as ttk
from typing import List


class OverviewTab:
    def __init__(self, parent_frame: ttk.Frame):
        self.parent_frame = parent_frame

    def create_paned_windows(self):
        self.main_pwindow = ttk.PanedWindow(
            self.parent_frame, orient=tk.HORIZONTAL
        )
        self.main_pwindow.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.right_frame = ttk.Frame(
            self.main_pwindow, padding=20
        )
        self.left_frame = ttk.Frame(
            self.main_pwindow, padding=20
        )
        self.main_pwindow.add(self.left_frame)
        self.main_pwindow.add(self.right_frame)
        self.left_pwindow = ttk.PanedWindow(
            self.left_frame, orient=tk.VERTICAL
        )
        self.left_pwindow.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def create_metrics_treeview_widget(
        self, statistics_df: pd.DataFrame
    ) -> ttk.Treeview:
        treeviews_frame = self._create_metrics_treeviews_frame()
        self.left_pwindow.add(treeviews_frame)

        columns = statistics_df.columns.tolist()
        rows = statistics_df.index.tolist()

        metrics_values_treeview = self._create_metrics_values_treeview(
            treeviews_frame, columns
        )
        self.metrics_names_treeview = self._create_metrics_names_treeview(
            treeviews_frame, rows
        )
        y_scrollbar, x_scrollbar = self._create_metrics_scrollbars(
            treeviews_frame, metrics_values_treeview
        )

        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.metrics_names_treeview.pack(
            side=tk.LEFT, fill=tk.Y, expand=True, padx=5, pady=2
        )
        metrics_values_treeview.pack(
            side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=2
        )

        return metrics_values_treeview

    def _create_metrics_treeviews_frame(self) -> ttk.LabelFrame:
        treeviews_frame = ttk.LabelFrame(
            self.left_pwindow, text='Métricas Gerais', padding=10
        )
        treeviews_frame.pack_propagate(False)
        return treeviews_frame

    def _create_metrics_values_treeview(
        self, parent_frame: ttk.Frame, columns: list[str]
    ) -> ttk.Treeview:
        treeview = ttk.Treeview(parent_frame, columns=columns, show='headings')

        style = ttk.Style()
        style.configure('Treeview', rowheight=25)
        style.map('Treeview', background=[('selected', style.colors.selectbg)])

        for col in columns:
            treeview.heading(col, text=col)
            treeview.column(
                col, width=125, anchor='center', stretch=False
            )

        return treeview

    def _create_metrics_names_treeview(
        self, parent_frame: ttk.Frame, rows: list[str]
    ) -> ttk.Treeview:
        treeview = ttk.Treeview(
            parent_frame, columns=(), show='tree headings'
        )

        style = ttk.Style()
        style.configure('Treeview', rowheight=25)
        style.map('Treeview', background=[('selected', style.colors.selectbg)])

        treeview.heading("#0", text="Métrica")
        treeview.column("#0", width=150, anchor='w')

        for row_name in rows:
            treeview.insert(
                parent='', index='end', iid=row_name, text=row_name
            )

        return treeview

    def _create_metrics_scrollbars(
        self, parent_frame: ttk.Frame, treeview: ttk.Treeview
    ) -> tuple[ttk.Scrollbar, ttk.Scrollbar]:
        y_scrollbar = ttk.Scrollbar(
            parent_frame, orient=tk.VERTICAL, command=treeview.yview
        )
        x_scrollbar = ttk.Scrollbar(
            parent_frame, orient=tk.HORIZONTAL, command=treeview.xview
        )
        treeview.configure(
            yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set
        )
        return y_scrollbar, x_scrollbar

    def create_tasks_treeview_widget(
        self, tasks: pd.DataFrame
    ) -> ttk.Treeview:
        treeview_frame = self._create_tasks_treeview_frame()
        treeview_frame.pack(
            side=tk.RIGHT, anchor='e', fill=tk.BOTH, expand=True
        )

        columns_names = tasks.columns.tolist()
        task_list_treeview = self._create_tasks_treeview(
            treeview_frame, columns_names
        )

        scrollbar = self._create_tasks_treeview_scrollbar(
            treeview_frame, task_list_treeview
        )

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        task_list_treeview.pack(
            side=tk.RIGHT,
            anchor='e',
            fill=tk.BOTH,
            expand=True,
            padx=5,
            pady=2
        )

        return task_list_treeview

    def _create_tasks_treeview_frame(self) -> ttk.LabelFrame:
        treeview_frame = ttk.LabelFrame(
            self.right_frame, text='Lista de task_name', padding=10
        )
        return treeview_frame

    def _create_tasks_treeview(
        self, parent_frame: ttk.Frame, columns: list[str]
    ) -> ttk.Treeview:
        treeview = ttk.Treeview(parent_frame, columns=columns, show='headings')

        headers_text = [
            'Atividade',
            'Tipo',
            'Responsável',
            'Criação',
            'Início',
            'Conclusão',
            'Entrega',
            'Reaction Time',
            'Cycle Time',
            'Lead Time'
        ]

        self._treeview_sort_orders = {col: True for col in columns}

        for col, header in zip(columns, headers_text):
            treeview.heading(
                col,
                text=header,
                command=lambda c=col: self._treeview_sort_column(
                    treeview, c, self._treeview_sort_orders
                ))
            treeview.column(col, width=75, anchor='center')

        return treeview

    def _treeview_sort_column(
        self, treeview: ttk.Treeview, col: str, sort_orders: dict
    ):
        data = []
        for iid in treeview.get_children(''):
            value = treeview.set(iid, col)
            data.append((value, iid))

        reverse_sort = sort_orders[col]
        data.sort(key=lambda x: x[0], reverse=reverse_sort)

        for index, (value, iid) in enumerate(data):
            treeview.move(iid, '', index)

        sort_orders[col] = not reverse_sort

    def _create_tasks_treeview_scrollbar(
        self, parent_frame: ttk.Frame, treeview: ttk.Treeview
    ) -> ttk.Scrollbar:
        scrollbar = ttk.Scrollbar(
            parent_frame, orient=tk.VERTICAL, command=treeview.yview
        )
        treeview.configure(yscrollcommand=scrollbar.set)
        return scrollbar

    def fill_task_list_treeview(
        self, task_list_treeview: ttk.Treeview, tasks: pd.DataFrame
    ):
        style = ttk.Style()
        odd_color = style.lookup('TFrame', 'background')
        even_color = style.lookup('TCombobox', 'fieldbackground')

        task_list_treeview.tag_configure('oddrow', background=odd_color)
        task_list_treeview.tag_configure('evenrow', background=even_color)

        for item in task_list_treeview.get_children():
            task_list_treeview.delete(item)

        for i, task in enumerate(tasks.itertuples(index=False)):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            task_list_treeview.insert(
                '', 'end', values=list(task), tags=(tag,)
            )

    def fill_metrics_treeview(
        self,
        statistics: pd.DataFrame,
        overview_metrics_treeview: ttk.Treeview
    ):
        style = ttk.Style()
        odd_color = style.colors.get('dark')
        even_color = style.colors.get('secondary')

        for tree in [overview_metrics_treeview, self.metrics_names_treeview]:
            tree.tag_configure('oddrow', background=odd_color)
            tree.tag_configure('evenrow', background=even_color)
            for item in tree.get_children():
                tree.delete(item)

        new_columns = statistics.columns.tolist()
        overview_metrics_treeview['columns'] = new_columns
        for col in new_columns:
            overview_metrics_treeview.heading(col, text=col)
            overview_metrics_treeview.column(
                col, width=125, anchor='center', stretch=False
            )

        for i, metric_row in enumerate(statistics.iterrows()):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            formatted_values = []
            for value in metric_row[1]:
                if pd.isna(value):
                    formatted_values.append('')
                elif isinstance(value, (int, float)) and value == int(value):
                    formatted_values.append(f'{int(value)}')
                elif isinstance(value, float):
                    formatted_values.append(f'{value:.2f}')
                else:
                    formatted_values.append(str(value))

            overview_metrics_treeview.insert(
                '', 'end', values=formatted_values, tags=(tag,)
            )

            self.metrics_names_treeview.insert(
                '', 'end', text=metric_row[0], tags=(tag,)
            )

    def create_controls_frame(self):
        self.controls_frame = ttk.LabelFrame(
            self.left_pwindow, padding=10, text='Filtros'
        )
        self.left_pwindow.add(self.controls_frame)

    def create_date_filters_entries(self):
        current_year = datetime.now().year
        start_date = datetime(current_year, 1, 1)
        end_date = datetime.now()

        self.start_date_entry = ttk.DateEntry(
            self.controls_frame,
            dateformat='%d/%m/%Y',
            width=10,
            startdate=start_date
        )
        self.end_date_entry = ttk.DateEntry(
            self.controls_frame,
            dateformat='%d/%m/%Y',
            startdate=end_date
        )

        self.start_date_entry.grid(
            row=0,
            column=0,
            padx=5,
            pady=2,
            sticky='ew'
        )
        self.end_date_entry.grid(
            row=1,
            column=0,
            padx=5,
            pady=2,
            sticky='ew'
        )

    def create_tag_filter(self, tags: List[str]):
        self.tag_filter_combobox = ttk.Combobox(
            self.controls_frame,
            values=['Todos'] + tags,
            state='readonly',
            width=20
        )
        self.tag_filter_combobox.set('Todos')
        self.tag_filter_combobox.grid(
            row=0,
            column=1,
            padx=5,
            pady=2,
            sticky='ew'
        )

    def create_assignee_filter(self, assignees: List[str]):
        self.assignees_filter_combobox = ttk.Combobox(
            self.controls_frame,
            values=['Todos'] + assignees,
            state='readonly',
            width=20
        )

        self.assignees_filter_combobox.set('Todos')
        self.assignees_filter_combobox.grid(
            row=1,
            column=1,
            padx=5,
            pady=2,
            sticky='ew'
        )

    def create_btns(self, apply_filters_command):
        edit_db_btn = ttk.Button(
            self.controls_frame,
            text='Editar Atividades'
        )
        apply_filters_btn = ttk.Button(
            self.controls_frame,
            text='Aplicar filtros',
            command=apply_filters_command
        )

        edit_db_btn.grid(
            row=0,
            column=2,
            padx=5,
            pady=2,
            sticky='ew'
        )
        apply_filters_btn.grid(
            row=1,
            column=2,
            padx=5,
            pady=2,
            sticky='ew'
        )
