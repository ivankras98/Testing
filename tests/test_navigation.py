# tests/test_navigation.py
import pytest
import allure
from dotenv import load_dotenv
from playwright.sync_api import expect, TimeoutError as PlaywrightTimeoutError
from allure import step, attach
from allure_commons.types import AttachmentType
from utils.logger import logger
from pages.authentication_page import AuthenticationPage
from pages.dashboard_page import DashboardPage

load_dotenv()


@pytest.fixture(scope="function")
def dashboard_page(authenticated_context):
    page = authenticated_context.new_page()
    dashboard_page = DashboardPage(page)
    yield dashboard_page
    page.close()


@pytest.mark.navigation
@pytest.mark.smoke
@allure.title("Загрузка дашборда после авторизации")
def test_homepage_loads(dashboard_page: DashboardPage):
    with step("Открыть дашборд"):
        dashboard_page.navigate_to(f"{dashboard_page.BASE_URL}/dashboard")
    with step("Проверить загрузку дашборда"):
        logger.info(f"Текущий URL: {dashboard_page.page.url}")
        expect(dashboard_page.page).to_have_url(f"{dashboard_page.BASE_URL}/dashboard", timeout=30000)
        assert dashboard_page.is_loaded(), "Дашборд не загружен"
        attach(dashboard_page.page.screenshot(), name="дашборд_загружен.png", attachment_type=AttachmentType.PNG)


@pytest.mark.navigation
@pytest.mark.regression
@allure.title("Переход в раздел сообщений")
def test_messages_navigation(dashboard_page: DashboardPage):
    with step("Открыть раздел сообщений"):
        dashboard_page.go_to_messages()
    with step("Проверить переход в раздел сообщений"):
        logger.info(f"Текущий URL: {dashboard_page.page.url}")
        expect(dashboard_page.page).to_have_url(f"{dashboard_page.BASE_URL}/messages", timeout=30000)
        attach(dashboard_page.page.screenshot(), name="страница_сообщений_загружена.png", attachment_type=AttachmentType.PNG)


@pytest.mark.navigation
@pytest.mark.regression
@allure.title("Переход в раздел участников")
def test_members_navigation(dashboard_page: DashboardPage):
    with step("Открыть раздел участников"):
        dashboard_page.go_to_members()
    with step("Проверить переход в раздел участников"):
        logger.info(f"Текущий URL: {dashboard_page.page.url}")
        expect(dashboard_page.page).to_have_url(f"{dashboard_page.BASE_URL}/members", timeout=30000)
        attach(dashboard_page.page.screenshot(), name="страница_участников_загружена.png", attachment_type=AttachmentType.PNG)


@pytest.mark.navigation
@pytest.mark.regression
@allure.title("Переход на несуществующую страницу")
def test_nonexistent_page(page):
    auth_page = AuthenticationPage(page)
    with step("Открыть несуществующую страницу"):
        auth_page.navigate_to(f"{auth_page.BASE_URL}/nonexistent")
        logger.info(f"Текущий URL: {auth_page.page.url}")
    with step("Проверить редирект на страницу авторизации"):
        expect(auth_page.page).to_have_url(f"{auth_page.BASE_URL}/authentication", timeout=30000)
        assert auth_page.is_loaded(), "Страница авторизации не загрузилась"
        expect(auth_page.email_input).to_be_visible(timeout=15000)
        expect(auth_page.password_input).to_be_visible(timeout=15000)
        expect(auth_page.submit_button).to_be_visible(timeout=15000)
        attach(auth_page.page.screenshot(), name="редирект_на_авторизацию_несуществующая.png", attachment_type=AttachmentType.PNG)


@pytest.mark.navigation
@pytest.mark.regression
@allure.title("Переход на дашборд без авторизации")
def test_dashboard_without_login(page):
    auth_page = AuthenticationPage(page)
    with step("Открыть дашборд"):
        auth_page.navigate_to(f"{auth_page.BASE_URL}/dashboard")
    with step("Проверить редирект на страницу авторизации"):
        logger.info(f"Текущий URL: {auth_page.page.url}")
        expect(auth_page.page).to_have_url(f"{auth_page.BASE_URL}/authentication", timeout=30000)
        assert auth_page.is_loaded(), "Страница авторизации не загрузилась"
        expect(auth_page.email_input).to_be_visible(timeout=15000)
        expect(auth_page.password_input).to_be_visible(timeout=15000)
        expect(auth_page.submit_button).to_be_visible(timeout=15000)
        attach(auth_page.page.screenshot(), name="редирект_на_авторизацию_дашборд.png", attachment_type=AttachmentType.PNG)


