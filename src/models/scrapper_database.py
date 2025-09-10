import sqlite3 as sql
import pathlib
import os
import pandas as pd


class ScrapperDatabase:
    def __init__(self):
        home_dir = pathlib.Path.home()

        if os.name == 'nt':
            db_path = os.getenv('LOCALAPPDATA')
            db_dir = pathlib.Path(db_path) / 'Torchlight'
        else:
            db_dir = home_dir / 'Torchlight'

        db_dir.mkdir(parents=True, exist_ok=True)
        self._db_file = db_dir / 'scrapper.db'

    def _connect(self):
        conn = sql.connect(self._db_file)
        conn.execute('PRAGMA foreign_keys = ON;')
        return conn

    def create_tables(self):
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

        conn = self._connect()

        try:
            cursor = conn.cursor()
            cursor.execute(create_tasks_table_sql)
            cursor.execute(create_tasks_info_sql)
            conn.commit()
        finally:
            conn.close()

    def save_task_data(self, task_data):
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

        conn = self._connect()

        try:
            cursor = conn.cursor()
            cursor.execute(
                insert_task_sql, (task_data.get('task_name', 'N/A'),)
            )
            task_id = cursor.lastrowid

            if task_data['done_date'] == 'N/A':
                task_data['done_date'] = task_data['delivery_date']
            task_info = (
                task_id,
                task_data.get('task_tag', 'N/A'),
                task_data.get('task_assignee', 'N/A'),
                task_data.get('backlog_date', 'N/A'),
                task_data.get('start_date', 'N/A'),
                task_data.get('done_date', 'N/A'),
                task_data.get('delivery_date', 'N/A')
            )

            cursor.execute(insert_task_info_sql, task_info)
            conn.commit()
        finally:
            conn.close()

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
        conn = self._connect()
        try:
            tasks = pd.read_sql(get_tasks_data, conn)
        finally:
            conn.close()

        return tasks

    def update_tasks_from_df(self, df: pd.DataFrame):
        conn = self._connect()
        try:
            cursor = conn.cursor()
            for _, row in df.iterrows():
                task_id = row['task_id']

                update_task_sql = '''
                    UPDATE tasks SET task_name = ? WHERE task_id = ?
                '''
                cursor.execute(update_task_sql, (row['task_name'], task_id))

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
                cursor.execute(update_task_info_sql, (
                    row['task_tag'],
                    row['task_assignee'],
                    row['task_backlog_date'],
                    row['task_start_date'],
                    row['task_done_date'],
                    row['task_delivery_date'],
                    task_id
                ))
            conn.commit()
        finally:
            conn.close()

    def empty_database(self):
        delete_tasks_sql = 'DELETE FROM tasks'
        conn = self._connect()
        try:
            cursor = conn.cursor()
            cursor.execute(delete_tasks_sql)
            conn.commit()
        finally:
            conn.close()
