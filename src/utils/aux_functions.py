from selenium.webdriver.support.ui import WebDriverWait
from collections import defaultdict
from datetime import datetime

_subscribers = defaultdict(list)


def subscribe(event_type: str, fn):
    _subscribers[event_type].append(fn)


def publish(event_type: str, data):
    if event_type not in _subscribers:
        return

    for fn in _subscribers[event_type]:
        fn(data)


def log(message: str):
    now = datetime.now().strftime("%H:%M:%S")
    log_entry = f"[{now}] {message}"
    publish("log", log_entry)


def wait(driver, HTML_element=None, timeout=None):
    if not timeout:
        timeout = 45
    if not HTML_element:
        return WebDriverWait(driver, timeout)
    else:
        return WebDriverWait(HTML_element, timeout)
