# pages/project_page.py
from playwright.sync_api import Page
from pages.base_page import BasePage
import allure
from utils.logger import logger
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

class ProjectPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.BASE_URL}/dashboard"
        self.project_name_input = page.locator("input[placeholder='Project Name']")
        self.description_input = page.locator("textarea[placeholder='Project Description']")
        self.start_date_input = page.locator("input[placeholder='Start Date']")
        self.end_date_input = page.locator("input[placeholder='End Date']")
        self.status_select = page.locator("select.mb-4.block.w-full")
        self.create_button = page.locator("button[type='submit']")
        self.cancel_button = page.locator("button:has(svg.lucide.lucide-x)")

    @allure.step("Заполнение поля 'Project Name'")
    def fill_project_name(self, name: str):
        try:
            with allure.step("Ожидание видимости поля 'Project Name'"):
                self.wait_for_selector("input[placeholder='Project Name']", timeout=30000)
            self.project_name_input.fill(name)
            logger.info(f"Поле 'Project Name' заполнено: {name}")
        except PlaywrightTimeoutError as e:
            logger.error(f"Не удалось заполнить поле названия: {e}")
            allure.attach(self.page.content(), name="project_name_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(self.page.screenshot(), name="project_name_error.png", attachment_type=allure.attachment_type.PNG)
            raise
        return self

    @allure.step("Заполнение поля 'Description'")
    def fill_description(self, description: str):
        try:
            with allure.step("Ожидание видимости поля 'Project Description'"):
                self.wait_for_selector("textarea[placeholder='Project Description']", timeout=30000)
            self.description_input.fill(description)
            logger.info(f"Поле 'Project Description' заполнено: {description}")
        except PlaywrightTimeoutError as e:
            logger.error(f"Не удалось заполнить поле описания: {e}")
            allure.attach(self.page.content(), name="description_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(self.page.screenshot(), name="description_error.png", attachment_type=allure.attachment_type.PNG)
            raise
        return self

    @allure.step("Заполнение поля 'Start Date'")
    def fill_start_date(self, date: str):
        try:
            with allure.step("Ожидание видимости поля 'Start Date'"):
                self.wait_for_selector("input[placeholder='Start Date']", timeout=30000)
            self.start_date_input.fill(date)
            logger.info(f"Поле 'Start Date' заполнено: {date}")
        except PlaywrightTimeoutError as e:
            logger.error(f"Не удалось заполнить поле даты начала: {e}")
            allure.attach(self.page.content(), name="start_date_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(self.page.screenshot(), name="start_date_error.png", attachment_type=allure.attachment_type.PNG)
            raise
        return self

    @allure.step("Заполнение поля 'End Date'")
    def fill_end_date(self, date: str):
        try:
            with allure.step("Ожидание видимости поля 'End Date'"):
                self.wait_for_selector("input[placeholder='End Date']", timeout=30000)
            self.end_date_input.fill(date)
            logger.info(f"Поле 'End Date' заполнено: {date}")
        except PlaywrightTimeoutError as e:
            logger.error(f"Не удалось заполнить поле даты окончания: {e}")
            allure.attach(self.page.content(), name="end_date_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(self.page.screenshot(), name="end_date_error.png", attachment_type=allure.attachment_type.PNG)
            raise
        return self

    @allure.step("Заполнение поля 'Status'")
    def fill_status(self, status: str):
        try:
            with allure.step("Ожидание видимости поля 'Status'"):
                self.wait_for_selector("select.mb-4.block.w-full", timeout=30000)
            self.status_select.select_option(status)
            logger.info(f"Поле 'Status' заполнено: {status}")
        except PlaywrightTimeoutError as e:
            logger.error(f"Не удалось заполнить поле статуса: {e}")
            allure.attach(self.page.content(), name="status_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(self.page.screenshot(), name="status_error.png", attachment_type=allure.attachment_type.PNG)
            raise
        return self

    @allure.step("Отправка формы создания проекта")
    def submit_create_project(self):
        try:
            with allure.step("Ожидание, пока кнопка 'Create' станет активной"):
                self.wait_for_selector("button[type='submit']:not([disabled])", timeout=30000)
            self.create_button.click()
            logger.info("Кликнули на кнопку 'Create' для создания проекта")
        except PlaywrightTimeoutError as e:
            logger.error(f"Не удалось отправить форму: {e}")
            allure.attach(self.page.content(), name="submit_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(self.page.screenshot(), name="submit_error.png", attachment_type=allure.attachment_type.PNG)
            raise
        return self

    @allure.step("Закрытие формы создания проекта")
    def cancel_create_form(self):
        try:
            self.cancel_button.click()
            logger.info("Форма создания проекта закрыта")
            allure.attach(self.page.screenshot(), name="form_closed.png", attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            logger.error(f"Ошибка при закрытии формы: {e}")
            allure.attach(self.page.screenshot(), name="form_close_error.png", attachment_type=allure.attachment_type.PNG)
            raise

    @allure.step("Проверка видимости формы создания")
    def is_create_form_visible(self):
        try:
            return self.project_name_input.is_visible()
        except PlaywrightTimeoutError as e:
            logger.error(f"Не удалось проверить видимость формы: {e}")
            allure.attach(self.page.content(), name="form_visibility_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(self.page.screenshot(), name="form_visibility_error.png", attachment_type=allure.attachment_type.PNG)
            raise

    @allure.step("Проверка видимости проекта")
    def is_project_visible(self, project_name: str):
        try:
            with allure.step(f"Ожидание видимости проекта с названием '{project_name}'"):
                self.wait_for_selector(f"text='{project_name}'", timeout=30000)
            return self.page.locator(f"text='{project_name}'").is_visible()
        except PlaywrightTimeoutError as e:
            logger.error(f"Не удалось проверить видимость проекта: {e}")
            allure.attach(self.page.content(), name="project_visibility_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(self.page.screenshot(), name="project_visibility_error.png", attachment_type=allure.attachment_type.PNG)
            raise

    @allure.step("Проверка активности кнопки создания")
    def is_create_button_enabled(self):
        try:
            return self.create_button.is_enabled()
        except PlaywrightTimeoutError as e:
            logger.error(f"Не удалось проверить кнопку создания: {e}")
            allure.attach(self.page.content(), name="create_button_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(self.page.screenshot(), name="create_button_error.png", attachment_type=allure.attachment_type.PNG)
            raise

    @allure.step("Проверка пустоты поля")
    def is_field_empty(self, field_name: str):
        try:
            field = {
                "project_name": self.project_name_input,
                "description": self.description_input,
                "start_date": self.start_date_input,
                "end_date": self.end_date_input
            }.get(field_name)
            return field.input_value() == ""
        except PlaywrightTimeoutError as e:
            logger.error(f"Не удалось проверить пустоту поля: {e}")
            allure.attach(self.page.content(), name="field_empty_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(self.page.screenshot(), name="field_empty_error.png", attachment_type=allure.attachment_type.PNG)
            raise

    @allure.step("Проверка значения статуса по умолчанию")
    def is_status_default(self):
        try:
            return self.status_select.input_value() == "Not Started"
        except PlaywrightTimeoutError as e:
            logger.error(f"Не удалось проверить статус по умолчанию: {e}")
            allure.attach(self.page.content(), name="status_default_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(self.page.screenshot(), name="status_default_error.png", attachment_type=allure.attachment_type.PNG)
            raise