from playwright.sync_api import Page
from pages.base_page import BasePage
import allure
from settings import BASE_URL
from utils.logger import logger
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


class DashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{BASE_URL}/dashboard"
        self.plus_button = page.locator("button:has(svg.lucide.lucide-plus)")
        self.project_list = page.locator(".relative.flex.items-center.w-full")
        self.profile_selector = page.locator("div.relative:has(svg.lucide-chevron-down), button[role='button']:has-text('Profile')")
        self.logout_option = page.locator("text=Logout")

    @allure.step("Открытие формы создания проекта")
    def click_plus_button(self):
        logger.info("Waiting for plus button visibility")
        plus_button_selector = "button:has(svg.lucide.lucide-plus)"
        try:
            self.page.wait_for_selector(plus_button_selector, state="visible", timeout=30000)
            self.plus_button = self.page.locator(plus_button_selector)
            logger.info(f"Plus button visible: {self.plus_button.is_visible()}")
            self.plus_button.click()
        except PlaywrightTimeoutError as e:
            logger.error(f"Plus button not found: {e}")
            allure.attach(self.page.content(), name="plus_button_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(self.page.screenshot(), name="plus_button_error.png", attachment_type=allure.attachment_type.PNG)
            raise
        logger.info("Waiting for create project form")
        form_selector = "form.mt-6.flex.flex-col.gap-4"
        try:
            self.page.wait_for_selector(form_selector, state="visible", timeout=30000)
            logger.info("Create project form loaded")
        except PlaywrightTimeoutError as e:
            logger.error(f"Form not found: {e}")
            allure.attach(self.page.content(), name="form_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(self.page.screenshot(), name="form_error.png", attachment_type=allure.attachment_type.PNG)
            raise
        return self

    @allure.step("Удаление первого проекта в списке")
    def delete_first_project(self):
    	self.page.locator('div.cursor-pointer:has(svg.lucide-chevrons-right)').click()
    	self.page.locator('div.flex.items-center.w-full >> svg.lucide-ellipsis').first.click()
    	self.page.locator('p.text-red-500:text("Delete")').click()

    @allure.step("Открытие проекта по названию")
    def open_project(self, project_name: str):
        logger.info(f"Opening project: {project_name}")
        try:
            project_selector = f"text={project_name}"
            self.page.wait_for_selector(project_selector, state="visible", timeout=30000)
            self.page.locator(project_selector).click()
            logger.info(f"Clicked on project: {project_name}")
        except PlaywrightTimeoutError as e:
            logger.error(f"Failed to open project: {e}")
            allure.attach(self.page.content(), name="open_project_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(self.page.screenshot(), name="open_project_error.png", attachment_type=allure.attachment_type.PNG)
            raise
        return self

    @allure.step("Переход в раздел сообщений")
    def go_to_messages(self):
        logger.info("Navigating to messages section")
        try:
            self.navigate_to(f"{BASE_URL}/messages")
            self.page.wait_for_url(f"{BASE_URL}/messages", timeout=30000)
            logger.info("Messages section loaded")
        except PlaywrightTimeoutError as e:
            logger.error(f"Failed to navigate to messages: {e}")
            allure.attach(self.page.content(), name="messages_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(self.page.screenshot(), name="messages_error.png", attachment_type=allure.attachment_type.PNG)
            raise
        return self

    @allure.step("Переход в раздел участников")
    def go_to_members(self):
        logger.info("Navigating to members section")
        try:
            self.navigate_to(f"{BASE_URL}/members")
            self.page.wait_for_url(f"{BASE_URL}/members", timeout=30000)
            logger.info("Members section loaded")
        except PlaywrightTimeoutError as e:
            logger.error(f"Failed to navigate to members: {e}")
            allure.attach(self.page.content(), name="members_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(self.page.screenshot(), name="members_error.png", attachment_type=allure.attachment_type.PNG)
            raise
        return self

    @allure.step("Переход в раздел задач")
    def go_to_tasks(self):
        logger.info("Navigating to tasks section")
        try:
            self.navigate_to(f"{BASE_URL}/tasks")
            self.page.wait_for_url(f"{BASE_URL}/tasks", timeout=30000)
            logger.info("Tasks section loaded")
        except PlaywrightTimeoutError as e:
            logger.error(f"Failed to navigate to tasks: {e}")
            allure.attach(self.page.content(), name="tasks_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(self.page.screenshot(), name="tasks_error.png", attachment_type=allure.attachment_type.PNG)
            raise
        return self

    @allure.step("Проверка загрузки дашборда")
    def is_loaded(self):
        logger.info("Checking if dashboard is loaded")
        try:
            self.page.wait_for_url(f"{BASE_URL}/dashboard", timeout=30000)
            return self.page.url == f"{BASE_URL}/dashboard"
        except PlaywrightTimeoutError as e:
            logger.error(f"Dashboard not loaded: {e}")
            allure.attach(self.page.content(), name="dashboard_load_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(self.page.screenshot(), name="dashboard_load_error.png", attachment_type=allure.attachment_type.PNG)
            raise

    @allure.step("Выполнение выхода из системы")
    def logout(self):
        try:
            logger.info("Checking profile selector visibility")
            self.profile_selector.wait_for(state="visible", timeout=10000)
            logger.info("Clicking profile selector")
            self.profile_selector.click()
            logger.info("Checking logout option visibility")
            self.logout_option.wait_for(state="visible", timeout=10000)
            logger.info("Clicking logout option")
            self.logout_option.click()
            logger.info("Waiting for authentication page")
            self.page.wait_for_url("**/authentication", timeout=30000)  # Увеличен таймаут
        except PlaywrightTimeoutError as e:
            logger.error(f"Logout failed: {e}")
            allure.attach(self.page.content(), name="logout_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(self.page.screenshot(), name="logout_error.png", attachment_type=allure.attachment_type.PNG)
            raise
        from pages.authentication_page import AuthenticationPage
        logger.info(f"Redirected to: {self.page.url}")
        return AuthenticationPage(self.page)