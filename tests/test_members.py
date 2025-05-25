import allure
import os
from playwright.sync_api import Page
from pages.authentication_page import AuthenticationPage
from pages.dashboard_page import DashboardPage
from pages.members_page import MembersPage
from utils.logger import logger

@allure.title("Тестирование перехода в раздел участников")
@allure.description("Проверяет переход с главной страницы в раздел участников через кнопку.")
def test_members_navigation(page: Page):
    console_logs = []
    network_logs = []

    # Логирование консоли и сети
    page.on("console", lambda msg: console_logs.append(msg.text))
    page.on("request", lambda req: network_logs.append(f"Request: {req.url}"))
    page.on("response", lambda res: network_logs.append(f"Response: {res.url} - {res.status}"))

    # Авторизация
    auth_page = AuthenticationPage(page)
    auth_page.navigate()
    auth_page.fill_email(os.getenv("EMAIL"))
    auth_page.fill_password(os.getenv("PASSWORD"))
    dashboard_page = auth_page.submit_login()

    # Проверка загрузки главной страницы
    assert dashboard_page.is_loaded(), "Главная страница не загрузилась"

    # Переход в раздел участников
    members_page = dashboard_page.go_to_members()

    # Проверка загрузки страницы участников
    assert members_page.is_loaded(), "Страница участников не загрузилась"

    # Прикрепление логов к Allure
    with allure.step("Прикрепление логов консоли"):
        allure.attach("\n".join(console_logs), name="Console Logs", attachment_type=allure.attachment_type.TEXT)
    with allure.step("Прикрепление логов сети"):
        allure.attach("\n".join(network_logs), name="Network Logs", attachment_type=allure.attachment_type.TEXT)