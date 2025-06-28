# pages/authentication_page.py
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from pages.base_page import BasePage
import allure
from utils.logger import logger
from pages.dashboard_page import DashboardPage
import random
import string

class AuthenticationPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.BASE_URL}/authentication"
        # Селекторы для формы авторизации
        self.email_input = page.locator("input[placeholder='Enter your email']")
        self.password_input = page.locator("input[placeholder='Enter your password']")
        self.submit_button = page.locator("button:has-text('Sign In')")
        self.error_message = page.locator("div.text-red-500:has-text('Invalid credentials'), div.text-red-500:has-text('Account locked'), div.text-red-500:has-text('Please fill in all fields')")
        # Селекторы для формы регистрации
        self.signup_link = page.locator("span.text-primary-600.font-bold.cursor-pointer:has-text('Sign Up')")
        self.signup_header = page.locator("h2.text-2xl.font-semibold.text-center.text-primary-600:has-text('Sign Up')")
        self.signup_name_input = page.locator("input#name")
        self.signup_email_input = page.locator("input#email")
        self.signup_phone_input = page.locator("input#phone")
        self.signup_password_input = page.locator("input#password")
        self.signup_confirm_password_input = page.locator("input#confirmPassword")
        self.signup_submit_button = page.locator("button.w-full:has-text('Sign Up')")
        self.signup_error_message = page.locator("p.text-red-500:has-text('All fields are required'), p.text-red-500:has-text('Passwords do not match')")

    @allure.step("Переход на страницу авторизации")
    def navigate(self, url=None):
        target_url = url if url else self.url
        logger.info(f"Переход на {target_url}")
        try:
            self.navigate_to(target_url)
            if not url:  # Только для /authentication ждём видимости полей
                self.email_input.wait_for(state="visible", timeout=60000)
        except Exception as e:
            logger.error(f"Не удалось перейти на страницу: {e}")
            self.take_screenshot(f"navigation_error_{target_url.split('/')[-1]}.png")
            allure.attach.file(f"navigation_error_{target_url.split('/')[-1]}.png", name="Скриншот ошибки навигации", attachment_type=allure.attachment_type.PNG)
            raise
        return self

    @allure.step("Проверка загрузки страницы авторизации")
    def is_loaded(self):
        current_url = self.page.url.rstrip('/')
        expected_url = self.url.rstrip('/')
        logger.info(f"Проверка загрузки страницы авторизации: текущий URL={current_url}, ожидаемый URL={expected_url}")
        return current_url == expected_url or "/authentication" in current_url

    @allure.step("Ввод email: {email}")
    def fill_email(self, email: str):
        self.email_input.fill(email)
        return self

    @allure.step("Ввод пароля")
    def fill_password(self, password: str):
        self.password_input.fill(password)
        return self

    @allure.step("Отправка формы авторизации")
    def submit_login(self, expect_success=True):
        self.submit_button.click()
        if expect_success:
            try:
                self.page.wait_for_url(f"{self.BASE_URL}/dashboard", timeout=60000)
                return DashboardPage(self.page)
            except PlaywrightTimeoutError as e:
                logger.error(f"Не удалось перейти на дашборд: {e}")
                allure.attach(self.page.content(), name="post_submit_login.html", attachment_type=allure.attachment_type.HTML)
                raise
        else:
            logger.info("Запись содержимого страницы после неудачной попытки входа")
            allure.attach(self.page.content(), name="failed_login_attempt.html", attachment_type=allure.attachment_type.HTML)
        return self

    @allure.step("Авторизация с email {email} и паролем")
    def login(self, email: str, password: str, expect_success=True):
        self.fill_email(email)
        self.fill_password(password)
        return self.submit_login(expect_success=expect_success)

    @allure.step("Открытие формы регистрации")
    def open_signup_form(self):
        self.signup_link.click()
        try:
            self.signup_header.wait_for(state="visible", timeout=10000)
            logger.info("Форма регистрации открыта")
        except PlaywrightTimeoutError as e:
            logger.error(f"Форма регистрации не открыта: {e}")
            allure.attach(self.page.content(), name="signup_form_error.html", attachment_type=allure.attachment_type.HTML)
            raise
        return self

    @allure.step("Ввод имени: {name}")
    def fill_signup_name(self, name: str):
        self.signup_name_input.fill(name)
        return self

    @allure.step("Ввод email для регистрации: {email}")
    def fill_signup_email(self, email: str):
        self.signup_email_input.fill(email)
        return self

    @allure.step("Ввод номера телефона: {phone}")
    def fill_signup_phone(self, phone: str):
        self.signup_phone_input.fill(phone)
        return self

    @allure.step("Ввод пароля для регистрации")
    def fill_signup_password(self, password: str):
        self.signup_password_input.fill(password)
        return self

    @allure.step("Ввод подтверждения пароля")
    def fill_signup_confirm_password(self, password: str):
        self.signup_confirm_password_input.fill(password)
        return self

    @allure.step("Отправка формы регистрации")
    def submit_signup(self, expect_success=True):
        self.signup_submit_button.click()
        if expect_success:
            try:
                self.page.wait_for_url(f"{self.BASE_URL}/dashboard", timeout=60000)
                logger.info("Успешный переход на дашборд после регистрации")
                return DashboardPage(self.page)
            except PlaywrightTimeoutError as e:
                logger.error(f"Не удалось перейти на дашборд: {e}")
                allure.attach(self.page.content(), name="post_submit_signup.html", attachment_type=allure.attachment_type.HTML)
                raise
        else:
            logger.info("Запись содержимого страницы после неудачной попытки регистрации")
            allure.attach(self.page.content(), name="failed_signup_attempt.html", attachment_type=allure.attachment_type.HTML)
        return self

    @allure.step("Регистрация с данными")
    def signup(self, name: str, email: str, phone: str, password: str, confirm_password: str, expect_success=True):
        self.fill_signup_name(name)
        self.fill_signup_email(email)
        self.fill_signup_phone(phone)
        self.fill_signup_password(password)
        self.fill_signup_confirm_password(confirm_password)
        return self.submit_signup(expect_success=expect_success)

    @allure.step("Генерация случайного имени длиной {length} символов")
    def generate_random_name(self, length=12):
        # Генерируем случайное имя из букв, первая буква заглавная
        name = ''.join(random.choices(string.ascii_lowercase, k=length-1))
        name = name.capitalize()
        return name

    @allure.step("Генерация случайного email")
    def generate_random_email(self):
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        return f"{random_string}@mail.ru"

    @allure.step("Генерация случайного номера телефона")
    def generate_random_phone(self):
        random_digits = ''.join(random.choices(string.digits, k=9))
        return f"89{random_digits}"