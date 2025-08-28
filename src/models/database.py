import sqlite3 as sql
import pathlib
import os
from typing import List
from typing import Dict


class Database:
    def __init__(self):
        home_dir = pathlib.Path.home()

        if os.name == 'nt':
            db_path = os.getenv('LOCALAPPDATA')
            db_dir = pathlib.Path(db_path) / 'Torchlight'
        else:
            db_dir = home_dir / 'Torchlight'

        db_dir.mkdir(parents=True, exist_ok=True)
        self._db_file = db_dir / 'torchlight.db'

        self.conn = sql.connect(self._db_file)
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

    def get_db_tasks_data(self) -> List[Dict[str, str]]:
        get_tasks_names_sql = '''SELECT task_name from tasks'''
        get_tasks_info_sql = '''
            SELECT
                task_tag,
                task_assignee,
                task_backlog_date,
                task_start_date,
                task_done_date,
                task_delivery_date
            FROM tasks_info
        '''
        tasks = []

        self.cursor.execute(get_tasks_names_sql)
        name_query_results = self.cursor.fetchall()

        self.cursor.execute(get_tasks_info_sql)
        info_query_results = self.cursor.fetchall()

        for name, infos in zip(name_query_results, info_query_results):
            task = {
                'task_name': name[0],
                'task_tag': infos[0],
                'task_assignee': infos[1],
                'task_backlog_date': infos[2],
                'task_start_date': infos[3],
                'task_done_date': infos[4],
                'task_delivery_date': infos[5]
            }
            tasks.append(task)

        return tasks
