from pages.base_page import BasePage
import allure
from utils.logger import logger

class TasksPage(BasePage):

    @allure.step("Проверка загрузки страницы задач")
    def is_loaded(self):
        logger.info("Проверяем, что страница задач успешно загрузилась")
        # Например, проверим наличие уникального элемента на странице задач
        return self.page.locator("h1, h2, p").filter(has_text="Tasks").is_visible()
