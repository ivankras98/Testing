# tests/test_tasks.py
import pytest
import allure
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from pages.authentication_page import AuthenticationPage
from pages.project_view_page import ProjectViewPage
from pages.dashboard_page import DashboardPage
from utils.logger import logger
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture(scope="function")
def project_page(authenticated_context):
    page = authenticated_context.new_page()
    project_view_page = ProjectViewPage(page)
    yield project_view_page
    page.close()

@pytest.mark.tasks
@allure.title("Переход на страницу задач")
def test_navigate_to_tasks(project_page: ProjectViewPage):
    with allure.step("Переход на страницу задач"):
        project_page.navigate_to(f"{project_page.BASE_URL}/tasks")
        allure.attach(project_page.page.screenshot(), name="tasks_page_loaded.png", attachment_type=allure.attachment_type.PNG)
    with allure.step("Проверка изменения URL"):
        project_page.page.wait_for_url(f"{project_page.BASE_URL}/tasks", timeout=30000)
        assert project_page.page.url == f"{project_page.BASE_URL}/tasks", "Не удалось перейти на страницу задач"
        logger.info("Успешно перешёл на страницу задач")
        allure.attach(project_page.page.screenshot(), name="tasks_page_confirmed.png", attachment_type=allure.attachment_type.PNG)

@pytest.mark.tasks
@allure.title("Переход на страницу проекта и открытие формы создания задачи")
def test_navigate_to_specific_project(project_page: ProjectViewPage):
    project_url = f"{project_page.BASE_URL}/projects/193"
    with allure.step("Переход на страницу проекта"):
        project_page.navigate_to(project_url)
        try:
            project_page.page.wait_for_url(project_url, timeout=30000)
            assert project_page.page.url == project_url, f"Не удалось перейти на страницу проекта, текущий URL: {project_page.page.url}"
            logger.info(f"Перешёл на страницу проекта: {project_url}")
            allure.attach(project_page.page.screenshot(), name="project_page_loaded.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Не удалось перейти на страницу проекта: {e}")
            allure.attach(project_page.page.content(), name="project_nav_error.html", attachment_type=allure.attachment_type.HTML)
            raise
    with allure.step("Проверка видимости колонки To Do"):
        try:
            todo_column = project_page.page.locator("div.border-green-400")
            todo_column.wait_for(state="visible", timeout=10000)
            logger.info("Колонка To Do видна")
            allure.attach(project_page.page.screenshot(), name="todo_column_visible.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Колонка To Do не видна: {e}")
            allure.attach(project_page.page.content(), name="todo_column_error.html", attachment_type=allure.attachment_type.HTML)
            raise
    with allure.step("Клик по кнопке 'плюс' в колонке To Do"):
        try:
            plus_button = project_page.page.locator("div.border-green-400 button:has(svg.lucide-plus)")
            plus_button.wait_for(state="visible", timeout=10000)
            plus_button.click()
            logger.info("Кликнул по кнопке 'плюс' в колонке To Do")
            allure.attach(project_page.page.screenshot(), name="plus_button_clicked.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Не удалось кликнуть по кнопке 'плюс': {e}")
            allure.attach(project_page.page.content(), name="plus_button_error.html", attachment_type=allure.attachment_type.HTML)
            raise
    with allure.step("Проверка открытия формы создания задачи"):
        try:
            task_form_title = project_page.page.locator("h1:has-text('Create new Task')")
            task_form_title.wait_for(state="visible", timeout=15000)
            assert task_form_title.is_visible(), "Форма создания задачи не открылась"
            logger.info("Форма создания задачи успешно открыта")
            allure.attach(project_page.page.screenshot(), name="task_form_opened.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Заголовок формы 'Create new Task' не виден: {e}")
            allure.attach(project_page.page.content(), name="task_form_error.html", attachment_type=allure.attachment_type.HTML)
            raise

