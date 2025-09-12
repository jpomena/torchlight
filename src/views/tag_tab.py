import dearpygui.dearpygui as dpg
from typing import List, Callable, Dict
from datetime import datetime
import pandas as pd
import time


class TagTab:
    def __init__(self):
        self.tag_name = None
        self.plot_tags = {}
        self.metric_table_tags = {}

    def create_tab(
        self,
        tag_name,
        assignees: List[str],
        apply_filters_callback: Callable
    ):
        self.tag_name = tag_name
        with dpg.tab(label=self.tag_name):
            with dpg.group():
                dpg.add_spacer(width=5)
                with dpg.group(
                    horizontal=True, tag=f'{self.tag_name}_upper_pane'
                ):
                    self._create_controls_section(
                        assignees, apply_filters_callback
                        )
                    dpg.add_spacer(width=50)
                    self._create_metrics_section()

                with dpg.group(
                    horizontal=True, tag=f'{self.tag_name}_lower_pane'
                ):
                    self._create_plots()

    def update_plots(
        self,
        tasks_df: pd.DataFrame,
        rt_fit: tuple,
        ct_fit: tuple,
        lt_fit: tuple
    ):
        if tasks_df.empty:
            return

        delivery_dates = [
            time.mktime(d.timetuple())
            for d in tasks_df['task_delivery_date']
        ]
        reaction_times = tasks_df['task_reaction_time'].tolist()
        cycle_times = tasks_df['task_cycle_time'].tolist()
        lead_times = tasks_df['task_lead_time'].tolist()

        rt_x_fit, rt_y_fit = rt_fit
        ct_x_fit, ct_y_fit = ct_fit
        lt_x_fit, lt_y_fit = lt_fit

        rt_x_fit = [time.mktime(d.timetuple()) for d in rt_x_fit]
        ct_x_fit = [time.mktime(d.timetuple()) for d in ct_x_fit]
        lt_x_fit = [time.mktime(d.timetuple()) for d in lt_x_fit]

        dpg.set_value(self.plot_tags['rt_scatter'], [delivery_dates, reaction_times]) # noqa
        dpg.set_value(self.plot_tags['rt_line'], [rt_x_fit, rt_y_fit])
        dpg.set_value(self.plot_tags['ct_scatter'], [delivery_dates, cycle_times]) # noqa
        dpg.set_value(self.plot_tags['ct_line'], [ct_x_fit, ct_y_fit])
        dpg.set_value(self.plot_tags['lt_scatter'], [delivery_dates, lead_times]) # noqa
        dpg.set_value(self.plot_tags['lt_line'], [lt_x_fit, lt_y_fit])

        dpg.fit_axis_data(self.plot_tags['rt_x_axis'])
        dpg.fit_axis_data(self.plot_tags['rt_y_axis'])
        dpg.fit_axis_data(self.plot_tags['ct_x_axis'])
        dpg.fit_axis_data(self.plot_tags['ct_y_axis'])
        dpg.fit_axis_data(self.plot_tags['lt_x_axis'])
        dpg.fit_axis_data(self.plot_tags['lt_y_axis'])

    def get_filter_values(self) -> Dict:
        start_date_dict = dpg.get_value(f"{self.tag_name}_start_date_picker")
        end_date_dict = dpg.get_value(f"{self.tag_name}_end_date_picker")

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
            "assignee": dpg.get_value(
                f"{self.tag_name}_assignee_filter_combo"
            )
        }

    def update_metrics_tables(self, statistics_df: pd.DataFrame):
        metrics_map = {
            'RT': self.metric_table_tags['rt_table'],
            'CT': self.metric_table_tags['ct_table'],
            'LT': self.metric_table_tags['lt_table'],
        }

        for metric_prefix, table_tag in metrics_map.items():
            if dpg.does_item_exist(table_tag):
                dpg.delete_item(table_tag, children_only=True)
            else:
                continue

            metric_rows = [
                f'Média {metric_prefix} (d)',
                f'Desv. Pad. {metric_prefix} (d)',
                f'{metric_prefix} Mín. (d)',
                f'{metric_prefix} Máx. (d)',
                f'< {metric_prefix} Mín.',
                f'<= Média {metric_prefix}',
                f'<= {metric_prefix} Máx.',
                f'm {metric_prefix}'
            ]

            dpg.add_table_column(
                label="Métrica", parent=table_tag
            )
            dpg.add_table_column(
                label="Valor", parent=table_tag
            )

            if self.tag_name in statistics_df.columns:
                for row_name in metric_rows:
                    if row_name in statistics_df.index:
                        with dpg.table_row(parent=table_tag):
                            dpg.add_text(row_name)
                            value = statistics_df.loc[row_name, self.tag_name]
                            dpg.add_text(str(value))

    def _create_plots(self):
        with dpg.tab_bar(parent=f'{self.tag_name}_lower_pane'):
            # Lead Time Plot
            with dpg.tab(label="Lead Time"):
                with dpg.plot(
                    label="Lead Time", height=-1, width=-1, no_legend=False
                ):
                    self.plot_tags['lt_x_axis'] = dpg.add_plot_axis(
                        dpg.mvXAxis, label="Data de Entrega", time=True
                    )
                    self.plot_tags['lt_y_axis'] = dpg.add_plot_axis(
                        dpg.mvYAxis, label="Dias"
                    )
                    self.plot_tags['lt_scatter'] = dpg.add_scatter_series(
                        [], [], parent=self.plot_tags['lt_y_axis'],
                        label='Lead Time'
                    )
                    self.plot_tags['lt_line'] = dpg.add_line_series(
                        [], [], parent=self.plot_tags['lt_y_axis'],
                        label='Tendência'
                    )

            # Cycle Time Plot
            with dpg.tab(label="Cycle Time"):
                with dpg.plot(
                    label="Cycle Time", height=-1, width=-1, no_legend=False
                ):
                    self.plot_tags['ct_x_axis'] = dpg.add_plot_axis(
                        dpg.mvXAxis, label="Data de Entrega", time=True
                    )
                    self.plot_tags['ct_y_axis'] = dpg.add_plot_axis(
                        dpg.mvYAxis, label="Dias"
                    )
                    self.plot_tags['ct_scatter'] = dpg.add_scatter_series(
                        [], [], parent=self.plot_tags['ct_y_axis'],
                        label='Cycle Time'
                    )
                    self.plot_tags['ct_line'] = dpg.add_line_series(
                        [], [], parent=self.plot_tags['ct_y_axis'],
                        label='Tendência'
                    )

            # Reaction Time Plot
            with dpg.tab(label="Reaction Time"):
                with dpg.plot(
                    label="Reaction Time", height=-1, width=-1, no_legend=False
                ):
                    self.plot_tags['rt_x_axis'] = dpg.add_plot_axis(
                        dpg.mvXAxis, label="Data de Entrega", time=True
                    )
                    self.plot_tags['rt_y_axis'] = dpg.add_plot_axis(
                        dpg.mvYAxis, label="Dias"
                    )
                    self.plot_tags['rt_scatter'] = dpg.add_scatter_series(
                        [], [], parent=self.plot_tags['rt_y_axis'],
                        label='Reaction Time'
                    )
                    self.plot_tags['rt_line'] = dpg.add_line_series(
                        [], [], parent=self.plot_tags['rt_y_axis'],
                        label='Tendência'
                    )

    def _create_controls_section(
        self,
        assignees: List[str],
        apply_filters_callback: Callable
    ):
        with dpg.group(
            horizontal=True, parent=f'{self.tag_name}_upper_pane'
        ):
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

            with dpg.group(horizontal=True):
                dpg.add_date_picker(
                    label="Início", tag=f"{self.tag_name}_start_date_picker",
                    default_value=start_date_dict
                )
                dpg.add_spacer(width=5)

                dpg.add_date_picker(
                    label="Fim", tag=f"{self.tag_name}_end_date_picker",
                    default_value=end_date_dict
                )
                dpg.add_spacer(width=5)

            with dpg.group():
                dpg.add_combo(
                    label="Responsável",
                    items=['Todos'] + assignees,
                    tag=f"{self.tag_name}_assignee_filter_combo",
                    default_value='Todos',
                    width=200
                )

                dpg.add_spacer(height=5)

                dpg.add_button(
                    label="Aplicar Filtros",
                    width=200,
                    callback=lambda: apply_filters_callback(self.tag_name)
                )

    def _create_metrics_section(self):
        with dpg.group(
            horizontal=True, parent=f'{self.tag_name}_upper_pane'
        ):
            rt_table_tag = f"rt_table_{self.tag_name}"
            ct_table_tag = f"ct_table_{self.tag_name}"
            lt_table_tag = f"lt_table_{self.tag_name}"

            self.metric_table_tags['rt_table'] = rt_table_tag
            self.metric_table_tags['ct_table'] = ct_table_tag
            self.metric_table_tags['lt_table'] = lt_table_tag

            dpg.add_table(
                header_row=True, tag=rt_table_tag,
                borders_outerH=True, borders_innerV=True,
                borders_innerH=True, borders_outerV=True,
                policy=dpg.mvTable_SizingFixedFit,
                row_background=True,
                height=225, width=175
            )
            dpg.add_spacer(width=5)
            dpg.add_table(
                header_row=True, tag=ct_table_tag,
                borders_outerH=True, borders_innerV=True,
                borders_innerH=True, borders_outerV=True,
                policy=dpg.mvTable_SizingFixedFit,
                row_background=True,
                height=225, width=175
            )
            dpg.add_spacer(width=5)
            dpg.add_table(
                header_row=True, tag=lt_table_tag,
                borders_outerH=True, borders_innerV=True,
                borders_innerH=True, borders_outerV=True,
                policy=dpg.mvTable_SizingFixedFit,
                row_background=True,
                height=225, width=175
            )
