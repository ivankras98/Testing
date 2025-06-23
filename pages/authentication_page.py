from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from pages.base_page import BasePage
import allure
from utils.logger import logger
from pages.dashboard_page import DashboardPage
from settings import BASE_URL

class AuthenticationPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{BASE_URL}/authentication"
        self.email_input = page.locator("input[placeholder='Enter your email']")
        self.password_input = page.locator("input[placeholder='Enter your password']")
        self.submit_button = page.locator("button:has-text('Sign In')")
        self.error_message = page.locator("div.text-red-500:has-text('Invalid credentials'), div.text-red-500:has-text('Account locked'), div.text-red-500:has-text('Please fill in all fields')")

    @allure.step("Переход на страницу")
    def navigate(self, url=None):
        target_url = url if url else self.url
        logger.info(f"Переход на {target_url}")
        try:
            self.page.goto(target_url, timeout=60000, wait_until="domcontentloaded")
            if not url:  # Только для /authentication ждем видимости полей
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
                self.page.wait_for_url("**/dashboard", timeout=60000)
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

    @allure.step("Переход на указанную страницу")
    def navigate_to(self, url: str):
        logger.info(f"Переход на {url}")
        try:
            self.page.goto(url, timeout=60000, wait_until="domcontentloaded")
        except Exception as e:
            logger.error(f"Не удалось перейти на страницу: {e}")
            self.take_screenshot(f"navigation_error_{url.split('/')[-1]}.png")
            allure.attach.file(f"navigation_error_{url.split('/')[-1]}.png", name="Скриншот ошибки навигации", attachment_type=allure.attachment_type.PNG)
            raise
        return self