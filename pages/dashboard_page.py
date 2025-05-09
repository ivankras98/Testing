# dashboard_page.py
from playwright.sync_api import Page
from pages.base_page import BasePage
import allure
from settings import BASE_URL
from utils.logger import logger

class DashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{BASE_URL}/dashboard"
        self.profile_selector = page.locator("div.relative:has(svg.lucide-chevron-down)")
        self.logout_option = page.locator("text=Logout")

    @allure.step("Проверка загрузки страницы дашборда по URL")
    def is_loaded(self):
        logger.info("Проверка загрузки страницы дашборда")
        return self.page.url == self.url

    @allure.step("Выполнение выхода из системы через меню профиля")
    def logout(self):
        from pages.authentication_page import AuthenticationPage
        with allure.step("Ожидать видимости элемента профиля с селектором 'div.relative:has(svg.lucide-chevron-down)'"):
            try:
                self.wait_for_selector("div.relative:has(svg.lucide-chevron-down)", timeout=60000)
            except Exception as e:
                logger.error(f"Ошибка ожидания элемента профиля (стрелки): {e}")
                self.take_screenshot("logout_profile_error.png")
                allure.attach.file("logout_profile_error.png", name="Скриншот ошибки выхода (профиль)", attachment_type=allure.attachment_type.PNG)
                raise
        with allure.step("Кликнуть на элемент профиля для открытия меню"):
            self.profile_selector.click()
            logger.info("Кликнули на стрелку для открытия выпадающего меню")
            self.page.wait_for_timeout(500)
        with allure.step("Ожидать видимости кнопки 'Logout'"):
            try:
                self.wait_for_selector("text=Logout", timeout=5000)
            except Exception as e:
                logger.error(f"Ошибка ожидания кнопки 'Logout': {e}")
                self.take_screenshot("logout_error.png")
                allure.attach.file("logout_error.png", name="Скриншот ошибки выхода", attachment_type=allure.attachment_type.PNG)
                raise
        with allure.step("Нажать кнопку 'Logout' для выхода"):
            self.logout_option.click()
            logger.info("Кликнули на кнопку 'Logout'")
        with allure.step("Ожидать редирект на страницу авторизации по URL"):
            self.page.wait_for_url(f"{BASE_URL}/authentication", wait_until="networkidle", timeout=60000)
            logger.info(f"URL после выхода: {self.page.url}")
            logger.info("Выход прошёл успешно")
        return AuthenticationPage(self.page)