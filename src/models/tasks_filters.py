from typing import List, Dict


class TaskFilters:
    def __init__(self):
        pass

    def filter_tasks_by_tag(
        self, tasks: list[Dict[str, str | int]], target_tag: str
    ) -> List[Dict[str, str | int]]:
        filtered_tasks = []
        for task in tasks:
            if task['task_tag'] == target_tag:
                filtered_tasks.append[task]

        return filtered_tasks

    def filter_tasks_by_assignee(
        self, tasks: list[Dict[str, str | int]], target_assignee: str
    ) -> List[Dict[str, str | int]]:
        filtered_tasks = []
        for task in tasks:
            if task['task_assignee'] == target_assignee:
                filtered_tasks.append(task)

        return filtered_tasks
