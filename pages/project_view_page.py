import allure
from playwright.sync_api import Page
from pages.base_page import BasePage
from settings import BASE_URL
from utils.logger import logger

class ProjectViewPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.base_url = BASE_URL

    @allure.step("Переход на страницу проекта")
    def navigate_to_project(self, project_id: str):
        logger.info(f"Переход на проект с ID: {project_id}")
        try:
            project_url = f"{self.base_url}/projects/{project_id}"
            self.navigate_to(project_url)
        except Exception as e:
            logger.error(f"Не удалось перейти на страницу проекта: {e}")
            allure.attach(self.page.content(), name="navigation_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(self.page.screenshot(), name="navigation_error.png", attachment_type=allure.attachment_type.PNG)
            raise