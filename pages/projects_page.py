# pages/project_page.py
from playwright.sync_api import Page
from pages.base_page import BasePage
import allure
from settings import BASE_URL
from utils.logger import logger

class ProjectPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{BASE_URL}/projects"

    @allure.step("Открыть страницу создания проекта")
    def navigate(self):
        logger.info(f"Переход на страницу проектов: {self.url}")
        self.page.goto(self.url, wait_until="networkidle", timeout=60000)
        logger.info(f"Текущий URL: {self.page.url}")
        return self

    @allure.step("Ввести название '{name}' в поле 'input[name='projectName']'")
    def enter_project_name(self, name):
        self.page.fill("input[name='projectName']", name)
        logger.info(f"Введено название проекта: {name}")
        return self

    @allure.step("Нажать кнопку 'Создать' с селектором 'button[type='submit']'")
    def click_create(self):
        self.page.click("button[type='submit']")
        logger.info("Нажата кнопка создания проекта")
        return self

    @allure.step("Проверить, что отображается проект '{name}'")
    def is_project_visible(self, name):
        return self.page.is_visible(f"text={name}")