import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# tests/conftest.py
import pytest
from playwright.sync_api import sync_playwright, Playwright, Page
from pages.authentication_page import AuthenticationPage
from pages.dashboard_page import DashboardPage
from settings import EMAIL, PASSWORD
from utils.logger import logger

@pytest.fixture(scope="session")
def playwright():
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser(playwright: Playwright):
    browser = playwright.chromium.launch(headless=True)
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    page.close()

@pytest.fixture(scope="function")
def auth_page(page: Page):
    return AuthenticationPage(page).navigate()

@pytest.fixture(scope="function")
def logged_in_page(page: Page):
    auth_page = AuthenticationPage(page).navigate()
    return auth_page.enter_email(EMAIL).enter_password(PASSWORD).click_login()