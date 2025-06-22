import pytest
import allure
from playwright.sync_api import Page
from pages.authentication_page import AuthenticationPage
from pages.project_view_page import ProjectViewPage
from pages.dashboard_page import DashboardPage
from settings import BASE_URL, EMAIL, PASSWORD
from utils.logger import logger
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from datetime import datetime

@pytest.mark.tasks
@allure.title("Переход на страницу задач")
def test_navigate_to_tasks(page):
    auth_page = AuthenticationPage(page)
    dashboard_page = DashboardPage(page)
    with allure.step("Переход на страницу авторизации"):
        auth_page.navigate()
        allure.attach(page.screenshot(), name="auth_page_loaded.png", attachment_type=allure.attachment_type.PNG)
    with allure.step("Вход в систему"):
        auth_page.login(EMAIL, PASSWORD)
        allure.attach(page.screenshot(), name="after_login.png", attachment_type=allure.attachment_type.PNG)
    with allure.step("Переход на дашборд"):
        page.goto(f"{BASE_URL}/dashboard", wait_until="domcontentloaded")
        allure.attach(page.screenshot(), name="dashboard_loaded.png", attachment_type=allure.attachment_type.PNG)
    with allure.step("Нажатие на кнопку задач"):
        allure.attach(page.screenshot(), name="before_tasks_button_click.png", attachment_type=allure.attachment_type.PNG)
        tasks_button = page.locator('a[href="/tasks"] svg.lucide-list-checks')
        tasks_button.wait_for(state='visible', timeout=30000)
        tasks_button.click(timeout=30000)
    with allure.step("Проверка изменения URL"):
        page.wait_for_url(f"{BASE_URL}/tasks", timeout=30000)
        assert page.url == f"{BASE_URL}/tasks", "Не удалось перейти на страницу задач"
        allure.attach(page.screenshot(), name="tasks_page_loaded.png", attachment_type=allure.attachment_type.PNG)
        logger.info("Successfully navigated to tasks page")

