from playwright.sync_api import Page
from pages.base_page import BasePage
import allure
from settings import BASE_URL
from utils.logger import logger

class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = BASE_URL


    @allure.step("Переход на главную страницу")
    def navigate(self):
        logger.info(f"Переход на главную страницу: {self.url}")
        self.page.goto(self.url, wait_until="networkidle", timeout=60000)
        logger.info(f"Текущий URL: {self.page.url}")
        return self


    @allure.step("Проверка загрузки главной страницы с заголовком 'ProjectM'")
    def is_loaded(self):
        title = self.page.title()
        is_loaded = "ProjectM" in title
        if is_loaded:
            logger.info(f"Главная страница загрузилась успешно, заголовок: {title}")
        return is_loaded