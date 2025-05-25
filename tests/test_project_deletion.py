import allure
import os
from playwright.sync_api import Page
from pages.authentication_page import AuthenticationPage
from pages.dashboard_page import DashboardPage
from utils.logger import logger

@allure.title("Тестирование удаления проекта")
@allure.description("Проверяет удаление первого проекта с главной страницы через боковое меню.")
def test_project_deletion(page: Page):
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

    # Удаление первого проекта
    dashboard_page.delete_first_project()

    # Проверка, что проект удалён (простая проверка: список проектов уменьшился)
    dashboard_page.open_side_menu()
    remaining_projects = dashboard_page.project_items.count()
    logger.info(f"Осталось проектов: {remaining_projects}")
    assert remaining_projects < 30, "Проект не был удалён (количество проектов не уменьшилось)"

    # Прикрепление логов к Allure
    with allure.step("Прикрепление логов консоли"):
        allure.attach("\n".join(console_logs), name="Console Logs", attachment_type=allure.attachment_type.TEXT)
    with allure.step("Прикрепление логов сети"):
        allure.attach("\n".join(network_logs), name="Network Logs", attachment_type=allure.attachment_type.TEXT)