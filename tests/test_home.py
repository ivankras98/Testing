import allure
from pages.home_page import HomePage
from utils.logger import logger

@allure.title("Проверка загрузки главной страницы")
@allure.description("Проверяет, что главная страница загружается и содержит заголовок 'ProjectM'.")
def test_homepage_loads(page: Page):
    home_page = HomePage(page).navigate()
    assert home_page.is_loaded(), "Главная страница не загрузилась или заголовок неверный"
    logger.info("Главная страница успешно загружена")