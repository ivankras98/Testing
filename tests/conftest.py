import pytest
import os
from playwright.sync_api import Playwright, Page
from pages.authentication_page import AuthenticationPage
from pages.dashboard_page import DashboardPage
from settings import BASE_URL
from utils.logger import logger

def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: mark test as smoke test")
    config.addinivalue_line("markers", "regression: mark test as regression test")
    config.addinivalue_line("markers", "auth: mark test as authentication test")
    config.addinivalue_line("markers", "projects: mark test as projects test")
    config.addinivalue_line("markers", "tasks: mark test as tasks test")
    config.addinivalue_line("markers", "navigation: mark test as navigation test")

@pytest.fixture(scope="session")
def browser(playwright: Playwright):
    headless = os.getenv("HEADLESS", "true").lower() == "false"
    logger.info(f"Запуск браузера Chromium в режиме headless={headless}")
    browser = playwright.chromium.launch(headless=headless)
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
def auth_page(page: Page):
    return AuthenticationPage(page)

@pytest.fixture(scope="function")
def authenticated_page(page: Page, auth_page):
    logger.info("Выполнение авторизации для получения страницы дашборда")
    auth_page.navigate()
    auth_page.ensure_logged_out()
    dashboard = auth_page.login(os.getenv("EMAIL", "test@example.com"), os.getenv("PASSWORD", "password"))
    page.evaluate("window.localStorage.setItem('authToken', 'test-token')")
    yield page
    page.evaluate("window.localStorage.clear()")

@pytest.fixture(scope="function")
def dashboard_page(authenticated_page):
    return DashboardPage(authenticated_page)