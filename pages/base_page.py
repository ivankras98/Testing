# pages/base_page.py
from playwright.sync_api import Page
from utils.logger import logger
from dotenv import load_dotenv
import allure
import os


load_dotenv()

class BasePage:
    BASE_URL = os.getenv("BASE_URL")
    API_URL = os.getenv("API_URL")

    def __init__(self, page):
        self.page = page

    @allure.step("Переход на URL: {url}")
    def navigate_to(self, url: str):
        logger.info(f"Переход на {url}")
        try:
            self.page.goto(url, wait_until="networkidle", timeout=60000)
            logger.info(f"Успешно перешёл на {url}")
        except Exception as e:
            logger.error(f"Не удалось перейти на {url}: {e}")
            allure.attach(self.page.content(), name="navigation_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(self.page.screenshot(), name="navigation_error.png", attachment_type=allure.attachment_type.PNG)
            raise

    @allure.step("Ожидание видимости элемента")
    def wait_for_selector(self, selector: str, timeout: int = 60000):
        logger.info(f"Ожидание элемента: {selector}")
        try:
            self.page.wait_for_selector(selector, state="visible", timeout=timeout)
        except Exception as e:
            logger.error(f"Элемент {selector} не найден: {e}")
            allure.attach(self.page.content(), name="selector_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(self.page.screenshot(), name="selector_error.png", attachment_type=allure.attachment_type.PNG)
            raise

    @allure.step("Сохранение скриншота")
    def take_screenshot(self, filename: str):
        logger.info(f"Сохранение скриншота: {filename}")
        self.page.screenshot(path=filename)