# test_login.py
import pytest
import allure
from pages.authentication_page import AuthenticationPage
from pages.dashboard_page import DashboardPage
from playwright.sync_api import Page
from settings import EMAIL, PASSWORD
from utils.logger import logger

@pytest.mark.smoke
@pytest.mark.feature("authentication")
@allure.title("Проверка успешного входа в систему")
@allure.description("Проверяет успешный вход с валидными данными с редиректом на страницу /dashboard.")
def test_login(page: Page):
    with allure.step("Открыть страницу авторизации с помощью метода navigate()"):
        auth_page = AuthenticationPage(page).navigate()
    with allure.step("Ввести email в поле с селектором '#email'"):
        auth_page.fill_email(EMAIL)
    with allure.step("Ввести пароль в поле с селектором '#password'"):
        auth_page.fill_password(PASSWORD)
    with allure.step("Нажать кнопку 'Войти' с селектором 'button[type='submit']'"):
        dashboard_page = auth_page.submit_login()
    with allure.step("Проверить загрузку дашборда по URL и видимости элемента"):
        assert dashboard_page.is_loaded(), "Дашборд не загружен после входа"
        try:
            page.wait_for_selector("h1, h2, div[class*='dashboard']", state="visible", timeout=5000)
            logger.info("Найден элемент, характерный для страницы /dashboard")
        except Exception as e:
            logger.error("Уникальный элемент на /dashboard не найден, полагаемся на URL")
            allure.attach(page.content(), name="HTML страницы при ошибке", attachment_type=allure.attachment_type.HTML)
            raise e