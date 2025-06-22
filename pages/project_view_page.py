import allure
from playwright.sync_api import Page
from utils.logger import logger

class ProjectViewPage:
    def __init__(self, page: Page):
        self.page = page
        self.base_url = "http://localhost:3000"  # Измените, если BASE_URL определен в другом месте

    @allure.step("Переход на страницу проекта")
    def navigate_to_project(self, project_id: str):
        logger.info(f"Navigating to project with ID: {project_id}")
        try:
            project_url = f"{self.base_url}/projects/{project_id}"
            self.navigate_to(project_url)
        except Exception as e:
            logger.error(f"Failed to navigate to project page: {e}")
            raise

    @allure.step("Навигатор на URL")
    def navigate_to(self, url: str):
        logger.info(f"Navigating to {url}")
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")  # Убедитесь, что страница полностью загружена