# authentication_page.py
from playwright.sync_api import Page
from pages.base_page import BasePage
import allure
from settings import BASE_URL
import os
from utils.logger import logger

class AuthenticationPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{BASE_URL}/authentication"
        self.email_input = page.locator("#email")
        self.password_input = page.locator("#password")
        self.submit_button = page.locator("button[type='submit']")
        self.error_message = page.locator("text='Invalid credentials'")

    @allure.step("Переход на страницу авторизации с загрузкой URL")
    def navigate(self):
        logger.info(f"Переход на страницу авторизации: {self.url}")
        self.page.goto(self.url, wait_until="networkidle", timeout=120000)
        logger.info(f"Текущий URL после загрузки: {self.page.url}")
        return self

    @allure.step("Проверка состояния выхода и переход на страницу авторизации при необходимости")
    def ensure_logged_out(self):
        if "dashboard" in self.page.url.lower():
            logger.info("Уже авторизованы, выполняем выход...")
            self.page.goto(f"{BASE_URL}/logout", wait_until="networkidle", timeout=120000)
            self.page.goto(self.url, wait_until="networkidle", timeout=120000)
            logger.info(f"URL после выхода: {self.page.url}")

    @allure.step("Заполнение поля email")
    def fill_email(self, email: str):
        with allure.step("Ожидание видимости поля email"):
            self.wait_for_selector("#email", timeout=120000)
        self.email_input.fill(email)
        logger.info(f"Поле email заполнено: {email}")

    @allure.step("Заполнение поля пароля")
    def fill_password(self, password: str):
        with allure.step("Ожидание видимости поля пароля"):
            self.wait_for_selector("#password", timeout=120000)
        self.password_input.fill(password)
        logger.info(f"Поле пароля заполнено: {password}")

    @allure.step("Нажатие кнопки входа")
    def submit_login(self):
        api_url = os.getenv("API_URL", f"{BASE_URL}")  # По умолчанию используем BASE_URL, если API_URL не задан
        expected_login_url = f"{api_url}/api/auth/login"
        with allure.step(f"Ожидание ответа API от {expected_login_url}"):
            with self.page.expect_response(lambda response: response.url == expected_login_url, timeout=10000) as response_info:
                self.submit_button.click()
        response = response_info.value
        logger.info(f"Сетевой запрос: {response.url}, статус: {response.status}")
        with allure.step("Ожидание редиректа на страницу /dashboard"):
            self.page.wait_for_url(f"{BASE_URL}/dashboard", wait_until="networkidle", timeout=120000)
            logger.info(f"URL после входа: {self.page.url}")
        if self.error_message.is_visible():
            self.take_screenshot("login_error.png")
            allure.attach.file("login_error.png", name="Скриншот ошибки входа", attachment_type=allure.attachment_type.PNG)
            raise AssertionError("Вход не удался: отображено сообщение 'Invalid credentials'")
        logger.info("Вход прошёл успешно")
        from pages.dashboard_page import DashboardPage
        return DashboardPage(self.page)

    def login(self, email: str, password: str):
        with allure.step("Выполнение полного процесса входа"):
            self.navigate()
            self.ensure_logged_out()
            self.fill_email(email)
            self.fill_password(password)
            return self.submit_login()

    @allure.step("Проверка загрузки страницы авторизации")
    def is_loaded(self):
        logger.info("Проверка загрузки страницы авторизации")
        return self.email_input.is_visible()