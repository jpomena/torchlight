import tkinter as tk
import ttkbootstrap as ttk


class MainWindow(ttk.Window):
    def __init__(self, themename):
        super().__init__(themename=themename)

        self.title('Torchlight v0.1')

        self.root_frame = ttk.Frame(self, padding=20)
        self.root_frame.pack(fill=tk.BOTH, expand=True)

        self.main_notebook = ttk.Notebook(self.root_frame)
        self.main_notebook.pack(fill=tk.BOTH, expand=True)

    def create_overview_parent_frame(self) -> ttk.Frame:
        overview_tab_parent_frame = ttk.Frame(self.root_frame)
        self.main_notebook.add(
            overview_tab_parent_frame, text='Visão Geral'
        )

        return overview_tab_parent_frame
