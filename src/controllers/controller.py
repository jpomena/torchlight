import dearpygui.dearpygui as dpg
import pandas as pd
from ..models.main_database import MainDatabase
from ..models.tasks_dataframe import TasksDataframe
from ..models.statistics_dataframe import StatisticsDataframe
from ..views.main_window import MainWindow
from .scrapper_controller import ScrapperController


class Controller:
    def __init__(
        self,
        database: MainDatabase,
        tasks_dataframe: TasksDataframe,
        statistics_dataframe: StatisticsDataframe,
        main_window: MainWindow,
    ):
        self.db = database
        self.tdf = tasks_dataframe
        self.sdf = statistics_dataframe
        self.mw = main_window
        self.scrapper_controller = ScrapperController(self.mw.scrapper_window)
        self.tasks_df = None
        self.filtered_df = None
        self.edited_df = None
        self.original_edited_df = None

    def initialize_view(self):
        self._create_dataframes()

        tags = self.tasks_df['task_tag'].unique().tolist()
        assignees = self.tasks_df['task_assignee'].unique().tolist()

        self.mw.create_main_window(
            tags=tags,
            assignees=assignees,
            apply_filters_callback=self.apply_filters,
            sort_tasks_callback=self._on_sort_tasks,
            edit_db_window_callback=self._toggle_edit_db_window,
            open_import_window_callback=self._transition_to_extract_window,
            save_callback=self.save_edited_tasks
        )

        self.mw.scrapper_window.create_window(
            start_callback=self.scrapper_controller.start_extraction,
            stop_callback=self.scrapper_controller.stop_extraction,
            edit_db_window_callback=(
                self.scrapper_controller._populate_edit_db_window
            ),
            save_callback=self.scrapper_controller.save_edited_tasks,
            import_callback=self.import_scrapper_df
        )

        self.apply_filters()

    def _transition_to_extract_window(self):
        dpg.configure_item(self.mw.edit_db_window_tag, show=False)
        dpg.split_frame()
        dpg.configure_item(self.mw.scrapper_window.window_tag, show=True)

    def _create_dataframes(self):
        self.tasks_df = self.db.create_tasks_df()
        self.tdf.calculate_task_metrics(self.tasks_df)

    def apply_filters(self):
        filter_values = self.mw.overview_tab.get_filter_values()
        start_date = filter_values['start_date']
        end_date = filter_values['end_date']
        selected_tag = filter_values['tag']
        selected_assignee = filter_values['assignee']

        filtered_df = self.tasks_df.copy()

        delivery_dates = filtered_df['task_delivery_date']

        valid_dates_mask = delivery_dates.notna()

        filtered_df = filtered_df[
            valid_dates_mask &
            (delivery_dates >= start_date) &
            (delivery_dates <= end_date)
        ]

        if selected_tag != 'Todos':
            filtered_df = filtered_df[filtered_df['task_tag'] == selected_tag]

        if selected_assignee != 'Todos':
            filtered_df = filtered_df[
                filtered_df['task_assignee'] == selected_assignee
            ]

        self.filtered_df = filtered_df
        self._update_overview_data()
        self._update_tag_tab_data()
        self._update_tag_tab_data()

    def _update_tag_tab_data(self):
        if self.filtered_df.empty:
            return

        statistics_df = self._calculate_statistics(self.filtered_df)

        tags = self.filtered_df['task_tag'].unique().tolist()
        for tag in tags:
            if tag in self.mw.tag_tabs:
                tag_df = self.filtered_df[
                    self.filtered_df['task_tag'] == tag
                ]

                rt_fit = self.sdf.get_loess_fit(
                    tag_df, 'task_reaction_time'
                )
                ct_fit = self.sdf.get_loess_fit(
                    tag_df, 'task_cycle_time'
                )
                lt_fit = self.sdf.get_loess_fit(
                    tag_df, 'task_lead_time'
                )

                self.mw.tag_tabs[tag].update_plots(
                    tag_df, rt_fit, ct_fit, lt_fit
                )
                self.mw.tag_tabs[tag].update_metrics_tables(statistics_df)

    def _update_overview_data(self):
        if self.filtered_df.empty:
            empty_stats = self.sdf.create_statistics_df(self.filtered_df)
            self.mw.overview_tab.update_metrics_table(empty_stats)
            self.mw.overview_tab.update_tasks_table(self.filtered_df)
            return

        statistics_df = self._calculate_statistics(self.filtered_df)

        self.mw.overview_tab.update_metrics_table(statistics_df)
        self.mw.overview_tab.update_tasks_table(self.filtered_df)

    def _calculate_statistics(self, tasks_df: pd.DataFrame) -> pd.DataFrame:
        statistics_df = self.sdf.create_statistics_df(tasks_df)
        tags_means = self.sdf.get_tags_means(tasks_df)
        tags_stdevs = self.sdf.get_tags_stdevs(tasks_df)
        tags_trends = self.sdf.get_tags_trends(tasks_df)

        filter_values = self.mw.overview_tab.get_filter_values()
        start_date = filter_values['start_date']
        end_date = filter_values['end_date']

        tags_takt_times = self.sdf.get_tasks_takt_times(
            tasks_df, start_date, end_date
        )
        task_count_by_tag = self.tdf.get_task_count_by_tag(tasks_df)

        self.sdf.fill_task_count(statistics_df, task_count_by_tag)
        self.sdf.fill_base_statistics(
            statistics_df, tags_means, tags_stdevs,
            tags_trends, tags_takt_times
        )
        self.sdf.fill_min_max_times(statistics_df)
        self.sdf.fill_percentages(tasks_df, statistics_df)
        self.sdf.format_numbers(statistics_df)

        return statistics_df

    def _on_sort_tasks(self, sender, sort_specs):
        if sort_specs is None or self.filtered_df is None:
            return

        col_id, direction = sort_specs[0]

        column_map = self.mw.overview_tab.get_tasks_table_column_map()
        col_name = column_map.get(col_id)

        if col_name:
            df_to_sort = self.filtered_df.copy()

            date_columns = [
                'task_backlog_date', 'task_start_date',
                'task_done_date', 'task_delivery_date'
            ]

            numeric_columns = [
                'task_reaction_time', 'task_cycle_time', 'task_lead_time'
            ]

            og_date_format = None
            if col_name in date_columns:
                og_date_format = df_to_sort[col_name].copy()
                df_to_sort[col_name] = pd.to_datetime(
                    df_to_sort[col_name], format='%d/%m/%Y', errors='coerce'
                )
            elif col_name in numeric_columns:
                df_to_sort[col_name] = pd.to_numeric(
                    df_to_sort[col_name], errors='coerce'
                )

            df_to_sort.sort_values(
                by=col_name,
                ascending=(direction > 0),
                inplace=True,
                na_position='last'
            )

            if og_date_format is not None:
                df_to_sort[col_name] = og_date_format.loc[df_to_sort.index]

            self.mw.overview_tab.update_tasks_table(df_to_sort)

    def _toggle_edit_db_window(self):
        self.edited_df = self.db.create_tasks_df()
        self.original_edited_df = self.edited_df.copy()
        self._populate_edit_db_window()
        dpg.configure_item(self.mw.edit_db_window_tag, show=True)

    def _populate_edit_db_window(self):
        table_tag = 'edit_db_table'
        container_tag = 'edit_db_table_container'
        headers = self.mw.overview_tab.headers_map

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
            for col in self.edited_df.columns:
                dpg.add_table_column(label=headers.get(col, col))
            dpg.add_table_column(label="Ações")

            for task_id, row in self.edited_df.iterrows():
                with dpg.table_row():
                    for col_name, item in row.items():
                        dpg.add_input_text(
                            default_value=str(item),
                            tag=f"cell_{task_id}_{col_name}"
                        )
                    dpg.add_button(
                        label="Remover",
                        callback=lambda s, a, u: self.delete_task(u),
                        user_data=task_id
                    )

    def save_edited_tasks(self):
        if self.original_edited_df is None or self.edited_df is None:
            return

        current_ui_df = self.edited_df.copy()
        for task_id, row in current_ui_df.iterrows():
            for col_name in current_ui_df.columns:
                tag = f"cell_{task_id}_{col_name}"
                if dpg.does_item_exist(tag):
                    new_value = dpg.get_value(tag)
                    current_ui_df.at[task_id, col_name] = new_value

        original_ids = set(self.original_edited_df.index)
        current_ids = set(current_ui_df.index)
        ids_to_delete = original_ids - current_ids

        for task_id in ids_to_delete:
            self.db.delete_task(task_id)

        self.db.update_tasks_from_df(current_ui_df)
        self._create_dataframes()
        self.apply_filters()
        self._toggle_edit_db_window()

    def delete_task(self, task_id: int):
        if self.edited_df is not None:
            self.edited_df.drop(task_id, inplace=True)
        self._populate_edit_db_window()

    def import_scrapper_df(self):
        scrapper_df = self.scrapper_controller.get_scrapper_df()
        self.db.insert_scrapper_df(scrapper_df)
        self.scrapper_controller.empty_database()

        self._create_dataframes()

        updated_tags = ['Todos'] + self.tasks_df['task_tag'].unique().tolist()
        updated_assignees = (
            ['Todos'] + self.tasks_df['task_assignee'].unique().tolist()
        )
        dpg.configure_item("tag_filter_combo", items=updated_tags)
        dpg.configure_item(
            "overview_assignee_filter_combo", items=updated_assignees
        )

        self.apply_filters()
