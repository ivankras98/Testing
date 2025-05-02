import allure
from pages.authentication_page import AuthenticationPage
from pages.dashboard_page import DashboardPage
from utils.logger import logger

@allure.title("Проверка выхода из системы")
@allure.description("Проверяет выход из системы с возвратом на страницу авторизации.")
def test_logout(logged_in_page: DashboardPage):
    auth_page = logged_in_page.logout()
    assert auth_page.is_loaded(), "Страница авторизации не загружена после выхода"
    logger.info("Выход из системы успешно выполнен")