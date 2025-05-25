import allure
import os
from playwright.sync_api import Page
from pages.base_page import BasePage
from pages.authentication_page import AuthenticationPage
from pages.messages_page import MessagesPage
from pages.settings_page import SettingsPage
from pages.tasks_page import TasksPage
from pages.members_page import MembersPage
from pages.project_view_page import ProjectViewPage
from utils.logger import logger

class DashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{os.getenv('BASE_URL')}/dashboard"
        self.profile_selector = page.locator("div.relative:has(svg.lucide-chevron-down)")
        self.logout_option = page.locator("text=Logout")
        self.messages_button = page.locator('a[href="/messages"]')
        self.settings_button = page.locator('a[href="/settings"]')
        self.menu_toggle = page.locator("div.text-gray-500:has(svg.lucide-chevrons-right)")  # Селектор для стрелочки
        self.project_items = page.locator("a[href^='/projects/']")  # Селектор для списка проектов
        self.ellipsis_button = page.locator("svg.lucide-ellipsis.text-primary-600")  # Селектор для троеточия
        self.delete_option = page.locator("p.text-red-500:has-text('Delete')")  # Селектор для кнопки Delete
        self.context_menu = page.locator("div.z-50")

    @allure.step("Проверка загрузки страницы дашборда")
    def is_loaded(self):
        logger.info("Проверка загрузки страницы дашборда")
        return self.page.url == self.url

    @allure.step("Переход в раздел сообщений")
    def go_to_messages(self):
        logger.info("Нажатие на кнопку перехода в раздел сообщений")
        with self.page.expect_navigation(url=f"{os.getenv('BASE_URL')}/messages", timeout=60000):
            self.messages_button.click()
        return MessagesPage(self.page)

    @allure.step("Переход в раздел настроек")
    def go_to_settings(self):
        logger.info("Нажатие на кнопку перехода в раздел настроек")
        with self.page.expect_navigation(url=f"{os.getenv('BASE_URL')}/settings", timeout=60000):
            self.settings_button.click()
        return SettingsPage(self.page)

    @allure.step("Переход в раздел задач")
    def go_to_tasks(self):
        logger.info("Нажатие на кнопку перехода в раздел задач")
        self.tasks_button = self.page.locator("a[href='/tasks']")
        with self.page.expect_navigation(url=f"{os.getenv('BASE_URL')}/tasks", timeout=60000):
            self.tasks_button.click()
        return TasksPage(self.page)

    @allure.step("Переход в раздел участников")
    def go_to_members(self):
        logger.info("Нажатие на кнопку перехода в раздел участников")
        self.members_button = self.page.locator("a[href='/members']")
        with self.page.expect_navigation(url=f"{os.getenv('BASE_URL')}/members", timeout=60000):
            self.members_button.click()
        return MembersPage(self.page)


    @allure.step("Открытие бокового меню")
    def open_side_menu(self):
        logger.info("Открытие бокового меню")
        self.menu_toggle.click()
        self.page.wait_for_timeout(500)  # Ждём, чтобы меню открылось
        return self


    @allure.step("Открытие второго проекта")
    def open_second_project(self):
        logger.info("Открытие второго проекта")
        # Открываем боковое меню
        self.open_side_menu()

        # Находим второй проект в списке (индекс 1, так как нумерация начинается с 0)
        second_project = self.project_items.nth(1)
        project_name = second_project.locator("p.text-sm.font-medium").text_content().strip()
        logger.info(f"Выбран второй проект для открытия: {project_name}")

        # Нажимаем на троеточие рядом с вторым проектом
        ellipsis = second_project.locator("svg.lucide-ellipsis.text-gray-500")
        ellipsis.click()

        # Ждём появления контекстного меню
        try:
            self.context_menu.wait_for(state="visible", timeout=10000)
            open_button = self.context_menu.locator("p.text-sm:has-text('Open')")
            open_button.wait_for(state="visible", timeout=5000)
            open_button.click()
            logger.info(f"Нажата кнопка Open для проекта {project_name}")
            project_url = second_project.get_attribute("href")
            self.page.wait_for_url(f"{os.getenv('BASE_URL')}{project_url}", wait_until="networkidle", timeout=60000)
        except Exception as e:
            logger.error(f"Ошибка при открытии контекстного меню или нажатии на Open: {e}")
            self.take_screenshot("open_project_error.png")
            allure.attach.file("open_project_error.png", name="Скриншот ошибки открытия проекта", attachment_type=allure.attachment_type.PNG)
            page_content = self.page.content()
            logger.info(f"Содержимое страницы: {page_content}")
            allure.attach(page_content, name="HTML страницы", attachment_type=allure.attachment_type.HTML)
            raise

        logger.info(f"Проект {project_name} открыт, URL: {self.page.url}")
        return project_url




    @allure.step("Открытие третьего проекта")
    def open_third_project(self):
        logger.info("Открытие третьего проекта")
        # Открываем боковое меню
        self.open_side_menu()

        # Проверяем, что в списке достаточно проектов
        project_count = self.project_items.count()
        logger.info(f"Количество проектов в списке: {project_count}")
        assert project_count >= 3, "В списке должно быть как минимум 3 проекта для открытия третьего"

        # Находим третий проект в списке (индекс 2, так как нумерация начинается с 0)
        third_project = self.project_items.nth(2)
        project_name = third_project.locator("p.text-sm.font-medium").text_content().strip()
        logger.info(f"Выбран третий проект для открытия: {project_name}")

        # Нажимаем на троеточие рядом с третьим проектом
        ellipsis = third_project.locator("svg.lucide-ellipsis.text-gray-500")
        ellipsis.click()

        # Ждём появления контекстного меню
        try:
            self.context_menu.wait_for(state="visible", timeout=10000)
            open_button = self.context_menu.locator("p.text-sm:has-text('Open')")
            open_button.wait_for(state="visible", timeout=5000)
            open_button.click()
            logger.info(f"Нажата кнопка Open для проекта {project_name}")
            project_url = third_project.get_attribute("href")
            project_id = project_url.split("/")[-1]
            self.page.wait_for_url(f"{os.getenv('BASE_URL')}{project_url}", wait_until="networkidle", timeout=60000)
        except Exception as e:
            logger.error(f"Ошибка при открытии контекстного меню или нажатии на Open: {e}")
            self.take_screenshot("open_project_error.png")
            allure.attach.file("open_project_error.png", name="Скриншот ошибки открытия проекта", attachment_type=allure.attachment_type.PNG)
            page_content = self.page.content()
            logger.info(f"Содержимое страницы: {page_content}")
            allure.attach(page_content, name="HTML страницы", attachment_type=allure.attachment_type.HTML)
            raise

        logger.info(f"Проект {project_name} открыт, URL: {self.page.url}")
        return ProjectViewPage(self.page), project_id






    @allure.step("Удаление первого проекта")
    def delete_first_project(self):
        logger.info("Удаление первого проекта")
        # Открываем боковое меню
        self.open_side_menu()

        # Находим первый проект в списке
        first_project = self.project_items.first
        project_name = first_project.locator("p.text-sm.font-medium").text_content().strip()
        logger.info(f"Выбран проект для удаления: {project_name}")

        # Нажимаем на троеточие рядом с первым проектом
        ellipsis = first_project.locator("svg.lucide-ellipsis.text-gray-500")
        ellipsis.click()

        # Ждём появления контекстного меню
        try:
            self.context_menu.wait_for(state="visible", timeout=10000)
            delete_button = self.context_menu.locator("p.text-red-500:has-text('Delete')")
            delete_button.wait_for(state="visible", timeout=5000)
            delete_button.click()
            logger.info(f"Нажата кнопка Delete для проекта {project_name}")
        except Exception as e:
            logger.error(f"Ошибка при открытии контекстного меню или нажатии на Delete: {e}")
            self.take_screenshot("delete_error.png")
            allure.attach.file("delete_error.png", name="Скриншот ошибки удаления", attachment_type=allure.attachment_type.PNG)
            page_content = self.page.content()
            logger.info(f"Содержимое страницы: {page_content}")
            allure.attach(page_content, name="HTML страницы", attachment_type=allure.attachment_type.HTML)
            raise

        # Ждём обновления списка проектов
        self.page.wait_for_timeout(1000)
        logger.info(f"Проект {project_name} удалён")
        return self


    @allure.step("Выполнение выхода из системы")
    def logout(self):
        with allure.step("Ожидание видимости элемента профиля"):
            try:
                self.wait_for_selector("div.relative:has(svg.lucide-chevron-down)", timeout=120000)
            except Exception as e:
                logger.error(f"Ошибка ожидания элемента профиля (стрелки): {e}")
                self.take_screenshot("logout_profile_error.png")
                allure.attach.file("logout_profile_error.png", name="Скриншот ошибки выхода (профиль)", attachment_type=allure.attachment_type.PNG)
                raise
        with allure.step("Кликнуть на элемент профиля для открытия меню"):
            self.profile_selector.click()
            logger.info("Кликнули на стрелку для открытия выпадающего меню")
            self.page.wait_for_timeout(500)
        with allure.step("Ожидание видимости кнопки 'Logout'"):
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
        with allure.step("Ожидать редирект на страницу авторизации"):
            self.page.wait_for_url(f"{os.getenv('BASE_URL')}/authentication", wait_until="networkidle", timeout=120000)
            logger.info(f"URL после выхода: {self.page.url}")
            logger.info("Выход прошёл успешно")
        return AuthenticationPage(self.page)