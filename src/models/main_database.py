import sqlite3 as sql
import pathlib
import os
import pandas as pd


class MainDatabase:
    def __init__(self):
        home_dir = pathlib.Path.home()

        if os.name == 'nt':
            db_path = os.getenv('LOCALAPPDATA')
            db_dir = pathlib.Path(db_path) / 'Torchlight'
        else:
            db_dir = home_dir / 'Torchlight'

        db_dir.mkdir(parents=True, exist_ok=True)
        self._db_file = db_dir / 'torchlight.db'

        self.conn = sql.connect(self._db_file, check_same_thread=False)
        self.conn.execute('PRAGMA foreign_keys = ON;')
        self.cursor = self.conn.cursor()

        self.create_table()

    def create_table(self):
        create_tasks_table_sql = '''
            CREATE TABLE IF NOT EXISTS tasks(
                task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name TEXT NOT NULL
            );'''

        create_tasks_info_sql = '''
            CREATE TABLE IF NOT EXISTS tasks_info(
                task_info_id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER,
                task_tag TEXT NOT NULL,
                task_assignee TEXT NOT NULL,
                task_backlog_date TEXT,
                task_start_date TEXT,
                task_done_date TEXT,
                task_delivery_date TEXT,
                FOREIGN KEY (task_id)
                REFERENCES tasks (task_id) ON DELETE CASCADE
            );'''

        self.cursor.execute(create_tasks_table_sql)
        self.cursor.execute(create_tasks_info_sql)
        self.conn.commit()

    def create_tasks_df(self) -> pd.DataFrame:
        get_tasks_data = '''
            SELECT
                tasks.task_id,
                tasks.task_name,
                tasks_info.task_tag,
                tasks_info.task_assignee,
                tasks_info.task_backlog_date,
                tasks_info.task_start_date,
                tasks_info.task_done_date,
                tasks_info.task_delivery_date
            FROM tasks JOIN tasks_info
                ON tasks.task_id = tasks_info.task_id
        '''
        tasks = pd.read_sql(get_tasks_data, self.conn, index_col='task_id')

        return tasks

    def insert_scrapper_df(self, scrapper_df: pd.DataFrame):
        insert_task_sql = '''
            INSERT INTO tasks (task_name) VALUES (?)
        '''

        insert_task_info_sql = '''
            INSERT INTO tasks_info(
                task_id,
                task_tag,
                task_assignee,
                task_backlog_date,
                task_start_date,
                task_done_date,
                task_delivery_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        '''

        for _, row in scrapper_df.iterrows():
            self.cursor.execute(insert_task_sql, (row['task_name'],))
            task_id = self.cursor.lastrowid

            task_info_data = (
                task_id,
                row['task_tag'],
                row['task_assignee'],
                row['task_backlog_date'],
                row['task_start_date'],
                row['task_done_date'],
                row['task_delivery_date']
            )
            self.cursor.execute(insert_task_info_sql, task_info_data)
        self.conn.commit()

    def update_tasks_from_df(self, df: pd.DataFrame):
        for task_id, row in df.iterrows():
            update_task_sql = '''
                UPDATE tasks SET task_name = ? WHERE task_id = ?
            '''
            self.cursor.execute(update_task_sql, (row['task_name'], task_id))

            update_task_info_sql = """
                UPDATE tasks_info
                SET task_tag = ?,
                    task_assignee = ?,
                    task_backlog_date = ?,
                    task_start_date = ?,
                    task_done_date = ?,
                    task_delivery_date = ?
                WHERE task_id = ?
            """
            self.cursor.execute(update_task_info_sql, (
                row['task_tag'],
                row['task_assignee'],
                row['task_backlog_date'],
                row['task_start_date'],
                row['task_done_date'],
                row['task_delivery_date'],
                task_id
            ))
        self.conn.commit()

    def delete_task(self, task_id: int):
        self.cursor.execute('DELETE FROM tasks WHERE task_id = ?', (task_id,))
        self.conn.commit()
