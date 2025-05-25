import allure
import os
from playwright.sync_api import Page
from pages.authentication_page import AuthenticationPage
from pages.dashboard_page import DashboardPage
from pages.project_view_page import ProjectViewPage
from utils.logger import logger

@allure.title("Тестирование создания задачи в третьем проекте")
@allure.description("Проверяет создание новой задачи в третьем проекте на странице проекта.")
def test_task_creation(page: Page):
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

    # Открытие третьего проекта
    project_page, project_id = dashboard_page.open_third_project()
    assert project_page.is_loaded(project_id), f"Страница проекта {project_id} не загрузилась"

    # Создание задачи
    project_page.open_create_task_form()
    project_page.fill_task_form()
    project_page.create_task()

    # Проверка (например, можно проверить, что задача появилась на странице)
    # Здесь можно добавить проверку наличия новой задачи, если есть уникальный селектор
    logger.info("Задача успешно создана")

    # Прикрепление логов к Allure
    with allure.step("Прикрепление логов консоли"):
        allure.attach("\n".join(console_logs), name="Console Logs", attachment_type=allure.attachment_type.TEXT)
    with allure.step("Прикрепление логов сети"):
        allure.attach("\n".join(network_logs), name="Network Logs", attachment_type=allure.attachment_type.TEXT)