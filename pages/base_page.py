# base_page.py
from playwright.sync_api import Page
from utils.logger import logger
import allure

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    @allure.step("Ожидание видимости элемента с селектором '{selector}'")
    def wait_for_selector(self, selector: str, timeout: int = 60000):
        """Ожидание видимости элемента."""
        logger.info(f"Ожидание элемента: {selector}")
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)

    @allure.step("Сохранение скриншота с именем '{filename}'")
    def take_screenshot(self, filename: str):
        """Сохранение скриншота при ошибке."""
        logger.info(f"Сохранение скриншота: {filename}")
        self.page.screenshot(path=filename)