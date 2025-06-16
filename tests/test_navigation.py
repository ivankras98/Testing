import pytest
import os
from dotenv import load_dotenv
from playwright.sync_api import expect, TimeoutError as PlaywrightTimeoutError
from allure import title, step
from utils.logger import logger
from settings import BASE_URL, EMAIL, PASSWORD
from pages.authentication_page import AuthenticationPage
from pages.dashboard_page import DashboardPage

# Загрузка переменных из .env
load_dotenv()

@pytest.mark.navigation
@title("Загрузка дашборда")
def test_homepage_loads(page):
    auth_page = AuthenticationPage(page)
    with step("Переход на страницу авторизации"):
        auth_page.navigate()
    with step("Авторизация"):
        auth_page.login(EMAIL, PASSWORD)
    with step("Переход на дашборд"):
        page.goto(f"{BASE_URL}/dashboard", timeout=60000, wait_until="domcontentloaded")
    with step("Проверка загрузки дашборда"):
        expect(page).to_have_url(f"{BASE_URL}/dashboard", timeout=60000)

@pytest.mark.navigation
@title("Переход в раздел сообщений")
def test_messages_navigation(page):
    auth_page = AuthenticationPage(page)
    with step("Переход на страницу авторизации"):
        auth_page.navigate()
    with step("Авторизация"):
        auth_page.login(EMAIL, PASSWORD)
    with step("Переход на дашборд"):
        page.goto(f"{BASE_URL}/dashboard", timeout=60000, wait_until="domcontentloaded")
    dashboard_page = DashboardPage(page)
    with step("Переход в раздел сообщений"):
        dashboard_page.go_to_messages()
    with step("Проверка перехода на страницу сообщений"):
        expect(dashboard_page.page).to_have_url(f"{BASE_URL}/messages", timeout=60000)

@pytest.mark.navigation
@title("Переход в раздел участников")
def test_members_navigation(page):
    auth_page = AuthenticationPage(page)
    with step("Переход на страницу авторизации"):
        auth_page.navigate()
    with step("Авторизация"):
        auth_page.login(EMAIL, PASSWORD)
    with step("Переход на дашборд"):
        page.goto(f"{BASE_URL}/dashboard", timeout=60000, wait_until="domcontentloaded")
    dashboard_page = DashboardPage(page)
    with step("Переход в раздел участников"):
        dashboard_page.go_to_members()
    with step("Проверка перехода на страницу участников"):
        expect(dashboard_page.page).to_have_url(f"{BASE_URL}/members", timeout=60000)

@pytest.mark.navigation
@title("Переход в раздел настроек")
def test_navigate_to_settings(page):
    auth_page = AuthenticationPage(page)
    with step("Переход на страницу авторизации"):
        auth_page.navigate()
    with step("Авторизация"):
        auth_page.login(EMAIL, PASSWORD)
    with step("Переход на дашборд"):
        page.goto(f"{BASE_URL}/dashboard", timeout=60000, wait_until="domcontentloaded")
    dashboard_page = DashboardPage(page)
    with step("Переход в раздел настроек"):
        dashboard_page.navigate_to(f"{BASE_URL}/settings")
    with step("Проверка ошибки 404"):
        expect(dashboard_page.page).to_have_url(f"{BASE_URL}/settings", timeout=60000)
        try:
            dashboard_page.page.wait_for_selector("h1.next-error-h1:has-text('404')", state="visible", timeout=60000)
            expect(dashboard_page.page.locator("h1.next-error-h1:has-text('404')")).to_be_visible(timeout=60000)
            expect(dashboard_page.page.locator("h2:has-text('This page could not be found')")).to_be_visible(timeout=60000)
        except PlaywrightTimeoutError as e:
            logger.error(f"404 page elements not visible: {e}")
            dashboard_page.take_screenshot("settings_404_error.png")
            allure.attach.file("settings_404_error.png", name="404 error screenshot", attachment_type=allure.attachment_type.PNG)
            raise

