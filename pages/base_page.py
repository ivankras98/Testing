# base_page.py
from playwright.sync_api import Page
from utils.logger import logger
import allure

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    @allure.step("Навигатор на URL")
    def navigate_to(self, url: str):
        logger.info(f"Navigating to {url}")
        try:
            self.page.goto(url)
            self.page.wait_for_load_state("networkidle")
            logger.info(f"Successfully navigated to {url}")
        except Exception as e:
            logger.error(f"Failed to navigate to {url}: {e}")
            allure.attach(self.page.content(), name="navigation_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(self.page.screenshot(), name="navigation_error.png", attachment_type=allure.attachment_type.PNG)
            raise

    @allure.step("Ожидание видимости элемента")
    def wait_for_selector(self, selector: str, timeout: int = 60000):
        """Ожидание видимости элемента."""
        logger.info(f"Ожидание элемента: {selector}")
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)

    @allure.step("Сохранение скриншота")
    def take_screenshot(self, filename: str):
        """Сохранение скриншота при ошибке."""
        logger.info(f"Сохранение скриншота: {filename}")
        self.page.screenshot(path=filename)