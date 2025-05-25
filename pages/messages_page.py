import allure
import os
from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.logger import logger

class MessagesPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{os.getenv('BASE_URL')}/messages"

    @allure.step("Проверка загрузки страницы сообщений")
    def is_loaded(self):
        logger.info(f"Проверка URL страницы сообщений: {self.page.url}")
        return self.page.url == self.url

    @allure.step("Проверка наличия текста 'No chat selected'")
    def has_no_chat_text(self):
        logger.info("Проверка наличия текста 'No chat selected'")
        return self.page.locator("text='No chat selected'").is_visible()