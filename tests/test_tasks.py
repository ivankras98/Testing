import allure
import pytest
from utils.logger import logger
from settings import BASE_URL
from pages.dashboard_page import DashboardPage

@allure.title("Проверка перехода на страницу задач")
@allure.description("Проверяет переход на страницу задач с дашборда и успешную загрузку страницы.")
@pytest.mark.regression
def test_navigate_to_tasks(logged_in_page):
    dashboard_page = DashboardPage(logged_in_page.page)
    
    with allure.step("Переходим в раздел задач"):
        tasks_page = dashboard_page.go_to_tasks()

    with allure.step("Проверяем URL страницы задач"):
        current_url = logged_in_page.page.url
        logger.info(f"Текущий URL: {current_url}")
        assert current_url == f"{BASE_URL}/tasks", "Не удалось перейти на страницу задач"

    with allure.step("Проверяем успешную загрузку страницы задач"):
        assert tasks_page.is_loaded(), "Страница задач не загрузилась корректно"
