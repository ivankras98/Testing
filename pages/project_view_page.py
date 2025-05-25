import allure
import os
from datetime import datetime, timedelta
from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.logger import logger

class ProjectViewPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url_pattern = f"{os.getenv('BASE_URL')}/projects/{{id}}"
        self.add_task_button = page.locator("button.flex.justify-center.items-center.h-5.w-5:has(svg.lucide-plus)")
        self.task_title_input = page.locator("input[placeholder='Task Title']")
        self.task_description_input = page.locator("textarea[placeholder='Task Description']")
        self.status_select = page.locator("select.w-full:has(option[value='To Do'])")
        self.priority_select = page.locator("select.w-full:has(option[value='low'])")
        self.tags_input = page.locator("input[placeholder='Tags (comma separated)']")
        self.start_date_input = page.locator("input[type='date'][placeholder='Start Date']")
        self.due_date_input = page.locator("input[type='date'][placeholder='Due Date']")
        self.story_points_input = page.locator("input[type='number'][placeholder='Story Points']")
        self.create_task_button = page.locator("button[type='submit'].bg-primary-600:has-text('Create New Task')")

    @allure.step("Проверка загрузки страницы проекта")
    def is_loaded(self, project_id):
        logger.info(f"Проверка загрузки страницы проекта с ID {project_id}")
        expected_url = self.url_pattern.format(id=project_id)
        return self.page.url == expected_url

    @allure.step("Открытие формы создания задачи")
    def open_create_task_form(self):
        logger.info("Открытие формы создания задачи")
        self.add_task_button.wait_for(state="visible", timeout=5000)  # Ожидание видимости кнопки
        self.add_task_button.click()
        self.page.wait_for_timeout(500)  # Ждём, чтобы форма открылась
        return self

    @allure.step("Заполнение формы создания задачи")
    def fill_task_form(self, title="Test Task", description="Description for test task", status="To Do", priority="medium", tags="tag1, tag2", story_points=5):
        logger.info("Заполнение формы создания задачи")
        # Сегодняшняя дата (25.05.2025)
        start_date = datetime(2025, 5, 25).strftime("%Y-%m-%d")
        # Дата через неделю (01.06.2025)
        due_date = (datetime(2025, 5, 25) + timedelta(days=7)).strftime("%Y-%m-%d")

        self.task_title_input.fill(title)
        self.task_description_input.fill(description)
        self.status_select.select_option(status)
        self.priority_select.select_option(priority)
        self.tags_input.fill(tags)
        self.start_date_input.fill(start_date)
        self.due_date_input.fill(due_date)
        self.story_points_input.fill(str(story_points))
        return self

    @allure.step("Создание новой задачи")
    def create_task(self):
        logger.info("Создание новой задачи")
        try:
            self.create_task_button.click()
            self.page.wait_for_load_state("networkidle", timeout=60000)
            logger.info("Задача успешно создана")
        except Exception as e:
            logger.error(f"Ошибка при создании задачи: {e}")
            self.take_screenshot("create_task_error.png")
            allure.attach.file("create_task_error.png", name="Скриншот ошибки создания задачи", attachment_type=allure.attachment_type.PNG)
            page_content = self.page.content()
            logger.info(f"Содержимое страницы: {page_content}")
            allure.attach(page_content, name="HTML страницы", attachment_type=allure.attachment_type.HTML)
            raise
        return self