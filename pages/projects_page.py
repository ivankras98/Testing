from playwright.sync_api import Page
from pages.base_page import BasePage
import allure
from settings import BASE_URL
from utils.logger import logger

class ProjectsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{BASE_URL}/dashboard"  # Раздел MY PROJECTS на странице Dashboard
        self.my_projects_label = page.locator("p.text-sm.font-medium.text-gray-500:has-text('MY PROJECTS')")
        self.create_project_button = page.locator("div.flex.justify-between.items-center >> button:has(svg.lucide-plus)")
        self.project_name_input = page.locator("input[placeholder='Project Name']")
        self.project_description_input = page.locator("textarea[placeholder='Project Description']")
        self.start_date_input = page.locator("input[placeholder='ДД.ММ.ГГГГ']").first
        self.end_date_input = page.locator("input[placeholder='ДД.ММ.ГГГГ']").last
        self.status_dropdown = page.locator("select")
        self.create_button = page.locator("button:has-text('Create')")


    @allure.step("Переход на дашборд для доступа к разделу проектов")
    def navigate(self):
        logger.info(f"Переход на страницу дашборда: {self.url}")
        self.page.goto(self.url, wait_until="networkidle", timeout=60000)
        logger.info(f"Текущий URL: {self.page.url}")
        return self


    @allure.step("Открытие формы создания проекта")
    def open_create_project_form(self):
        try:
            self.wait_for_selector("p.text-sm.font-medium.text-gray-500:has-text('MY PROJECTS')", timeout=60000)
            self.my_projects_label.wait_for(state="visible")
            logger.info("Элемент MY PROJECTS виден")
        except Exception as e:
            logger.error(f"Ошибка ожидания элемента MY PROJECTS: {e}")
            self.take_screenshot("my_projects_error.png")
            allure.attach.file("my_projects_error.png", name="Скриншот ошибки MY PROJECTS", attachment_type=allure.attachment_type.PNG)
            raise
        
        try:
            self.create_project_button.wait_for(state="visible", timeout=10000)
            self.create_project_button.click()
            logger.info("Кликнули на кнопку '+' для открытия формы создания проекта")
        except Exception as e:
            logger.error(f"Ошибка ожидания или клика на кнопку '+': {e}")
            self.take_screenshot("create_project_button_error.png")
            allure.attach.file("create_project_button_error.png", name="Скриншот ошибки кнопки создания проекта", attachment_type=allure.attachment_type.PNG)
            raise
        
        self.wait_for_selector("input[placeholder='Project Name']", timeout=10000)
        logger.info("Форма создания проекта открыта")
        return self


    @allure.step("Заполнение формы создания проекта: Имя={name}, Описание={description}, Дата начала={start_date}, Дата окончания={end_date}, Статус={status}")
    def fill_create_project_form(self, name: str, description: str, start_date: str, end_date: str, status: str):
        self.project_name_input.fill(name)
        logger.info(f"Поле Project Name заполнено: {name}")
        self.project_description_input.fill(description)
        logger.info(f"Поле Project Description заполнено: {description}")
        self.start_date_input.fill(start_date)
        logger.info(f"Поле Start Date заполнено: {start_date}")
        self.end_date_input.fill(end_date)
        logger.info(f"Поле End Date заполнено: {end_date}")
        self.status_dropdown.select_option(status)
        logger.info(f"Выбран статус: {status}")
        return self


    @allure.step("Отправка формы создания проекта")
    def submit_create_project_form(self):
        self.create_button.click()
        logger.info("Кликнули на кнопку 'Create'")
        try:
            self.page.wait_for_selector("input[placeholder='Project Name']", state="detached", timeout=10000)
            logger.info("Форма создания проекта закрыта")
        except Exception as e:
            logger.error(f"Ошибка ожидания закрытия формы: {e}")
            self.take_screenshot("create_project_error.png")
            allure.attach.file("create_project_error.png", name="Скриншот ошибки создания проекта", attachment_type=allure.attachment_type.PNG)
            raise
        return self