# project_page.py
import random
from datetime import datetime, timedelta
from playwright.sync_api import Page
from pages.base_page import BasePage
import allure
from settings import BASE_URL
from utils.logger import logger


class ProjectPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{BASE_URL}/dashboard"
        self.plus_button = page.locator("button:has(svg.lucide-plus)")
        self.project_name_input = page.locator("input[placeholder='Project Name']")
        self.description_input = page.locator("textarea[placeholder='Project Description']")
        self.start_date_input = page.locator("input[placeholder='Start Date']")
        self.end_date_input = page.locator("input[placeholder='End Date']")
        self.status_select = page.locator("select")
        self.create_button = page.locator("button[type='submit']")


    @allure.step("Переход на страницу дашборда")
    def navigate(self):
        logger.info(f"Переход на страницу дашборда: {self.url}")
        self.page.goto(self.url, wait_until="networkidle", timeout=120000)
        logger.info(f"Текущий URL после загрузки: {self.page.url}")
        return self


    @allure.step("Открытие формы создания проекта")
    def open_create_project_form(self):
        with allure.step("Ожидание видимости кнопки 'плюсик'"):
            self.wait_for_selector("button:has(svg.lucide-plus)", timeout=120000)
        self.plus_button.click()
        logger.info("Кликнули на кнопку 'плюсик' для открытия формы")


    @allure.step("Заполнение поля 'Project Name'")
    def fill_project_name(self):
        project_name = f"Project-{random.randint(1000, 9999)}"
        with allure.step("Ожидание видимости поля 'Project Name'"):
            self.wait_for_selector("input[placeholder='Project Name']", timeout=120000)
        self.project_name_input.fill(project_name)
        logger.info(f"Поле 'Project Name' заполнено: {project_name}")
        return project_name


    @allure.step("Заполнение поля 'Description'")
    def fill_description(self):
        description = f"Description-{random.randint(1000, 9999)}"
        with allure.step("Ожидание видимости поля 'Project Description'"):
            self.wait_for_selector("textarea[placeholder='Project Description']", timeout=120000)
        self.description_input.fill(description)
        logger.info(f"Поле 'Project Description' заполнено: {description}")
        return description


    @allure.step("Заполнение поля 'Start Date'")
    def fill_start_date(self):
        start_date = datetime.now().strftime("%d.%m.%Y")
        start_date_for_input = datetime.now().strftime("%Y-%m-%d")
        with allure.step("Ожидание видимости поля 'Start Date'"):
            self.wait_for_selector("input[placeholder='Start Date']", timeout=120000)
        self.start_date_input.fill(start_date_for_input)
        logger.info(f"Поле 'Start Date' заполнено: {start_date}")
        return start_date


    @allure.step("Заполнение поля 'End Date'")
    def fill_end_date(self, start_date_str: str):
        start_date = datetime.strptime(start_date_str, "%d.%m.%Y")
        end_date = (start_date + timedelta(days=7)).strftime("%d.%m.%Y")
        end_date_for_input = (start_date + timedelta(days=7)).strftime("%Y-%m-%d")
        with allure.step("Ожидание видимости поля 'End Date'"):
            self.wait_for_selector("input[placeholder='End Date']", timeout=120000)
        self.end_date_input.fill(end_date_for_input)
        logger.info(f"Поле 'End Date' заполнено: {end_date}")
        return end_date


    @allure.step("Заполнение поля 'Status'")
    def fill_status(self):
        status_options = ["Not Started", "Planning", "In Progress", "Completed"]
        selected_status = random.choice(status_options)
        with allure.step("Ожидание видимости поля 'Status'"):
            self.wait_for_selector("select", timeout=120000)
        self.status_select.select_option(selected_status)
        logger.info(f"Поле 'Status' заполнено: {selected_status}")
        return selected_status


    @allure.step("Нажатие кнопки 'Create'")
    def submit_create_project(self):
        with allure.step("Ожидание, пока кнопка 'Create' станет активной"):
            self.page.wait_for_selector("button[type='submit']:not([disabled])", state="visible", timeout=120000)
        self.create_button.click()
        logger.info("Кликнули на кнопку 'Create' для создания проекта")


    @allure.step("Проверка отображения созданного проекта")
    def is_project_visible(self, project_name: str):
        with allure.step(f"Ожидание видимости проекта с названием '{project_name}'"):
            self.wait_for_selector(f"text='{project_name}'", timeout=120000)
        return self.page.locator(f"text='{project_name}'").is_visible()