@pytest.mark.tasks
@allure.title("Заполнение и отправка формы создания задачи")
def test_create_task_in_todo(project_page: ProjectViewPage):
    project_url = f"{project_page.BASE_URL}/projects/193"
    with allure.step("Переход на страницу проекта"):
        project_page.navigate_to(project_url)
        try:
            project_page.page.wait_for_url(project_url, timeout=30000)
            assert project_page.page.url == project_url, f"Не удалось перейти на страницу проекта, текущий URL: {project_page.page.url}"
            logger.info(f"Перешёл на страницу проекта: {project_url}")
            allure.attach(project_page.page.screenshot(), name="project_page_loaded.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Не удалось перейти на страницу проекта: {e}")
            allure.attach(project_page.page.content(), name="project_nav_error.html", attachment_type=allure.attachment_type.HTML)
            raise
    with allure.step("Проверка видимости колонки To Do"):
        try:
            todo_column = project_page.page.locator("div.border-green-400")
            todo_column.wait_for(state="visible", timeout=10000)
            logger.info("Колонка To Do видна")
            allure.attach(project_page.page.screenshot(), name="todo_column_visible.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Колонка To Do не видна: {e}")
            allure.attach(project_page.page.content(), name="todo_column_error.html", attachment_type=allure.attachment_type.HTML)
            raise
    with allure.step("Клик по кнопке 'плюс' в колонке To Do"):
        try:
            plus_button = project_page.page.locator("div.border-green-400 button:has(svg.lucide-plus)")
            plus_button.wait_for(state="visible", timeout=10000)
            plus_button.click()
            logger.info("Кликнул по кнопке 'плюс' в колонке To Do")
            allure.attach(project_page.page.screenshot(), name="plus_button_clicked.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Не удалось кликнуть по кнопке 'плюс': {e}")
            allure.attach(project_page.page.content(), name="plus_button_error.html", attachment_type=allure.attachment_type.HTML)
            raise
    with allure.step("Проверка открытия формы создания задачи"):
        try:
            task_form_title = project_page.page.locator("h1:has-text('Create new Task')")
            task_form_title.wait_for(state="visible", timeout=15000)
            assert task_form_title.is_visible(), "Форма создания задачи не открылась"
            logger.info("Форма создания задачи успешно открыта")
            allure.attach(project_page.page.screenshot(), name="task_form_opened.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Заголовок формы 'Create new Task' не виден: {e}")
            allure.attach(project_page.page.content(), name="task_form_error.html", attachment_type=allure.attachment_type.HTML)
            raise
    with allure.step("Заполнение формы создания задачи"):
        try:
            page = project_page.page
            page.locator("input[placeholder='Task Title']").fill("Test Task")
            logger.info("Заполнено название задачи: Test Task")
            page.locator("textarea[placeholder='Task Description']").fill("This is a test task description")
            logger.info("Заполнено описание задачи")
            page.locator("input[placeholder='Tags (comma separated)']").fill("test, automation")
            logger.info("Заполнены теги: test, automation")
            page.locator("input[placeholder='Start Date']").fill("2025-06-23")
            logger.info("Заполнена дата начала: 2025-06-23")
            page.locator("input[placeholder='Due Date']").fill("2025-06-30")
            logger.info("Заполнена дата окончания: 2025-06-30")
            page.locator("input[placeholder='Story Points']").fill("5")
            logger.info("Заполнены Story Points: 5")
            allure.attach(page.screenshot(), name="task_form_filled.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Не удалось заполнить форму задачи: {e}")
            allure.attach(page.content(), name="task_form_fill_error.html", attachment_type=allure.attachment_type.HTML)
            raise
    with allure.step("Отправка формы"):
        try:
            submit_button = page.locator("button[type='submit']:has-text('Create New Task')")
            submit_button.wait_for(state="visible", timeout=10000)
            submit_button.click()
            logger.info("Кликнул по кнопке 'Create New Task'")
            allure.attach(page.screenshot(), name="task_form_submitted.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Не удалось отправить форму задачи: {e}")
            allure.attach(page.content(), name="task_form_submit_error.html", attachment_type=allure.attachment_type.HTML)
            raise

