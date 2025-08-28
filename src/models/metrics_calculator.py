import statistics as st
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime
from typing import List, Dict


class MetricsCalculator:
    def __init__(self):
        pass

    def calculate_task_metrics(self, tasks: List[Dict[str, str]]):
        for task in tasks:
            task_backlog_date = datetime.strptime(
                task['task_backlog_date'], '%d/%m/%Y'
            )
            task_start_date = datetime.strptime(
                task['task_start_date'], '%d/%m/%Y'
            )
            task_done_date = datetime.strptime(
                task['task_done_date'], '%d/%m/%Y'
            )
            task_delivery_date = datetime.strptime(
                task['task_delivery_date'], '%d/%m/%Y'
            )

            task_reaction_timedelta = task_start_date - task_backlog_date
            task_cycle_timedelta = task_done_date - task_start_date
            task_lead_timedelta = task_delivery_date - task_backlog_date

            task['task_reaction_time'] = int(
                (task_reaction_timedelta.total_seconds())/86400
            )
            task['task_cycle_time'] = int(
                (task_cycle_timedelta.total_seconds())/86400
            )
            task['task_lead_time'] = int(
                (task_lead_timedelta.total_seconds())/86400
            )

    def get_filtered_tasks_metrics_populations(
        self, filtered_tasks: List[Dict[str, str | int]]
    ) -> Dict[str, List[int]]:
        reaction_time_population = []
        cycle_time_population = []
        lead_time_population = []

        for task in filtered_tasks:
            reaction_time = task['task_reaction_time']
            cycle_time = task['task_cycle_time']
            lead_time = task['task_lead_time']

            reaction_time_population.append(reaction_time)
            cycle_time_population.append(cycle_time)
            lead_time_population.append(lead_time)

        filtered_tasks_populations = {
            'reaction_time_population': reaction_time_population,
            'cycle_time_population': cycle_time_population,
            'lead_time_population': lead_time_population
        }
        return filtered_tasks_populations

    def get_filtered_tasks_means(
        self, filtered_tasks_populations: Dict[str, List[int]]
    ) -> Dict[str, float]:
        filtered_tasks_means = {}

        mean_reaction_time = st.mean(
            filtered_tasks_populations['reaction_time_population']
        )
        mean_cycle_time = st.mean(
            filtered_tasks_populations['cycle_time_population']
        )
        mean_lead_time = st.mean(
            filtered_tasks_populations['lead_time_population']
        )

        filtered_tasks_means['mean_reaction_time'] = mean_reaction_time
        filtered_tasks_means['mean_cycle_time'] = mean_cycle_time
        filtered_tasks_means['mean_lead_time'] = mean_lead_time

        return filtered_tasks_means

    def get_filtered_tasks_pstdevs(
        self, filtered_tasks_populations: Dict[str, List[int]]
    ) -> Dict[str, float]:
        filtered_tasks_pstdevs = {}

        reaction_time_stdev = st.pstdev(
            filtered_tasks_populations['reaction_time_population']
        )
        cycle_time_stdev = st.pstdev(
            filtered_tasks_populations['cycle_time_population']
        )
        lead_time_stdev = st.pstdev(
            filtered_tasks_populations['lead_time_population']
        )

        filtered_tasks_pstdevs['reaction_time_stdev'] = reaction_time_stdev
        filtered_tasks_pstdevs['cycle_time_stdev'] = cycle_time_stdev
        filtered_tasks_pstdevs['lead_time_stdev'] = lead_time_stdev

        return filtered_tasks_pstdevs

    def lead_time_trend(self, filtered_tasks: List[Dict[str, str | int]]):
        tasks_delivery_dates = []
        tasks_lead_times = []
        for task in filtered_tasks:
            task_delivery_date_obj = datetime.strptime(
                task['task_delivery_date'], '%d/%m/%Y'
            )
            tasks_delivery_dates.append(task_delivery_date_obj.timestamp())
            tasks_lead_times.append(task['task_lead_time'])
        X = np.array(tasks_delivery_dates).reshape(-1, 1)
        y = np.array(tasks_lead_times)

        model = LinearRegression()

        model.fit(X, y)
        m_coefficient = model.coef_[0]
        interception = model.intercept_

        return m_coefficient, interception
