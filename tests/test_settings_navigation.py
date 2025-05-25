import allure
import pytest
from utils.logger import logger
from settings import BASE_URL
from pages.dashboard_page import DashboardPage

@allure.title("Проверка перехода на страницу настроек")
@allure.description("Проверяет переход на страницу настроек с дашборда, но ожидает ошибку 404.")
@pytest.mark.regression
def test_navigate_to_settings(logged_in_page):
    dashboard_page = DashboardPage(logged_in_page.page)
    
    with allure.step("Переходим в раздел настроек"):
        settings_page = dashboard_page.go_to_settings()
    
    with allure.step("Проверяем URL страницы настроек"):
        current_url = logged_in_page.page.url
        logger.info(f"Текущий URL: {current_url}")
        assert current_url == f"{BASE_URL}/settings", "Не удалось перейти на страницу настроек"

    with allure.step("Проверяем наличие ошибки 404 на странице настроек"):
        assert settings_page.is_error_404_displayed(), "Ошибка 404 не отображается на странице настроек"
