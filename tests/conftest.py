# conftest.py
import pytest
from playwright.sync_api import Playwright, Page
from pages.authentication_page import AuthenticationPage
from pages.dashboard_page import DashboardPage
from settings import EMAIL, PASSWORD
from utils.logger import logger

def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: mark test as smoke test")
    config.addinivalue_line("markers", "regression: mark test as regression test")
    config.addinivalue_line("markers", "feature: mark test with feature name")

@pytest.fixture(scope="session")
def browser(playwright: Playwright):
    logger.info("Запуск браузера Chromium в режиме без headless")
    browser = playwright.chromium.launch(headless=False)
    yield browser
    logger.info("Закрытие браузера")
    browser.close()

@pytest.fixture(scope="function")
def page(browser):
    logger.info("Создание новой страницы")
    context = browser.new_context()
    page = context.new_page()
    page.on("console", lambda msg: logger.info(f"Консоль: {msg.text}"))
    page.on("request", lambda req: logger.info(f"Запрос: {req.method} {req.url}"))
    page.on("response", lambda res: logger.info(f"Ответ: {res.status} {res.url}"))
    yield page
    logger.info("Закрытие контекста страницы")
    context.close()

@pytest.fixture(scope="function")
def logged_in_page(page: Page):
    logger.info("Выполнение авторизации для получения страницы дашборда")
    auth_page = AuthenticationPage(page).navigate()
    dashboard_page = auth_page.login(EMAIL, PASSWORD)
    return dashboard_page