@pytest.mark.navigation
@title("Переход на несуществующую страницу")
def test_nonexistent_page(page):
    auth_page = AuthenticationPage(page)
    with step("Переход на страницу авторизации"):
        auth_page.navigate()
    with step("Авторизация"):
        auth_page.login(EMAIL, PASSWORD)
    with step("Переход на несуществующую страницу"):
        auth_page.navigate_to(f"{BASE_URL}/nonexistent")
    with step("Проверка ошибки 404"):
        expect(auth_page.page).to_have_url(f"{BASE_URL}/nonexistent", timeout=60000)
        try:
            auth_page.page.wait_for_selector("h1.next-error-h1:has-text('404')", state="visible", timeout=60000)
            expect(auth_page.page.locator("h1.next-error-h1:has-text('404')")).to_be_visible(timeout=60000)
            expect(auth_page.page.locator("h2:has-text('This page could not be found')")).to_be_visible(timeout=60000)
        except PlaywrightTimeoutError as e:
            logger.error(f"404 page elements not visible: {e}")
            auth_page.take_screenshot("nonexistent_404_error.png")
            allure.attach.file("nonexistent_404_error.png", name="404 error screenshot", attachment_type=allure.attachment_type.PNG)
            raise

@pytest.mark.navigation
@title("Переход на дашборд без авторизации")
def test_dashboard_without_login(page):
    auth_page = AuthenticationPage(page)
    with step("Переход на дашборд"):
        auth_page.navigate(f"{BASE_URL}/dashboard")
    with step("Проверка редиректа на страницу авторизации"):
        expect(auth_page.page).to_have_url(f"{BASE_URL}/authentication", timeout=60000)
        expect(auth_page.email_input).to_be_visible(timeout=60000)
        expect(auth_page.password_input).to_be_visible(timeout=60000)
        expect(auth_page.submit_button).to_be_visible(timeout=60000)

@pytest.mark.navigation
@title("Переход на проекты без авторизации")
def test_projects_without_login(page):
    auth_page = AuthenticationPage(page)
    with step("Переход на проекты"):
        auth_page.navigate(f"{BASE_URL}/projects")
    with step("Проверка редиректа на страницу авторизации"):
        expect(auth_page.page).to_have_url(f"{BASE_URL}/authentication", timeout=60000)
        expect(auth_page.email_input).to_be_visible(timeout=60000)
        expect(auth_page.password_input).to_be_visible(timeout=60000)
        expect(auth_page.submit_button).to_be_visible(timeout=60000)

@pytest.mark.navigation
@title("Переход на задачи без авторизации")
def test_tasks_without_login(page):
    auth_page = AuthenticationPage(page)
    with step("Переход на задачи"):
        auth_page.navigate(f"{BASE_URL}/tasks")
    with step("Проверка редиректа на страницу авторизации"):
        expect(auth_page.page).to_have_url(f"{BASE_URL}/authentication", timeout=60000)
        expect(auth_page.email_input).to_be_visible(timeout=60000)
        expect(auth_page.password_input).to_be_visible(timeout=60000)
        expect(auth_page.submit_button).to_be_visible(timeout=60000)

@pytest.mark.navigation
@title("Переход на участников без авторизации")
def test_members_without_login(page):
    auth_page = AuthenticationPage(page)
    with step("Переход на участников"):
        auth_page.navigate(f"{BASE_URL}/members")
    with step("Проверка редиректа на страницу авторизации"):
        expect(auth_page.page).to_have_url(f"{BASE_URL}/authentication", timeout=60000)
        expect(auth_page.email_input).to_be_visible(timeout=60000)
        expect(auth_page.password_input).to_be_visible(timeout=60000)
        expect(auth_page.submit_button).to_be_visible(timeout=60000)

@pytest.mark.navigation
@title("Переход на сообщения без авторизации")
def test_messages_without_login(page):
    auth_page = AuthenticationPage(page)
    with step("Переход на сообщения"):
        auth_page.navigate(f"{BASE_URL}/messages")
    with step("Проверка редиректа на страницу авторизации"):
        expect(auth_page.page).to_have_url(f"{BASE_URL}/authentication", timeout=60000)
        expect(auth_page.email_input).to_be_visible(timeout=60000)
        expect(auth_page.password_input).to_be_visible(timeout=60000)
        expect(auth_page.submit_button).to_be_visible(timeout=60000)