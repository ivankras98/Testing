import pytest
from playwright.sync_api import Playwright, Page
from pages.authentication_page import AuthenticationPage
from pages.dashboard_page import DashboardPage
from settings import EMAIL, PASSWORD
from utils.logger import logger

@pytest.fixture(scope="session")
def browser(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    page.on("console", lambda msg: logger.info(f"Консоль: {msg.text}"))
    page.on("request", lambda req: logger.info(f"Запрос: {req.method} {req.url}"))
    page.on("response", lambda res: logger.info(f"Ответ: {res.status} {res.url}"))
    yield page
    context.close()


@pytest.fixture(scope="function")
def logged_in_page(page: Page):
    auth_page = AuthenticationPage(page).navigate()
    dashboard_page = auth_page.login(EMAIL, PASSWORD)
    return dashboard_page