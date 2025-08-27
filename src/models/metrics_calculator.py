import statistics as st


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
        rt_average = st.mean(tasks_rt)
        rt_population_st_dev = st.pstdev(tasks_rt)

    def linreg(X, Y):
        N = len(X)
        Sx = Sy = Sxx = Syy = Sxy = 0.0
        for x, y in zip(X, Y):
            Sx = Sx + x
            Sy = Sy + y
            Sxx = Sxx + x*x
            Syy = Syy + y*y
            Sxy = Sxy + x*y
        det = Sxx * N - Sx * Sx
        return (Sxy * N - Sy * Sx)/det, (Sxx * Sy - Sx * Sxy)/det


    x = [12, 34, 29, 38, 34, 51, 29, 34, 47, 34, 55, 94, 68, 81]
    a,b = linreg(range(len(x)),x)  //your x,y are switched from standard notation
