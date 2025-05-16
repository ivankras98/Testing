# test_home.py
import pytest
import allure
from pages.home_page import HomePage
from playwright.sync_api import Page


@pytest.mark.smoke
@pytest.mark.homepage
@allure.title("Проверка загрузки главной страницы")
@allure.description("Проверяет редирект на страницу авторизации при отсутствии авторизации.")
def test_homepage_loads(page: Page):
    with allure.step("Открыть главную страницу"):
        home_page = HomePage(page).navigate()
    with allure.step("Проверить редирект на страницу авторизации"):
        assert "authentication" in page.url, "Ожидался редирект на страницу авторизации"