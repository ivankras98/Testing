# tests/test_logout.py
import allure
from pages.dashboard_page import DashboardPage
from pages.authentication_page import AuthenticationPage
from playwright.sync_api import Page

@allure.title("Проверка выхода из системы")
@allure.description("Проверяет выход из системы с редиректом на страницу авторизации.")
def test_logout(logged_in_page):
    with allure.step("Перейти на дашборд с помощью метода navigate()"):
        dashboard_page = DashboardPage(logged_in_page)
    with allure.step("Нажать кнопку 'Выход' с селектором 'button#logout'"):
        auth_page = dashboard_page.click_logout()
    with allure.step("Проверить, что появляется страница авторизации"):
        assert "authentication" in auth_page.page.url, "Ожидалась страница авторизации"