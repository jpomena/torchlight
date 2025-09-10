from bs4 import BeautifulSoup


class HTMLParser:
    def soupfy_html_element(self, html_element):
        html_element_soup = BeautifulSoup(html_element, 'html.parser')
        return html_element_soup
