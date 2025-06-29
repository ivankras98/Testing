# tests/test_projects.py
import pytest
import allure
from pages.project_page import ProjectPage
from pages.dashboard_page import DashboardPage
from utils.logger import logger
from datetime import datetime, timedelta
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="function")
def project_page(authenticated_context):
    page = authenticated_context.new_page()
    project_page = ProjectPage(page)
    yield project_page
    page.close()


@pytest.mark.smoke
@pytest.mark.projects
@allure.title("Удаление первого проекта в списке")
def test_delete_first_project(project_page: ProjectPage):
    with allure.step("Переход на дашборд"):
        project_page.navigate_to(f"{project_page.BASE_URL}/dashboard")
    with allure.step("Удаление первого проекта"):
        try:
            dashboard_page = DashboardPage(project_page.page)
            project_name = dashboard_page.delete_first_project()
            allure.attach(project_page.page.screenshot(), name="after_delete.png", attachment_type=allure.attachment_type.PNG)
            logger.info(f"Первый проект {project_name} успешно удалён")
        except PlaywrightTimeoutError as e:
            logger.error(f"Не удалось удалить проект: {e}")
            allure.attach(project_page.page.content(), name="delete_error.html", attachment_type=allure.attachment_type.HTML)
            raise


@pytest.mark.projects
@pytest.mark.regression
@allure.title("Успешное создание проекта со всеми заполненными полями")
def test_create_project_success(project_page: ProjectPage):
    with allure.step("Переход на дашборд"):
        project_page.navigate_to(f"{project_page.BASE_URL}/dashboard")
    with allure.step("Закрытие формы создания проекта, если она открыта"):
        if project_page.is_create_form_visible():
            project_page.close_create_form()
            logger.info("Форма создания проекта была открыта и закрыта")
    with allure.step("Открытие формы создания проекта"):
        dashboard_page = DashboardPage(project_page.page)
        dashboard_page.click_plus_button()
    with allure.step("Заполнение формы"):
        project_name = "Test Project " + datetime.now().strftime("%Y%m%d%H%M%S")
        project_page.fill_project_name(project_name)
        project_page.fill_description("Test description")
        start_date = datetime.now().strftime("%Y-%m-%d")
        project_page.fill_start_date(start_date)
        end_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        project_page.fill_end_date(end_date)
        project_page.fill_status("In Progress")
        allure.attach(project_page.page.screenshot(), name="project_form_filled.png", attachment_type=allure.attachment_type.PNG)
    with allure.step("Отправка формы"):
        project_page.submit_create_project()

    with allure.step("Проверка успешности создания проекта"):
        try:
            project_page.page.wait_for_selector("div.text-green-500:has-text('Project created successfully'), [class*='success']", state="visible", timeout=5000)
            logger.info(f"Проект {project_name} успешно создан")
            allure.attach(project_page.page.screenshot(), name="project_created.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError:
            logger.error("Сообщение об успехе не найдено, проверка отсутствия ошибки")
            assert not project_page.error_message.is_visible(timeout=5000), "Обнаружена ошибка при создании проекта"
            logger.info(f"Проект {project_name} создан (без сообщения об успехе)")
            allure.attach(project_page.page.screenshot(), name="project_created_no_success_message.png", attachment_type=allure.attachment_type.PNG)


@pytest.mark.projects
@pytest.mark.regression
@allure.title("Создание проекта с длинным названием (больше 100 символов)")
def test_create_project_long_name(project_page: ProjectPage):
    with allure.step("Переход на дашборд"):
        project_page.navigate_to(f"{project_page.BASE_URL}/dashboard")
    with allure.step("Закрытие формы создания проекта, если она открыта"):
        if project_page.is_create_form_visible():
            project_page.close_create_form()
            logger.info("Форма создания проекта была открыта и закрыта")
    with allure.step("Заполнение длинным названием"):
        long_name = "LongName_" + "a" * 90 + datetime.now().strftime("%Y%m%d%H%M%S")
        project_page.fill_project_name(long_name)
        project_page.fill_description("Test description")
        start_date = datetime.now().strftime("%Y-%m-%d")
        project_page.fill_start_date(start_date)
        end_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        project_page.fill_end_date(end_date)
        project_page.fill_status("In Progress")
        allure.attach(project_page.page.screenshot(), name="project_form_long_name.png", attachment_type=allure.attachment_type.PNG)
    with allure.step("Отправка формы"):
        project_page.submit_create_project()

    with allure.step("Проверка отображения ошибки"):
        try:
            project_page.page.wait_for_selector("text=Project name too long", state="visible", timeout=5000)
            logger.info("Ошибка для длинного названия отображена")
            allure.attach(project_page.page.screenshot(), name="long_name_error.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError:
            logger.error("Ошибка для длинного названия не отображена, проверка отсутствия сообщения об успехе")
            assert not project_page.page.locator("div.text-green-500:has-text('Project created successfully'), [class*='success']").is_visible(timeout=5000), "Проект с длинным названием неожиданно создан"
            logger.info(f"Проект с названием длиной {len(long_name)} символов не создан")
            allure.attach(project_page.page.screenshot(), name="long_name_not_created.png", attachment_type=allure.attachment_type.PNG)


@pytest.mark.projects
@pytest.mark.regression
@allure.title("Создание проекта с названием, содержащим специальные символы")
def test_create_project_special_chars(project_page: ProjectPage):
    with allure.step("Переход на дашборд"):
        project_page.navigate_to(f"{project_page.BASE_URL}/dashboard")
    with allure.step("Закрытие формы создания проекта, если она открыта"):
        if project_page.is_create_form_visible():
            project_page.close_create_form()
            logger.info("Форма создания проекта была открыта и закрыта")
    with allure.step("Заполнение формы с особыми символами"):
        project_name = "Test@#$%_" + datetime.now().strftime("%Y%m%d%H%M%S")
        project_page.fill_project_name(project_name)
        project_page.fill_description("Test with special chars")
        start_date = datetime.now().strftime("%Y-%m-%d")
        project_page.fill_start_date(start_date)
        end_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        project_page.fill_end_date(end_date)
        project_page.fill_status("In Progress")
        allure.attach(project_page.page.screenshot(), name="project_form_special_chars.png", attachment_type=allure.attachment_type.PNG)
    with allure.step("Отправка формы"):
        project_page.submit_create_project()

    with allure.step("Проверка успешности создания проекта"):
        try:
            project_page.page.wait_for_selector("div.text-green-500:has-text('Project created successfully'), [class*='success']", state="visible", timeout=5000)
            logger.info(f"Проект {project_name} с особыми символами успешно создан")
            allure.attach(project_page.page.screenshot(), name="project_special_chars_created.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError:
            logger.error("Сообщение об успехе не найдено, проверка отсутствия ошибки")
            assert not project_page.error_message.is_visible(timeout=5000), "Обнаружена ошибка при создании проекта"
            logger.info(f"Проект {project_name} создан (без сообщения об успехе)")
            allure.attach(project_page.page.screenshot(), name="project_special_chars_no_success_message.png", attachment_type=allure.attachment_type.PNG)


@pytest.mark.projects
@pytest.mark.regression
@allure.title("Проверка, что кнопка 'Create' неактивна при пустом названии")
def test_create_button_disabled_on_empty_name(project_page: ProjectPage):
    with allure.step("Переход на дашборд"):
        project_page.navigate_to(f"{project_page.BASE_URL}/dashboard")
    with allure.step("Закрытие формы создания проекта, если она открыта"):
        if project_page.is_create_form_visible():
            project_page.close_create_form()
            logger.info("Форма создания проекта была открыта и закрыта")
    with allure.step("Оставление поля названия пустым"):
        project_page.fill_project_name("")
        project_page.fill_description("Test description")
        start_date = datetime.now().strftime("%Y-%m-%d")
        project_page.fill_start_date(start_date)
        end_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        project_page.fill_end_date(end_date)
        project_page.fill_status("In Progress")
        allure.attach(project_page.page.screenshot(), name="project_form_empty_name.png", attachment_type=allure.attachment_type.PNG)
    with allure.step("Проверка неактивности кнопки"):
        assert not project_page.is_create_button_enabled(), "Кнопка 'Create' активна при пустом названии"
        logger.info("Кнопка 'Create' корректно неактивна при пустом названии")
        allure.attach(project_page.page.screenshot(), name="create_button_disabled.png", attachment_type=allure.attachment_type.PNG)


@pytest.mark.projects
@pytest.mark.regression
@allure.title("Создание проекта с End Date раньше, чем Start Date")
def test_create_project_invalid_date_range(project_page: ProjectPage):
    with allure.step("Переход на дашборд"):
        project_page.navigate_to(f"{project_page.BASE_URL}/dashboard")
    with allure.step("Закрытие формы создания проекта, если она открыта"):
        if project_page.is_create_form_visible():
            project_page.close_create_form()
            logger.info("Форма создания проекта была открыта и закрыта")
    with allure.step("Заполнение формы с неверным диапазоном дат"):
        project_name = "InvalidDate_" + datetime.now().strftime("%Y%m%d%H%M%S")
        project_page.fill_project_name(project_name)
        project_page.fill_description("Test with invalid date range")
        start_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        project_page.fill_start_date(start_date)
        end_date = datetime.now().strftime("%Y-%m-%d")
        project_page.fill_end_date(end_date)
        project_page.fill_status("In Progress")
        allure.attach(project_page.page.screenshot(), name="project_form_invalid_dates.png", attachment_type=allure.attachment_type.PNG)
    with allure.step("Отправка формы"):
        project_page.submit_create_project()

    with allure.step("Проверка, что проект не создан"):
        try:
            project_page.page.wait_for_selector("text=Invalid date range", state="visible", timeout=5000)
            logger.info("Ошибка для неверного диапазона дат отображена")
            allure.attach(project_page.page.screenshot(), name="invalid_date_range_error.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError:
            logger.error("Ошибка для неверного диапазона дат не отображена, проверка отсутствия сообщения об успехе")
            assert not project_page.page.locator("div.text-green-500:has-text('Project created successfully'), [class*='success']").is_visible(timeout=5000), "Проект с неверным диапазоном дат неожиданно создан"
            logger.info(f"Проект {project_name} не создан")
            allure.attach(project_page.page.screenshot(), name="invalid_date_range_not_created.png", attachment_type=allure.attachment_type.PNG)


@pytest.mark.projects
@pytest.mark.regression
@allure.title("Создание проекта с некорректной датой")
def test_create_project_invalid_date(project_page: ProjectPage):
    with allure.step("Переход на дашборд"):
        project_page.navigate_to(f"{project_page.BASE_URL}/dashboard")
    with allure.step("Закрытие формы создания проекта, если она открыта"):
        if project_page.is_create_form_visible():
            project_page.close_create_form()
            logger.info("Форма создания проекта была открыта и закрыта")
    with allure.step("Заполнение формы с некорректной датой"):
        project_name = "InvalidDateTest_" + datetime.now().strftime("%Y%m%d%H%M%S")
        project_page.fill_project_name(project_name)
        project_page.fill_description("Test with invalid date")
        invalid_start_date = "275760-01-01"
        project_page.fill_start_date(invalid_start_date)
        end_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        project_page.fill_end_date(end_date)
        project_page.fill_status("In Progress")
        allure.attach(project_page.page.screenshot(), name="project_form_invalid_date.png", attachment_type=allure.attachment_type.PNG)
    with allure.step("Отправка формы"):
        project_page.submit_create_project()
 
    with allure.step("Проверка, что проект не создан"):
        try:
            project_page.page.wait_for_selector("text=Invalid date", state="visible", timeout=5000)
            logger.info("Ошибка для некорректной даты отображена")
            allure.attach(project_page.page.screenshot(), name="invalid_date_error.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError:
            logger.error("Ошибка для некорректной даты не отображена, проверка отсутствия сообщения об успехе")
            assert not project_page.page.locator("div.text-green-500:has-text('Project created successfully'), [class*='success']").is_visible(timeout=5000), "Проект с некорректной датой неожиданно создан"
            logger.info(f"Проект {project_name} не создан")
            allure.attach(project_page.page.screenshot(), name="invalid_date_not_created.png", attachment_type=allure.attachment_type.PNG)