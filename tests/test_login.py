# tests/test_login.py
import allure
from settings import EMAIL, PASSWORD
from pages.authentication_page import AuthenticationPage
from playwright.sync_api import Page

@allure.title("Проверка входа в систему")
@allure.description("Проверяет успешный вход с валидными данными на страницу /dashboard.")
def test_login(auth_page):
    with allure.step("Перейти на страницу авторизации с помощью метода navigate()"):
        auth_page.navigate()
    with allure.step("Ввести email в поле 'input[name='email']'"):
        auth_page.enter_email(EMAIL)
    with allure.step("Ввести пароль в поле 'input[name='password']'"):
        auth_page.enter_password(PASSWORD)
    with allure.step("Нажать кнопку 'Войти' с селектором 'button[type='submit']'"):
        dashboard_page = auth_page.click_login()
    with allure.step("Проверить, что появляется дашборд"):
        assert dashboard_page.is_dashboard_visible(), "Дашборд не отображается"