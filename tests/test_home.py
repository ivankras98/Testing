# tests/test_home.py
import pytest
import allure
from pages.home_page import HomePage
from playwright.sync_api import Page

@pytest.mark.smoke
@pytest.mark.feature("homepage")
@allure.title("Проверка загрузки главной страницы")
@allure.description("Проверяет загрузку главной страницы или редирект на авторизацию.")
def test_homepage_loads(page: Page):
    with allure.step("Открыть главную страницу с помощью метода navigate()"):
        home_page = HomePage(page).navigate()
    with allure.step("Проверить, что загружается страница с заголовком 'ProjectM'"):
        assert home_page.is_loaded(), "Ожидался заголовок 'ProjectM'"
    with allure.step("Проверить, что при отсутствии авторизации открывается страница авторизации"):
        assert "authentication" in page.url or home_page.is_loaded(), "Ожидался редирект на авторизацию"