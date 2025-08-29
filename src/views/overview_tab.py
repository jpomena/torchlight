from datetime import datetime
import tkinter as tk
import ttkbootstrap as ttk
from typing import List, Dict


class OverviewTab:
    def __init__(self, parent_frame: ttk.Frame):
        self.parent_frame = parent_frame

    def create_paned_windows(self):
        self.main_pwindow = ttk.PanedWindow(
            self.parent_frame, orient=tk.HORIZONTAL
        )
        self.main_pwindow.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.overview_frame = ttk.Frame(
            self.main_pwindow
        )
        self.tasks_frame = ttk.Frame(
            self.main_pwindow
        )
        self.main_pwindow.add(self.overview_frame)
        self.main_pwindow.add(self.tasks_frame)
        self.tasks_pwindow = ttk.PanedWindow(
            self.overview_frame, orient=tk.VERTICAL, width=500
        )
        self.tasks_pwindow.pack(side=tk.RIGHT, fill=tk.Y, expand=True)
        self.overview_frame = ttk.Frame(self.tasks_pwindow)
        self.tasks_pwindow.add(self.overview_frame)

    def create_metrics_treeview_widget(self) -> ttk.Treeview:
        treeviews_frame = ttk.LabelFrame(
            self.overview_frame,
            text='Métricas Gerais',
            padding=10
        )
        treeviews_frame.pack(
            side=tk.BOTTOM,
            anchor='sw',
            fill=tk.BOTH,
            expand=True
        )

        columns = {
            'compliance': 'Compliance',
            'advisory': 'Consultivo',
            'litigation': 'Contencioso',
            'contracts': 'Contratos',
            'agreements': 'Convênios',
            'corporate': 'Docs. Corporativos',
            'notices': 'Editais',
            'tax_immunities': 'Imunidades',
            'rental': 'Locação',
            'legal_letters': 'Ofícios'
        }

        rows = [
            'Demandas Abertas',
            'Demandas Fechadas',
            'μ RT (d)',
            'σ RT (d)',
            'μ LT (d)',
            'σ LT (d)',
            'μ CT (d)',
            'σ CT (d)',
            'TT (d)',
            'm LT',
            'LT Mínimo Estimado (d)',
            'LT Máximo Estimado (d)',
            '<LT Mín. Estimado',
            '<=μ LT',
            '<=LT Máx. Estimado',
            'Dentro do Intervalo'
        ]

        overview_metrics_treeview = ttk.Treeview(
            treeviews_frame,
            columns=list(columns.keys()),
            show='headings'
        )
        overview_metrics_names_treeview = ttk.Treeview(
            treeviews_frame,
            columns=(),
            show='tree headings'
        )

        overview_metrics_names_treeview.heading("#0", text="Métrica")
        overview_metrics_names_treeview.column("#0", width=150, anchor='w')

        for key, value in columns.items():
            overview_metrics_treeview.heading(key, text=value)
            overview_metrics_treeview.column(key, width=125, anchor='center')

        for row_name in rows:
            overview_metrics_names_treeview.insert(
                parent='', index='end', iid=row_name, text=row_name
            )

        treeview_y_scrollbar = ttk.Scrollbar(
            treeviews_frame,
            orient=tk.VERTICAL,
            command=overview_metrics_treeview.yview
        )
        treeview_y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        overview_metrics_treeview.configure(
            yscrollcommand=treeview_y_scrollbar.set
        )

        treeview_x_scrollbar = ttk.Scrollbar(
            treeviews_frame,
            orient=tk.HORIZONTAL,
            command=overview_metrics_treeview.xview
        )
        treeview_x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        overview_metrics_treeview.configure(
            yscrollcommand=treeview_y_scrollbar.set
        )

        overview_metrics_names_treeview.pack(
            side=tk.LEFT,
            fill=tk.Y,
            expand=True,
            padx=5,
            pady=2
        )
        overview_metrics_treeview.pack(
            side=tk.LEFT,
            fill=tk.Y,
            expand=True,
            padx=5,
            pady=2
        )

        return overview_metrics_treeview

    def create_tasks_treeview_widget(self) -> ttk.Treeview:
        treeview_frame = ttk.LabelFrame(
            self.tasks_frame,
            text='Lista de Atividades',
            padding=10
        )
        treeview_frame.pack(
            side=tk.RIGHT,
            anchor='e',
            fill=tk.BOTH,
            expand=True
        )

        columns = {
            'task_name': 'Nome da Atividade',
            'task_tag': 'Tipo',
            'task_assignee': 'Responsável',
            'task_backlog_date': 'Criação',
            'task_start_date': 'Início',
            'task_done_date': 'Conclusão',
            'task_delivery_date': 'Entrega'
        }

        overview_task_list_treeview = ttk.Treeview(
            treeview_frame,
            columns=list(columns.keys()),
            show='headings'
        )

        for key, value in columns.items():
            overview_task_list_treeview.heading(key, text=value)
            overview_task_list_treeview.column(key, width=75, anchor='center')

        treeview_scrollbar = ttk.Scrollbar(
            treeview_frame,
            orient=tk.VERTICAL,
            command=overview_task_list_treeview.yview
        )
        treeview_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        overview_task_list_treeview.pack(
            side=tk.RIGHT,
            anchor='e',
            fill=tk.BOTH,
            expand=True,
            padx=5,
            pady=2
        )
        overview_task_list_treeview.configure(
            yscrollcommand=treeview_scrollbar.set
        )

        return overview_task_list_treeview

    def fill_task_list_treeview(
        self, task_list_treeview: ttk.Treeview, tasks: List[Dict[str, str]]
    ):
        for task in tasks:
            task_name = task['task_name']
            task_tag = task['task_tag']
            task_assignee = task['task_assignee']
            task_backlog_date = task['task_backlog_date']
            task_start_date = task['task_start_date']
            task_done_date = task['task_done_date']
            task_delivery_date = task['task_delivery_date']
            task_list_treeview.insert(
                '',
                'end',
                values=(
                    task_name,
                    task_tag,
                    task_assignee,
                    task_backlog_date,
                    task_start_date,
                    task_done_date,
                    task_delivery_date
                ))

    def create_controls_frame(self):
        self.controls_frame = ttk.Frame(self.overview_frame, padding=10)
        self.controls_frame.pack(
            side=tk.TOP,
            anchor='nw',
            fill=tk.X,
            expand=True
        )

    def create_date_filters_entries(self):
        current_year = datetime.now().year
        start_date = datetime(current_year, 1, 1)
        end_date = datetime.now()

        start_date_entry = ttk.DateEntry(
            self.controls_frame,
            dateformat='%d/%m/%Y',
            width=10,
            startdate=start_date
        )
        end_date_entry = ttk.DateEntry(
            self.controls_frame,
            dateformat='%d/%m/%Y',
            startdate=end_date
        )

        start_date_entry.grid(
            row=0,
            column=0,
            padx=5,
            pady=2,
            sticky='ew'
        )
        end_date_entry.grid(
            row=1,
            column=0,
            padx=5,
            pady=2,
            sticky='ew'
        )

    def create_tag_filter(self, tags: List[str]):
        tag_filter_combobox = ttk.Combobox(
            self.controls_frame,
            values=tags,
            state='readonly',
            width=20
        )

        tag_filter_combobox.grid(
            row=0,
            column=1,
            padx=5,
            pady=2,
            sticky='ew'
        )

    def create_assignee_filter(self, assignees: List[str]):
        assignees_filter_combobox = ttk.Combobox(
            self.controls_frame,
            values=assignees,
            state='readonly',
            width=20
        )

        assignees_filter_combobox.grid(
            row=1,
            column=1,
            padx=5,
            pady=2,
            sticky='ew'
        )

    def create_btns(self):
        edit_db_btn = ttk.Button(
            self.controls_frame,
            text='Editar atividades'
        )
        apply_filters_btn = ttk.Button(
            self.controls_frame,
            text='Aplicar filtros'
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