@pytest.mark.tasks
@allure.title("Переход на страницу проекта и открытие формы создания задачи")
def test_navigate_to_specific_project(page):
    auth_page = AuthenticationPage(page)
    project_view_page = ProjectViewPage(page)
    with allure.step("Переход на страницу авторизации"):
        auth_page.navigate()
        allure.attach(page.screenshot(), name="auth_page_loaded.png", attachment_type=allure.attachment_type.PNG)
    with allure.step("Вход в систему"):
        auth_page.login(EMAIL, PASSWORD)
        allure.attach(page.screenshot(), name="after_login.png", attachment_type=allure.attachment_type.PNG)
    with allure.step("Переход на страницу проекта"):
        project_url = f"{BASE_URL}/projects/193"
        try:
            project_view_page.navigate_to(project_url)
            page.wait_for_url(project_url, timeout=30000)
            assert page.url == project_url, f"Не удалось перейти на страницу проекта, текущий URL: {page.url}"
            logger.info(f"Navigated to project page: {project_url}")
            allure.attach(page.screenshot(), name="project_page_loaded.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Failed to navigate to project page: {e}")
            allure.attach(page.content(), name="project_nav_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(page.screenshot(), name="project_nav_error.png", attachment_type=allure.attachment_type.PNG)
            raise
    with allure.step("Проверка видимости колонки To Do"):
        try:
            todo_column = page.locator("div.border-green-400")
            todo_column.wait_for(state="visible", timeout=10000)
            logger.info("To Do column is visible")
            allure.attach(page.screenshot(), name="todo_column_visible.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"To Do column not visible: {e}")
            allure.attach(page.content(), name="todo_column_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(page.screenshot(), name="todo_column_error.png", attachment_type=allure.attachment_type.PNG)
            raise
    with allure.step("Клик по кнопке 'плюс' в колонке To Do"):
        try:
            plus_button = page.locator("div.border-green-400 button:has(svg.lucide-plus)")
            plus_button.wait_for(state="visible", timeout=10000)
            plus_button.click()
            logger.info("Clicked plus button in To Do column")
            allure.attach(page.screenshot(), name="plus_button_clicked.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Failed to click plus button: {e}")
            allure.attach(page.content(), name="plus_button_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(page.screenshot(), name="plus_button_error.png", attachment_type=allure.attachment_type.PNG)
            raise
    with allure.step("Проверка открытия формы создания задачи"):
        try:
            task_form_title = page.locator("h1:has-text('Create new Task')")
            task_form_title.wait_for(state="visible", timeout=15000)
            assert task_form_title.is_visible(), "Форма создания задачи не открылась (заголовок не виден)"
            logger.info("Task creation form opened successfully with title 'Create new Task'")
            allure.attach(page.screenshot(), name="task_form_opened.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Task form title 'Create new Task' not visible: {e}")
            allure.attach(page.content(), name="task_form_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(page.screenshot(), name="task_form_error.png", attachment_type=allure.attachment_type.PNG)
            raise

@pytest.mark.tasks
@allure.title("Заполнение и отправка формы создания задачи")
def test_create_task_in_todo(page):
    auth_page = AuthenticationPage(page)
    project_view_page = ProjectViewPage(page)
    with allure.step("Переход на страницу авторизации"):
        auth_page.navigate()
        allure.attach(page.screenshot(), name="auth_page_loaded.png", attachment_type=allure.attachment_type.PNG)
    with allure.step("Вход в систему"):
        auth_page.login(EMAIL, PASSWORD)
        allure.attach(page.screenshot(), name="after_login.png", attachment_type=allure.attachment_type.PNG)
    with allure.step("Переход на страницу проекта"):
        project_url = f"{BASE_URL}/projects/193"
        try:
            project_view_page.navigate_to(project_url)
            page.wait_for_url(project_url, timeout=30000)
            assert page.url == project_url, f"Не удалось перейти на страницу проекта, текущий URL: {page.url}"
            logger.info(f"Navigated to project page: {project_url}")
            allure.attach(page.screenshot(), name="project_page_loaded.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Failed to navigate to project page: {e}")
            allure.attach(page.content(), name="project_nav_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(page.screenshot(), name="project_nav_error.png", attachment_type=allure.attachment_type.PNG)
            raise
    with allure.step("Проверка видимости колонки To Do"):
        try:
            todo_column = page.locator("div.border-green-400")
            todo_column.wait_for(state="visible", timeout=10000)
            logger.info("To Do column is visible")
            allure.attach(page.screenshot(), name="todo_column_visible.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"To Do column not visible: {e}")
            allure.attach(page.content(), name="todo_column_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(page.screenshot(), name="todo_column_error.png", attachment_type=allure.attachment_type.PNG)
            raise
    with allure.step("Клик по кнопке 'плюс' в колонке To Do"):
        try:
            plus_button = page.locator("div.border-green-400 button:has(svg.lucide-plus)")
            plus_button.wait_for(state="visible", timeout=10000)
            plus_button.click()
            logger.info("Clicked plus button in To Do column")
            allure.attach(page.screenshot(), name="plus_button_clicked.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Failed to click plus button: {e}")
            allure.attach(page.content(), name="plus_button_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(page.screenshot(), name="plus_button_error.png", attachment_type=allure.attachment_type.PNG)
            raise
    with allure.step("Проверка открытия формы создания задачи"):
        try:
            task_form_title = page.locator("h1:has-text('Create new Task')")
            task_form_title.wait_for(state="visible", timeout=15000)
            assert task_form_title.is_visible(), "Форма создания задачи не открылась (заголовок не виден)"
            logger.info("Task creation form opened successfully")
            allure.attach(page.screenshot(), name="task_form_opened.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Task form title 'Create new Task' not visible: {e}")
            allure.attach(page.content(), name="task_form_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(page.screenshot(), name="task_form_error.png", attachment_type=allure.attachment_type.PNG)
            raise
    with allure.step("Заполнение формы создания задачи"):
        try:
            # Task Title
            task_title = "Test Task"
            page.locator("input[placeholder='Task Title']").fill(task_title)
            logger.info(f"Filled Task Title: {task_title}")
            # Task Description
            page.locator("textarea[placeholder='Task Description']").fill("This is a test task description")
            logger.info("Filled Task Description")
            # Tags
            page.locator("input[placeholder='Tags (comma separated)']").fill("test, automation")
            logger.info("Filled Tags: test, automation")
            # Start Date
            page.locator("input[placeholder='Start Date']").fill("2025-06-23")
            logger.info("Filled Start Date: 2025-06-23")
            # Due Date
            page.locator("input[placeholder='Due Date']").fill("2025-06-30")
            logger.info("Filled Due Date: 2025-06-30")
            # Story Points
            page.locator("input[placeholder='Story Points']").fill("5")
            logger.info("Filled Story Points: 5")
            allure.attach(page.screenshot(), name="task_form_filled.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Failed to fill task form: {e}")
            allure.attach(page.content(), name="task_form_fill_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(page.screenshot(), name="task_form_fill_error.png", attachment_type=allure.attachment_type.PNG)
            raise
    with allure.step("Отправка формы"):
        try:
            submit_button = page.locator("button[type='submit']:has-text('Create New Task')")
            submit_button.wait_for(state="visible", timeout=10000)
            logger.info("Submit button is visible")
            submit_button.click()
            logger.info("Clicked Create New Task button")
            allure.attach(page.screenshot(), name="task_form_submitted.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Failed to submit task form: {e}")
            allure.attach(page.content(), name="task_form_submit_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(page.screenshot(), name="task_form_submit_error.png", attachment_type=allure.attachment_type.PNG)
            raise

@pytest.mark.tasks
@allure.title("Заполнение и отправка формы с названием задачи на 100 символов")
def test_create_task_with_100_char_title(page):
    auth_page = AuthenticationPage(page)
    project_view_page = ProjectViewPage(page)
    with allure.step("Переход на страницу авторизации"):
        auth_page.navigate()
        allure.attach(page.screenshot(), name="auth_page_loaded.png", attachment_type=allure.attachment_type.PNG)
    with allure.step("Вход в систему"):
        auth_page.login(EMAIL, PASSWORD)
        allure.attach(page.screenshot(), name="after_login.png", attachment_type=allure.attachment_type.PNG)
    with allure.step("Переход на страницу проекта"):
        project_url = f"{BASE_URL}/projects/193"
        try:
            project_view_page.navigate_to(project_url)
            page.wait_for_url(project_url, timeout=30000)
            assert page.url == project_url, f"Не удалось перейти на страницу проекта, текущий URL: {page.url}"
            logger.info(f"Navigated to project page: {project_url}")
            allure.attach(page.screenshot(), name="project_page_loaded.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Failed to navigate to project page: {e}")
            allure.attach(page.content(), name="project_nav_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(page.screenshot(), name="project_nav_error.png", attachment_type=allure.attachment_type.PNG)
            raise
    with allure.step("Проверка видимости колонки To Do"):
        try:
            todo_column = page.locator("div.border-green-400")
            todo_column.wait_for(state="visible", timeout=10000)
            logger.info("To Do column is visible")
            allure.attach(page.screenshot(), name="todo_column_visible.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"To Do column not visible: {e}")
            allure.attach(page.content(), name="todo_column_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(page.screenshot(), name="todo_column_error.png", attachment_type=allure.attachment_type.PNG)
            raise
    with allure.step("Клик по кнопке 'плюс' в колонке To Do"):
        try:
            plus_button = page.locator("div.border-green-400 button:has(svg.lucide-plus)")
            plus_button.wait_for(state="visible", timeout=10000)
            plus_button.click()
            logger.info("Clicked plus button in To Do column")
            allure.attach(page.screenshot(), name="plus_button_clicked.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Failed to click plus button: {e}")
            allure.attach(page.content(), name="plus_button_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(page.screenshot(), name="plus_button_error.png", attachment_type=allure.attachment_type.PNG)
            raise
    with allure.step("Проверка открытия формы создания задачи"):
        try:
            task_form_title = page.locator("h1:has-text('Create new Task')")
            task_form_title.wait_for(state="visible", timeout=15000)
            assert task_form_title.is_visible(), "Форма создания задачи не открылась (заголовок не виден)"
            logger.info("Task creation form opened successfully")
            allure.attach(page.screenshot(), name="task_form_opened.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Task form title 'Create new Task' not visible: {e}")
            allure.attach(page.content(), name="task_form_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(page.screenshot(), name="task_form_error.png", attachment_type=allure.attachment_type.PNG)
            raise
    with allure.step("Заполнение формы создания задачи"):
        try:
            # Generate 100-character task title with current date and time
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            base_title = "Long Task Title for Testing Purposes Created on TaskFiller"
            filler = "X" * (100 - len(base_title) - len(current_time) - 1)  # -1 for space
            task_title = f"{base_title}{filler} {current_time}"
            assert len(task_title) == 100, f"Task title length is {len(task_title)}, expected 100"
            page.locator("input[placeholder='Task Title']").fill(task_title)
            logger.info(f"Filled Task Title: {task_title}")
            # Task Description
            page.locator("textarea[placeholder='Task Description']").fill("This is a test task description")
            logger.info("Filled Task Description")
            # Tags
            page.locator("input[placeholder='Tags (comma separated)']").fill("test, automation")
            logger.info("Filled Tags: test, automation")
            # Start Date
            page.locator("input[placeholder='Start Date']").fill("2025-06-23")
            logger.info("Filled Start Date: 2025-06-23")
            # Due Date
            page.locator("input[placeholder='Due Date']").fill("2025-06-30")
            logger.info("Filled Due Date: 2025-06-30")
            # Story Points
            page.locator("input[placeholder='Story Points']").fill("5")
            logger.info("Filled Story Points: 5")
            allure.attach(page.screenshot(), name="task_form_filled_100.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Failed to fill task form: {e}")
            allure.attach(page.content(), name="task_form_fill_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(page.screenshot(), name="task_form_fill_error.png", attachment_type=allure.attachment_type.PNG)
            raise
    with allure.step("Отправка формы"):
        try:
            submit_button = page.locator("button[type='submit']:has-text('Create New Task')")
            submit_button.wait_for(state="visible", timeout=10000)
            logger.info("Submit button is visible")
            submit_button.click()
            logger.info("Clicked Create New Task button")
            allure.attach(page.screenshot(), name="task_form_submitted_100.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Failed to submit task form: {e}")
            allure.attach(page.content(), name="task_form_submit_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(page.screenshot(), name="task_form_submit_error.png", attachment_type=allure.attachment_type.PNG)
            raise

@pytest.mark.tasks
@allure.title("Заполнение и отправка формы с названием задачи со специальными символами")
def test_create_task_with_special_chars_title(page):
    auth_page = AuthenticationPage(page)
    project_view_page = ProjectViewPage(page)
    with allure.step("Переход на страницу авторизации"):
        auth_page.navigate()
        allure.attach(page.screenshot(), name="auth_page_loaded.png", attachment_type=allure.attachment_type.PNG)
    with allure.step("Вход в систему"):
        auth_page.login(EMAIL, PASSWORD)
        allure.attach(page.screenshot(), name="after_login.png", attachment_type=allure.attachment_type.PNG)
    with allure.step("Переход на страницу проекта"):
        project_url = f"{BASE_URL}/projects/193"
        try:
            project_view_page.navigate_to(project_url)
            page.wait_for_url(project_url, timeout=30000)
            assert page.url == project_url, f"Не удалось перейти на страницу проекта, текущий URL: {page.url}"
            logger.info(f"Navigated to project page: {project_url}")
            allure.attach(page.screenshot(), name="project_page_loaded.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Failed to navigate to project page: {e}")
            allure.attach(page.content(), name="project_nav_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(page.screenshot(), name="project_nav_error.png", attachment_type=allure.attachment_type.PNG)
            raise
    with allure.step("Проверка видимости колонки To Do"):
        try:
            todo_column = page.locator("div.border-green-400")
            todo_column.wait_for(state="visible", timeout=10000)
            logger.info("To Do column is visible")
            allure.attach(page.screenshot(), name="todo_column_visible.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"To Do column not visible: {e}")
            allure.attach(page.content(), name="todo_column_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(page.screenshot(), name="todo_column_error.png", attachment_type=allure.attachment_type.PNG)
            raise
    with allure.step("Клик по кнопке 'плюс' в колонке To Do"):
        try:
            plus_button = page.locator("div.border-green-400 button:has(svg.lucide-plus)")
            plus_button.wait_for(state="visible", timeout=10000)
            plus_button.click()
            logger.info("Clicked plus button in To Do column")
            allure.attach(page.screenshot(), name="plus_button_clicked.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Failed to click plus button: {e}")
            allure.attach(page.content(), name="plus_button_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(page.screenshot(), name="plus_button_error.png", attachment_type=allure.attachment_type.PNG)
            raise
    with allure.step("Проверка открытия формы создания задачи"):
        try:
            task_form_title = page.locator("h1:has-text('Create new Task')")
            task_form_title.wait_for(state="visible", timeout=15000)
            assert task_form_title.is_visible(), "Форма создания задачи не открылась (заголовок не виден)"
            logger.info("Task creation form opened successfully")
            allure.attach(page.screenshot(), name="task_form_opened.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Task form title 'Create new Task' not visible: {e}")
            allure.attach(page.content(), name="task_form_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(page.screenshot(), name="task_form_error.png", attachment_type=allure.attachment_type.PNG)
            raise
    with allure.step("Заполнение формы создания задачи"):
        try:
            # Generate task title with special characters and current date and time
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            base_title = "Task with Symbols @#$%&*! on"
            filler = "X" * 3  # To reach ~50 characters
            task_title = f"{base_title} {filler} {current_time}"
            page.locator("input[placeholder='Task Title']").fill(task_title)
            logger.info(f"Filled Task Title: {task_title}")
            # Task Description
            page.locator("textarea[placeholder='Task Description']").fill("This is a test task description")
            logger.info("Filled Task Description")
            # Tags
            page.locator("input[placeholder='Tags (comma separated)']").fill("test, automation")
            logger.info("Filled Tags: test, automation")
            # Start Date
            page.locator("input[placeholder='Start Date']").fill("2025-06-23")
            logger.info("Filled Start Date: 2025-06-23")
            # Due Date
            page.locator("input[placeholder='Due Date']").fill("2025-06-30")
            logger.info("Filled Due Date: 2025-06-30")
            # Story Points
            page.locator("input[placeholder='Story Points']").fill("5")
            logger.info("Filled Story Points: 5")
            allure.attach(page.screenshot(), name="task_form_filled_special_chars.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Failed to fill task form: {e}")
            allure.attach(page.content(), name="task_form_fill_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(page.screenshot(), name="task_form_fill_error.png", attachment_type=allure.attachment_type.PNG)
            raise
    with allure.step("Отправка формы"):
        try:
            submit_button = page.locator("button[type='submit']:has-text('Create New Task')")
            submit_button.wait_for(state="visible", timeout=10000)
            logger.info("Submit button is visible")
            submit_button.click()
            logger.info("Clicked Create New Task button")
            allure.attach(page.screenshot(), name="task_form_submitted_special_chars.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Failed to submit task form: {e}")
            allure.attach(page.content(), name="task_form_submit_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(page.screenshot(), name="task_form_submit_error.png", attachment_type=allure.attachment_type.PNG)
            raise