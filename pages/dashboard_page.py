# pages/dashboard_page.py
from playwright.sync_api import Page
from pages.base_page import BasePage
import allure
from utils.logger import logger
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

class DashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.BASE_URL}/dashboard"
        self.plus_button = page.locator("button:has(svg.lucide.lucide-plus)")
        self.project_list = page.locator(".relative.flex.items-center.w-full")
        self.profile_selector = page.locator("div.relative:has(svg.lucide-chevron-down), button[role='button']:has-text('Profile')")
        self.logout_option = page.locator("text=Logout")

    @allure.step("Открытие формы создания проекта")
    def click_plus_button(self):
        logger.info("Ожидание видимости кнопки плюс")
        plus_button_selector = "button:has(svg.lucide.lucide-plus)"
        try:
            self.wait_for_selector(plus_button_selector, timeout=30000)
            self.plus_button.click()
            logger.info("Клик по кнопке плюс выполнен")
        except PlaywrightTimeoutError as e:
            logger.error(f"Кнопка плюс не найдена: {e}")
            allure.attach(self.page.content(), name="plus_button_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(self.page.screenshot(), name="plus_button_error.png", attachment_type=allure.attachment_type.PNG)
            raise
        logger.info("Ожидание формы создания проекта")
        form_selector = "form.mt-6.flex.flex-col.gap-4"
        try:
            self.wait_for_selector(form_selector, timeout=30000)
            logger.info("Форма создания проекта загружена")
        except PlaywrightTimeoutError as e:
            logger.error(f"Форма не найдена: {e}")
            allure.attach(self.page.content(), name="form_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(self.page.screenshot(), name="form_error.png", attachment_type=allure.attachment_type.PNG)
            raise
        return self

    @allure.step("Удаление первого проекта в списке")
    def delete_first_project(self):
        logger.info("Удаление первого проекта")
        try:
            self.page.locator('div.flex.items-center.w-full >> svg.lucide-ellipsis').first.click()
            self.page.locator('p.text-red-500:text("Delete")').click()
            logger.info("Первый проект удалён")
            return self.page.locator(".relative.flex.items-center.w-full").first.text_content()
        except PlaywrightTimeoutError as e:
            logger.error(f"Не удалось удалить проект: {e}")
            allure.attach(self.page.content(), name="delete_project_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(self.page.screenshot(), name="delete_project_error.png", attachment_type=allure.attachment_type.PNG)
            raise

    @allure.step("Открытие проекта по названию")
    def open_project(self, project_name: str):
        logger.info(f"Открытие проекта: {project_name}")
        try:
            project_selector = f"text={project_name}"
            self.wait_for_selector(project_selector, timeout=30000)
            self.page.locator(project_selector).click()
            logger.info(f"Клик по проекту: {project_name}")
        except PlaywrightTimeoutError as e:
            logger.error(f"Не удалось открыть проект: {e}")
            allure.attach(self.page.content(), name="open_project_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(self.page.screenshot(), name="open_project_error.png", attachment_type=allure.attachment_type.PNG)
            raise
        return self

    @allure.step("Переход в раздел сообщений")
    def go_to_messages(self):
        logger.info("Переход в раздел сообщений")
        try:
            self.navigate_to(f"{self.BASE_URL}/messages")
            self.page.wait_for_url(f"{self.BASE_URL}/messages", timeout=30000)
            logger.info("Раздел сообщений загружен")
        except PlaywrightTimeoutError as e:
            logger.error(f"Не удалось перейти в раздел сообщений: {e}")
            allure.attach(self.page.content(), name="messages_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(self.page.screenshot(), name="messages_error.png", attachment_type=allure.attachment_type.PNG)
            raise
        return self

    @allure.step("Переход в раздел участников")
    def go_to_members(self):
        logger.info("Переход в раздел участников")
        try:
            self.navigate_to(f"{self.BASE_URL}/members")
            self.page.wait_for_url(f"{self.BASE_URL}/members", timeout=30000)
            logger.info("Раздел участников загружен")
        except PlaywrightTimeoutError as e:
            logger.error(f"Не удалось перейти в раздел участников: {e}")
            allure.attach(self.page.content(), name="members_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(self.page.screenshot(), name="members_error.png", attachment_type=allure.attachment_type.PNG)
            raise
        return self

    @allure.step("Переход в раздел задач")
    def go_to_tasks(self):
        logger.info("Переход в раздел задач")
        try:
            self.navigate_to(f"{self.BASE_URL}/tasks")
            self.page.wait_for_url(f"{self.BASE_URL}/tasks", timeout=30000)
            logger.info("Раздел задач загружен")
        except PlaywrightTimeoutError as e:
            logger.error(f"Не удалось перейти в раздел задач: {e}")
            allure.attach(self.page.content(), name="tasks_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(self.page.screenshot(), name="tasks_error.png", attachment_type=allure.attachment_type.PNG)
            raise
        return self

    @allure.step("Проверка загрузки дашборда")
    def is_loaded(self):
        logger.info("Проверка загрузки дашборда")
        try:
            self.page.wait_for_url(f"{self.BASE_URL}/dashboard", timeout=30000)
            return self.page.url == f"{self.BASE_URL}/dashboard"
        except PlaywrightTimeoutError as e:
            logger.error(f"Дашборд не загружен: {e}")
            allure.attach(self.page.content(), name="dashboard_load_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(self.page.screenshot(), name="dashboard_load_error.png", attachment_type=allure.attachment_type.PNG)
            raise

    @allure.step("Выполнение выхода из системы")
    def logout(self):
        try:
            logger.info("Ожидание видимости селектора профиля")
            self.profile_selector.wait_for(state="visible", timeout=10000)
            logger.info("Клик по селектору профиля")
            self.profile_selector.click()
            logger.info("Ожидание видимости опции выхода")
            self.logout_option.wait_for(state="visible", timeout=10000)
            logger.info("Клик по опции выхода")
            self.logout_option.click()
            logger.info("Ожидание страницы авторизации")
            self.page.wait_for_url(f"{self.BASE_URL}/authentication", timeout=30000)
        except PlaywrightTimeoutError as e:
            logger.error(f"Выход не удался: {e}")
            allure.attach(self.page.content(), name="logout_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(self.page.screenshot(), name="logout_error.png", attachment_type=allure.attachment_type.PNG)
            raise
        from pages.authentication_page import AuthenticationPage
        logger.info(f"Перенаправлено на: {self.page.url}")
        return AuthenticationPage(self.page)