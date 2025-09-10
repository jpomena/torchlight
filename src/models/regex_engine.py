from ..utils.aux_functions import log
from ..utils.regex_patterns import RegexPatterns as regex


class RegexEngine:
    def __init__(self):
        pass

    def get_task_name(self, task_name_soup):
        log('Definindo nome da atividade...')
        try:
            task_name = regex.name.search(str(task_name_soup)).group(1)
            log(f'Atividade: {task_name}')

        except Exception:
            task_name = 'N/A'
            log('Não foi possível definir o nome.')
        return task_name

    def get_task_tag(self, task_tag_soup):
        try:
            log('Definindo etiqueta da atividade...')
            task_tag_minusc = regex.tag.search(str(task_tag_soup)).group(1)
            task_tag = task_tag_minusc.capitalize()
            log(f'Etiqueta: {task_tag}')
        except Exception:
            task_tag = 'N/A'
            log('Não foi possível definir a etiqueta.')
        return task_tag

    def get_task_assignee(self, task_assignee_soup):
        try:
            task_assignee = regex.assignee.search(
                str(task_assignee_soup)
                ).group(1)
            log(f'Responsável: {task_assignee}')
        except Exception:
            task_assignee = 'N/A'
            log('Não foi possível definir o responsável.')
        return task_assignee

    def _filtro_match(self, match):
        if match.group('today3') or match.group('today2') or match.group('today1'):  # noqa: E501
            return f'{regex.current_day}/{regex.current_month}/{regex.current_year}'  # noqa: E501
        elif match.group('yesterday'):
            return f'{regex.yesterday_day}/{regex.yesterday_month}/{regex.yesterday_year}'  # noqa: E501
        elif match.group('month') and match.group('day'):
            day = match.group('day')
            month_num = regex.months_mapping.get(match.group('month'))
            return f'{day}/{month_num}/{regex.current_year}'

    def get_task_backlog(self, task_history_soup):
        log('Buscando data de criação da atividade...')
        try:
            backlog_regex_results = list(
                regex.backlog.finditer(
                    task_history_soup.get_text(separator='\n')
                ))
            if backlog_regex_results:
                task_backlog_match = backlog_regex_results[-1]
                task_backlog_str = self._filtro_match(task_backlog_match)
                if task_backlog_str:
                    log(f'Demanda criada em: {task_backlog_str}')
                else:
                    task_backlog_str = 'N/A'
                    log('Data de criação não encontrada.')
            else:
                task_backlog_str = 'N/A'
                log('Data de criação não encontrada.')
        except Exception:
            task_backlog_str = 'N/A'
            log('Data de criação não encontrada.')

        return task_backlog_str

    def get_task_start(self, task_history_soup):
        log('Buscando data de início da atividade...')
        try:
            start_regex_results = list(
                regex.start.finditer(
                    task_history_soup.get_text(separator='\n')
                ))
            if start_regex_results:
                start_match = start_regex_results[-1]
                task_start = self._filtro_match(start_match)
                if task_start:
                    log(f'Início da atividade em: {task_start}')
                else:
                    task_start = 'N/A'
                    log('Data de início não encontrada.')
            else:
                task_start = 'N/A'
                log('Data de início não encontrada.')
        except Exception:
            task_start = 'N/A'
            log('Data de início não encontrada.')

        return task_start

    def get_task_done(self, task_history_soup):
        log('Buscando data de conclusão da atividade...')
        try:
            done_regex_results = list(
                regex.done.finditer(task_history_soup.get_text(separator='\n'))
            )
            if done_regex_results:
                done_match = done_regex_results[0]
                task_done = self._filtro_match(done_match)
                if task_done:
                    log(f'Conclusão da atividade em: {task_done}')
                else:
                    task_done = 'N/A'
                    log('Atividade concluída na entrega.')
            else:
                task_done = 'N/A'
                log('Atividade concluída na entrega.')
        except Exception:
            task_done = 'N/A'
            log('Atividade concluída na entrega.')

        return task_done

    def get_task_delivery(self, task_history_soup):
        log('Buscando data de entrega da atividade...')
        try:
            delivery_regex_results = list(
                regex.delivery.finditer(task_history_soup.get_text(
                    separator='\n'
                )))
            if delivery_regex_results:
                delivery_matches = delivery_regex_results[0]
                task_delivery = self._filtro_match(delivery_matches)
                if task_delivery:
                    log(f'Atividade entregue em: {task_delivery}')
                else:
                    task_delivery = 'N/A'
                    log('Data de entrega não encontrada.')
            else:
                task_delivery = 'N/A'
                log('Data de entrega não encontrada.')
        except Exception:
            task_delivery = 'N/A'
            log('Data de entrega não encontrada.')

        return task_delivery
