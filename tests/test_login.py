# test_login.py
import pytest
import allure
from pages.authentication_page import AuthenticationPage
from pages.dashboard_page import DashboardPage
from playwright.sync_api import Page
from settings import EMAIL, PASSWORD
from utils.logger import logger


@pytest.mark.smoke
@pytest.mark.authentication
@allure.title("Проверка успешного входа в систему")
@allure.description("Проверяет успешный вход с валидными данными с редиректом на страницу /dashboard.")
def test_login(page: Page):
    with allure.step("Открыть страницу авторизации"):
        auth_page = AuthenticationPage(page).navigate()
    with allure.step("Ввести email и пароль"):
        auth_page.fill_email(EMAIL)
        auth_page.fill_password(PASSWORD)
    with allure.step("Нажать кнопку 'Войти'"):
        dashboard_page = auth_page.submit_login()
    with allure.step("Проверить загрузку дашборда"):
        assert dashboard_page.is_loaded(), "Дашборд не загружен после входа"
        try:
            page.wait_for_selector("h1, h2, div[class*='dashboard']", state="visible", timeout=5000)
            logger.info("Найден элемент, характерный для страницы /dashboard")
        except Exception as e:
            logger.error("Уникальный элемент на /dashboard не найден, полагаемся на URL")
            allure.attach(page.content(), name="HTML страницы при ошибке", attachment_type=allure.attachment_type.HTML)
            raise e