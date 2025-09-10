import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from ..utils.aux_functions import log, wait
from ..utils.clickup_selectors import ClickUpSelectors as cs


class PuppetBrowser:
    def __init__(self, username: str, password: str, driver_path: str):
        self.username = username
        self.password = password
        self.driver_path = driver_path
        self.driver = None

        self.open_browser()

    def open_browser(self):
        try:
            if self.driver_path:
                log('Caminho do driver fornecido. Abrindo...')
                self.driver = webdriver.Firefox(
                    executable_path=self.driver_path
                )
            else:
                log('Caminho do driver não fornecido. Buscando no PATH...')
                self.driver = webdriver.Firefox()
        except Exception as e:
            log(f'{e}')

    def get_driver(self):
        return self.driver

    def access_site(self):
        log('Acessando site...')
        self.driver.get('https://app.clickup.com/login')
        return

    def login(self):
        log('Acessando plataforma...')
        user_entry = wait(self.driver).until(
            EC.presence_of_element_located((By.ID, cs.login_entry_selector))
        )
        password_entry = wait(self.driver).until(
            EC.presence_of_element_located((By.ID, cs.password_entry_selector))
        )
        user_entry.send_keys(self.username)
        password_entry.send_keys(self.password)
        password_entry.send_keys(Keys.RETURN)

    def open_list(self, list_name):
        log('Abrindo lista...')
        list_btn = wait(self.driver).until(
            EC.element_to_be_clickable(
                (By.XPATH, cs.list_name_btn_selector(list_name))
            ))
        list_btn.click()

    def open_list_kanban(self):
        log('Abrindo Kanban...')
        kanban_btn = wait(self.driver).until(
            EC.element_to_be_clickable((By.XPATH, cs.kanban_btn_selector))
        )
        kanban_btn.click()

    def config_columns(self):
        log('Configurando colunas...')
        grouping_btn = wait(self.driver).until(
            EC.visibility_of_element_located(
                (By.XPATH, cs.grouping_btn_selector)
            ))
        grouping_btn.click()
        try:
            second_group_by_btn = wait(self.driver, 20).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, cs.second_group_by_btn_selector)
                ))
            log('Botão encontrado')
            second_group_by_btn.click()
        except Exception as e:
            log(f'Não foi possível alterar o agrupamento das colunas: {e}')
        self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)

    def select_column(self):
        # log('Indo até a última coluna...')
        # wait(self.driver).until(
        #     EC.visibility_of_element_located(
        #         (By.CSS_SELECTOR, cs.kanban_selector)
        #     ))
        log('Aguardando a presença da coluna "Entregue" no DOM...')
        delivered_column = wait(self.driver).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, cs.delivered_column_selector))
        )
        log('Coluna "Entregue" encontrada. Rolando até ela...')
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);", delivered_column
        )
        time.sleep(1)
        log('Coluna "Entregue" está visível.')

        return delivered_column

    def open_card(self, delivered_column):
        try:
            log('Buscando e abrindo card...')
            card = wait(delivered_column).until(
                EC.visibility_of_element_located(
                    (By.XPATH, cs.card_selector)
                ))
            card_btn = wait(card).until(
                EC.element_to_be_clickable((By.XPATH, cs.card_btn_selector))
            )
            self.driver.execute_script("arguments[0].click();", card_btn)
            log('Card aberto.')
            card_found = True
        except Exception as e:
            log(f'ERRO: {e}')
            card_found = False

        return card_found

    def get_task_name_html_element(self):
        time.sleep(5)
        log('Buscando fonte para nome...')
        try:
            name_html_element = wait(self.driver).until(
                EC.visibility_of_element_located(
                    (By.XPATH, cs.name_html_element_selector)
                )).get_attribute('outerHTML')
            log('Fonte para nome encontrada.')
            return name_html_element
        except Exception as e:
            log(f'Fonte para nome não encontrada: {e}')

    def get_task_tag_html_element(self):
        log('Buscando fonte para responsável...')
        try:
            tag_html_element = wait(self.driver).until(
                EC.visibility_of_element_located(
                    (By.XPATH, cs.tag_html_element_selector)
                )).get_attribute('outerHTML')
            log('Fonte para responsável encontrado')
            return tag_html_element
        except Exception:
            log('Fonte para responsável não encontrado.')

    def get_task_assignee_html_element(self):
        log('Buscando fonte para etiqueta...')
        try:
            assignee_html_element = wait(self.driver).until(
                EC.visibility_of_element_located(
                    (By.XPATH, cs.assignee_html_element_selector)
                )).get_attribute('outerHTML')
            log('Fonte para etiqueta encontrada.')
            return assignee_html_element

        except Exception:
            log('Fonte para etiqueta não encontrada.')

    def get_task_history_html_element(self):
        log('Buscando fonte para datas...')
        try:
            task_details_btn = wait(self.driver).until(
                EC.element_to_be_clickable(
                    (By.XPATH, cs.task_details_btn_selector)
                ))
            task_details_btn.click()
            log('Tentando ampliar histórico...')
            try:
                expand_task_history_btn = wait(self.driver).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, cs.expand_task_history_btn_selector)
                    ))
                expand_task_history_btn.click()
                log('Histórico ampliado.')
            except Exception:
                log('Histórico não ampliável.')
            time.sleep(5)
            task_history_html_element = wait(self.driver).until(
                EC.visibility_of_element_located(
                    (By.XPATH, cs.task_history_html_element_selector)
                )).get_attribute('outerHTML')
            return task_history_html_element
        except Exception:
            log('Fonte para datas não encontrada.')

    def archive_card(self):
        log('Arquivando card...')
        card_config_menu = wait(self.driver).until(
            EC.element_to_be_clickable(
                (By.XPATH, cs.card_config_menu_selector)
            ))
        card_config_menu.click()
        archive_card_btn = wait(self.driver).until(
            EC.element_to_be_clickable(
                (By.XPATH, cs.archive_card_btn_selector)
            ))
        archive_card_btn.click()
        time.sleep(5)
        log('Fechando card...')
        self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
        time.sleep(3)
        self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
        time.sleep(3)
        self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
        time.sleep(3)

    def close_browser(self):
        if self.driver:
            log('Fechando navegador...')
            self.driver.quit()
            log('Navegador fechado.')
