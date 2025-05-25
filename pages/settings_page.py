from pages.base_page import BasePage
import allure
from utils.logger import logger

class SettingsPage(BasePage):

    @allure.step("Проверка загрузки страницы настроек и отображения ошибки 404")
    def is_error_404_displayed(self):
        logger.info("Ожидаем появление ошибки 404 на странице настроек")
        try:
            # Ждем появления h1 с текстом "404" (до 10 секунд)
            self.page.wait_for_selector("h1.next-error-h1", timeout=10000)
            error_h1 = self.page.locator("h1.next-error-h1", has_text="404")
            error_h2 = self.page.locator("h2", has_text="This page could not be found.")
            # Проверяем, видны ли оба элемента
            result = error_h1.is_visible() and error_h2.is_visible()
            logger.info(f"Результат проверки 404: {result}")
            return result
        except Exception as e:
            logger.error(f"Ошибка при ожидании элементов 404: {e}")
            return False