@pytest.mark.tasks
@allure.title("Заполнение и отправка формы с названием задачи на 100 символов")
def test_create_task_with_100_char_title(project_page: ProjectViewPage):
    project_url = f"{project_page.BASE_URL}/projects/193"
    with allure.step("Переход на страницу проекта"):
        project_page.navigate_to(project_url)
        try:
            project_page.page.wait_for_url(project_url, timeout=30000)
            assert project_page.page.url == project_url, f"Не удалось перейти на страницу проекта, текущий URL: {project_page.page.url}"
            logger.info(f"Перешёл на страницу проекта: {project_url}")
            allure.attach(project_page.page.screenshot(), name="project_page_loaded.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Не удалось перейти на страницу проекта: {e}")
            allure.attach(project_page.page.content(), name="project_nav_error.html", attachment_type=allure.attachment_type.HTML)
            raise
    with allure.step("Проверка видимости колонки To Do"):
        try:
            todo_column = project_page.page.locator("div.border-green-400")
            todo_column.wait_for(state="visible", timeout=10000)
            logger.info("Колонка To Do видна")
            allure.attach(project_page.page.screenshot(), name="todo_column_visible.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Колонка To Do не видна: {e}")
            allure.attach(project_page.page.content(), name="todo_column_error.html", attachment_type=allure.attachment_type.HTML)
            raise
    with allure.step("Клик по кнопке 'плюс' в колонке To Do"):
        try:
            plus_button = project_page.page.locator("div.border-green-400 button:has(svg.lucide-plus)")
            plus_button.wait_for(state="visible", timeout=10000)
            plus_button.click()
            logger.info("Кликнул по кнопке 'плюс' в колонке To Do")
            allure.attach(project_page.page.screenshot(), name="plus_button_clicked.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Не удалось кликнуть по кнопке 'плюс': {e}")
            allure.attach(project_page.page.content(), name="plus_button_error.html", attachment_type=allure.attachment_type.HTML)
            raise
    with allure.step("Проверка открытия формы создания задачи"):
        try:
            task_form_title = project_page.page.locator("h1:has-text('Create new Task')")
            task_form_title.wait_for(state="visible", timeout=15000)
            assert task_form_title.is_visible(), "Форма создания задачи не открылась"
            logger.info("Форма создания задачи успешно открыта")
            allure.attach(project_page.page.screenshot(), name="task_form_opened.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Заголовок формы 'Create new Task' не виден: {e}")
            allure.attach(project_page.page.content(), name="task_form_error.html", attachment_type=allure.attachment_type.HTML)
            raise
    with allure.step("Заполнение формы создания задачи"):
        try:
            page = project_page.page
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            base_title = "Long Task Title for Testing Purposes Created on TaskFiller"
            filler = "X" * (100 - len(base_title) - len(current_time) - 1)
            task_title = f"{base_title}{filler} {current_time}"
            assert len(task_title) == 100, f"Длина названия задачи {len(task_title)}, ожидалось 100"
            page.locator("input[placeholder='Task Title']").fill(task_title)
            logger.info(f"Заполнено название задачи: {task_title}")
            page.locator("textarea[placeholder='Task Description']").fill("This is a test task description")
            logger.info("Заполнено описание задачи")
            page.locator("input[placeholder='Tags (comma separated)']").fill("test, automation")
            logger.info("Заполнены теги: test, automation")
            page.locator("input[placeholder='Start Date']").fill("2025-06-23")
            logger.info("Заполнена дата начала: 2025-06-23")
            page.locator("input[placeholder='Due Date']").fill("2025-06-30")
            logger.info("Заполнена дата окончания: 2025-06-30")
            page.locator("input[placeholder='Story Points']").fill("5")
            logger.info("Заполнены Story Points: 5")
            allure.attach(page.screenshot(), name="task_form_filled_100.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Не удалось заполнить форму задачи: {e}")
            allure.attach(page.content(), name="task_form_fill_error.html", attachment_type=allure.attachment_type.HTML)
            raise
    with allure.step("Отправка формы"):
        try:
            submit_button = page.locator("button[type='submit']:has-text('Create New Task')")
            submit_button.wait_for(state="visible", timeout=10000)
            submit_button.click()
            logger.info("Кликнул по кнопке 'Create New Task'")
            allure.attach(page.screenshot(), name="task_form_submitted_100.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Не удалось отправить форму задачи: {e}")
            allure.attach(page.content(), name="task_form_submit_error.html", attachment_type=allure.attachment_type.HTML)
            raise

