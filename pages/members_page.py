# pages/members_page.py
import allure
from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.logger import logger

class MembersPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.BASE_URL}/members"

    @allure.step("Проверка загрузки страницы участников")
    def is_loaded(self):
        logger.info(f"Проверка URL страницы участников: {self.page.url}")
        self.page.wait_for_url(self.url, wait_until="networkidle", timeout=60000)
        return self.page.url == self.url