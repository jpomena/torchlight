from typing import List, Dict

def synthetize_tag_overview_metrics(
    tasks: List[Dict[str, str | int]],
    tasks_means: Dict[str, float],
    tasks_stdevs: Dict[str, float],
    task_trend: float,
    interval_end_date,
    interval_start_date
):
    tag_overview_metrics = []
    tag_takt_time = interval_end_date - interval_start_date
    task_lead_time_trend = task_trend
    min_reaction_time = tag_reaction_time_mean - tag_reaction_time_stdev
    max_reaction_time = tag_reaction_time_mean + tag_reaction_time_stdev
    min_cycle_time = tag_cycle_time_mean - tag_cycle_time_stdev
    max_cycle_time = tag_cycle_time_mean + tag_cycle_time_stdev
    min_lead_time = tag_lead_time_mean - tag_lead_time_stdev
    max_lead_time = tag_lead_time_mean + tag_lead_time_stdev
    under_min_reaction_time = sum(meets_condition)