@pytest.mark.tasks
@allure.title("Заполнение и отправка формы с названием задачи со специальными символами")
def test_create_task_with_special_chars_title(project_page: ProjectViewPage):
    project_url = f"{project_page.BASE_URL}/projects/193"
    with allure.step("Переход на страницу проекта"):
        project_page.navigate_to(project_url)
        try:
            project_page.page.wait_for_url(project_url, timeout=30000)
            assert project_page.page.url == project_url, f"Не удалось перейти на страницу проекта, текущий URL: {project_page.page.url}"
            logger.info(f"Перешёл на страницу проекта: {project_url}")
            allure.attach(project_page.page.screenshot(), name="project_page_loaded.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Не удалось перейти на страницу проекта: {e}")
            allure.attach(project_page.page.content(), name="project_nav_error.html", attachment_type=allure.attachment_type.HTML)
            raise
    with allure.step("Проверка видимости колонки To Do"):
        try:
            todo_column = project_page.page.locator("div.border-green-400")
            todo_column.wait_for(state="visible", timeout=10000)
            logger.info("Колонка To Do видна")
            allure.attach(project_page.page.screenshot(), name="todo_column_visible.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Колонка To Do не видна: {e}")
            allure.attach(project_page.page.content(), name="todo_column_error.html", attachment_type=allure.attachment_type.HTML)
            raise
    with allure.step("Клик по кнопке 'плюс' в колонке To Do"):
        try:
            plus_button = project_page.page.locator("div.border-green-400 button:has(svg.lucide-plus)")
            plus_button.wait_for(state="visible", timeout=10000)
            plus_button.click()
            logger.info("Кликнул по кнопке 'плюс' в колонке To Do")
            allure.attach(project_page.page.screenshot(), name="plus_button_clicked.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Не удалось кликнуть по кнопке 'плюс': {e}")
            allure.attach(project_page.page.content(), name="plus_button_error.html", attachment_type=allure.attachment_type.HTML)
            raise
    with allure.step("Проверка открытия формы создания задачи"):
        try:
            task_form_title = project_page.page.locator("h1:has-text('Create new Task')")
            task_form_title.wait_for(state="visible", timeout=15000)
            assert task_form_title.is_visible(), "Форма создания задачи не открылась"
            logger.info("Форма создания задачи успешно открыта")
            allure.attach(project_page.page.screenshot(), name="task_form_opened.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Заголовок формы 'Create new Task' не виден: {e}")
            allure.attach(project_page.page.content(), name="task_form_error.html", attachment_type=allure.attachment_type.HTML)
            raise
    with allure.step("Заполнение формы создания задачи"):
        try:
            page = project_page.page
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            base_title = "Task with Symbols @#$%&*! on"
            filler = "X" * 3
            task_title = f"{base_title} {filler} {current_time}"
            page.locator("input[placeholder='Task Title']").fill(task_title)
            logger.info(f"Заполнено название задачи: {task_title}")
            page.locator("textarea[placeholder='Task Description']").fill("This is a test task description")
            logger.info("Заполнено описание задачи")
            page.locator("input[placeholder='Tags (comma separated)']").fill("test, automation")
            logger.info("Заполнены теги: test, automation")
            page.locator("input[placeholder='Start Date']").fill("2025-06-23")
            logger.info("Заполнена дата начала: 2025-06-23")
            page.locator("input[placeholder='Due Date']").fill("2025-06-30")
            logger.info("Заполнена дата окончания: 2025-06-30")
            page.locator("input[placeholder='Story Points']").fill("5")
            logger.info("Заполнены Story Points: 5")
            allure.attach(page.screenshot(), name="task_form_filled_special_chars.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Не удалось заполнить форму задачи: {e}")
            allure.attach(page.content(), name="task_form_fill_error.html", attachment_type=allure.attachment_type.HTML)
            raise
    with allure.step("Отправка формы"):
        try:
            submit_button = page.locator("button[type='submit']:has-text('Create New Task')")
            submit_button.wait_for(state="visible", timeout=10000)
            submit_button.click()
            logger.info("Кликнул по кнопке 'Create New Task'")
            allure.attach(page.screenshot(), name="task_form_submitted_special_chars.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Не удалось отправить форму задачи: {e}")
            allure.attach(page.content(), name="task_form_submit_error.html", attachment_type=allure.attachment_type.HTML)
            raise