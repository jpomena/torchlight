import statistics


class MetricsCalculator:
    def __init__(self):
        pass

    def get_task_metrics(task_info):
        task_metrics = []

        task_rt = task_info['task_start_date'] - task_info['task_backlog_date']
        task_ct = task_info['task_done_date'] - ['task_start_date']
        task_lt = task_info['task_delivery_date'] - task_info['task_backlog_date']

        task_metrics.append[task_rt, task_ct, task_lt]

        return task_metrics

    def get_tasks_statics(tasks_rt, tasks_ct, tasks_lt):
        