@pytest.mark.navigation
@pytest.mark.regression
@allure.title("Переход на проекты без авторизации")
def test_projects_without_login(page):
    auth_page = AuthenticationPage(page)
    with step("Открыть страницу проектов"):
        auth_page.navigate_to(f"{auth_page.BASE_URL}/projects")
    with step("Проверить редирект на страницу авторизации"):
        logger.info(f"Текущий URL: {auth_page.page.url}")
        expect(auth_page.page).to_have_url(f"{auth_page.BASE_URL}/authentication", timeout=30000)
        assert auth_page.is_loaded(), "Страница авторизации не загрузилась"
        expect(auth_page.email_input).to_be_visible(timeout=15000)
        expect(auth_page.password_input).to_be_visible(timeout=15000)
        expect(auth_page.submit_button).to_be_visible(timeout=15000)
        attach(auth_page.page.screenshot(), name="редирект_на_авторизацию_проекты.png", attachment_type=AttachmentType.PNG)


@pytest.mark.navigation
@pytest.mark.regression
@allure.title("Переход на задачи без авторизации")
def test_tasks_without_login(page):
    auth_page = AuthenticationPage(page)
    with step("Открыть страницу задач"):
        auth_page.navigate_to(f"{auth_page.BASE_URL}/tasks")
    with step("Проверить редирект на страницу авторизации"):
        logger.info(f"Текущий URL: {auth_page.page.url}")
        expect(auth_page.page).to_have_url(f"{auth_page.BASE_URL}/authentication", timeout=30000)
        assert auth_page.is_loaded(), "Страница авторизации не загрузилась"
        expect(auth_page.email_input).to_be_visible(timeout=15000)
        expect(auth_page.password_input).to_be_visible(timeout=15000)
        expect(auth_page.submit_button).to_be_visible(timeout=15000)
        attach(auth_page.page.screenshot(), name="редирект_на_авторизацию_задачи.png", attachment_type=AttachmentType.PNG)


@pytest.mark.navigation
@pytest.mark.regression
@allure.title("Переход на участников без авторизации")
def test_members_without_login(page):
    auth_page = AuthenticationPage(page)
    with step("Переход на участников"):
        auth_page.navigate_to(f"{auth_page.BASE_URL}/members")
    with step("Проверка редиректа на страницу авторизации"):
        logger.info(f"Текущий URL: {auth_page.page.url}")
        expect(auth_page.page).to_have_url(f"{auth_page.BASE_URL}/authentication", timeout=30000)
        assert auth_page.is_loaded(), "Страница авторизации не загрузилась"
        expect(auth_page.email_input).to_be_visible(timeout=15000)
        expect(auth_page.password_input).to_be_visible(timeout=15000)
        expect(auth_page.submit_button).to_be_visible(timeout=15000)
        attach(auth_page.page.screenshot(), name="members_auth_redirect.png", attachment_type=AttachmentType.PNG)


@pytest.mark.navigation
@pytest.mark.regression
@allure.title("Переход на сообщения без авторизации")
def test_messages_without_login(page):
    auth_page = AuthenticationPage(page)
    with step("Открыть страницу сообщений"):
        auth_page.navigate_to(f"{auth_page.BASE_URL}/messages")
    with step("Проверить редирект на страницу авторизации"):
        logger.info(f"Текущий URL: {auth_page.page.url}")
        expect(auth_page.page).to_have_url(f"{auth_page.BASE_URL}/authentication", timeout=30000)
        assert auth_page.is_loaded(), "Страница авторизации не загрузилась"
        expect(auth_page.email_input).to_be_visible(timeout=15000)
        expect(auth_page.password_input).to_be_visible(timeout=15000)
        expect(auth_page.submit_button).to_be_visible(timeout=15000)
        attach(auth_page.page.screenshot(), name="редирект_на_авторизацию_сообщения.png", attachment_type=AttachmentType.PNG)