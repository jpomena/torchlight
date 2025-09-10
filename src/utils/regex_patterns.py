import re
from datetime import date
from datetime import timedelta


class RegexPatterns:
    clickup_time_units = ['minutos', 'minuto', 'horas']
    clickup_time_units_join = '|'.join(clickup_time_units)

    clickup_months_names = [
        'jan', 'fev', 'mar', 'abr', 'mai', 'jun',
        'jul', 'ago', 'set', 'out', 'nov', 'dez'
    ]
    clickup_months_names_join = '|'.join(clickup_months_names)
    months_mapping = {
        month: index + 1 for index, month in enumerate(clickup_months_names)
    }

    current_date = date.today()
    current_day = current_date.day
    current_month = current_date.month
    current_year = current_date.year
    yesterday_date = current_date - timedelta(days=1)
    yesterday_day = yesterday_date.day
    yesterday_month = yesterday_date.month
    yesterday_year = yesterday_date.year

    today_pattern1 = r'(?P<today1>\d{1,2}:\d{2})'
    today_pattern2 = r'(?P<today2>\d{1,2})' + r'\s*' + rf'({clickup_time_units_join})'  # noqa: E501
    today_pattern3 = r'(?P<today3>Agora)'
    yesterday_pattern = r'(?P<yesterday>Ontem)'
    older_pattern = rf'(?P<month>{clickup_months_names_join})' + r'\s*' + r'(?P<day>\d{1,2})'  # noqa: E501

    backlog_pattern = 'criou(?:.*?)esta(?:.*?)tarefa'
    start_pattern = 'demandas(?:.*?)\n(?:.*?)para'
    done_pattern = 'para(?:.*?)\n(?:.*?)complete'
    delivery_pattern = 'para(?:.*?)\n(?:.*?)entregue'

    backlog = re.compile(rf'(?:{backlog_pattern})(?:.*?)\n(?:.*?)({older_pattern}|{yesterday_pattern}|{today_pattern3}|{today_pattern2}|{today_pattern1})')  # noqa: E501
    start = re.compile(rf'(?:{start_pattern})(?:.*?)\n(?:.*?)\n(?:.*?)({older_pattern}|{yesterday_pattern}|{today_pattern3}|{today_pattern2}|{today_pattern1})')  # noqa: E501
    done = re.compile(rf'(?:{done_pattern})(?:.*?)\n(?:.*?)({older_pattern}|{yesterday_pattern}|{today_pattern3}|{today_pattern2}|{today_pattern1})')  # noqa: E501
    delivery = re.compile(rf'(?:{delivery_pattern})(?:.*?)\n(?:.*?)({older_pattern}|{yesterday_pattern}|{today_pattern3}|{today_pattern2}|{today_pattern1})')  # noqa: E501
    name = re.compile(re.escape('style="text-indent: 0px;">') + r'(.*?)(?=<)')  # noqa: E501
    tag = re.compile(re.escape('tags-select__name-shadow-') + r'(.*?)(?=")')
    assignee = re.compile(re.escape('avatar-group__user-icon-') + r'(.*?)(?=")')  # noqa: E501
