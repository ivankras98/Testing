import pytest
import allure
from pages.project_page import ProjectPage
from pages.dashboard_page import DashboardPage
from pages.authentication_page import AuthenticationPage
from settings import BASE_URL, EMAIL, PASSWORD
from utils.logger import logger
from datetime import datetime, timedelta
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

@pytest.mark.smoke
@pytest.mark.projects
@allure.title("Успешное создание проекта со всеми заполненными полями")
def test_create_project_success(page):
    auth_page = AuthenticationPage(page)
    dashboard_page = DashboardPage(page)
    project_page = ProjectPage(page)
    with allure.step("Переход на страницу авторизации"):
        auth_page.navigate()
    with allure.step("Вход в систему"):
        auth_page.login(EMAIL, PASSWORD)
    with allure.step("Переход на дашборд"):
        page.goto(f"{BASE_URL}/dashboard", wait_until="domcontentloaded")
    with allure.step("Открытие формы создания проекта"):
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
    with allure.step("Отправка формы"):
        project_page.submit_create_project()
    with allure.step("Проверка отображения проекта"):
        page.wait_for_selector(f"text={project_name}", state="visible", timeout=5000)
        assert project_page.is_project_visible(project_name), "Созданный проект не отображается"
        logger.info(f"Проект {project_name} успешно создан")

@pytest.mark.projects
@allure.title("Создание проекта с длинным названием (больше 100 символов)")
def test_create_project_long_name(page):
    auth_page = AuthenticationPage(page)
    dashboard_page = DashboardPage(page)
    project_page = ProjectPage(page)
    with allure.step("Переход на страницу авторизации"):
        auth_page.navigate()
    with allure.step("Вход в систему"):
        auth_page.login(EMAIL, PASSWORD)
    with allure.step("Переход на дашборд"):
        page.goto(f"{BASE_URL}/dashboard", wait_until="domcontentloaded")
    with allure.step("Открытие формы создания проекта"):
        dashboard_page.click_plus_button()
    with allure.step("Заполнение длинным названием"):
        long_name = "a" * 101
        project_page.fill_project_name(long_name)
        project_page.fill_description("Test description")
        start_date = datetime.now().strftime("%Y-%m-%d")
        project_page.fill_start_date(start_date)
        end_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        project_page.fill_end_date(end_date)
        project_page.fill_status("In Progress")
    with allure.step("Отправка формы"):
        project_page.submit_create_project()
    with allure.step("Проверка отображения ошибки или успеха"):
        try:
            project_page.page.wait_for_selector("text=Project name too long", state="visible", timeout=5000)
            assert False, "Ожидалась ошибка для длинного названия"
        except PlaywrightTimeoutError:
            page.wait_for_selector(f"text={long_name}", state="visible", timeout=5000)
            assert project_page.is_project_visible(long_name), "Проект с длинным названием не отображается"
        logger.info(f"Попытка создания проекта с названием длиной {len(long_name)} символов")

@pytest.mark.projects
@allure.title("Открытие формы создания проекта и её закрытие без сохранения")
def test_open_and_close_create_form(page):
    auth_page = AuthenticationPage(page)
    dashboard_page = DashboardPage(page)
    project_page = ProjectPage(page)
    with allure.step("Переход на страницу авторизации"):
        auth_page.navigate()
    with allure.step("Вход в систему"):
        auth_page.login(EMAIL, PASSWORD)
    with allure.step("Переход на дашборд"):
        page.goto(f"{BASE_URL}/dashboard", wait_until="domcontentloaded")
    with allure.step("Открытие формы создания проекта"):
        dashboard_page.click_plus_button()
    with allure.step("Закрытие формы без сохранения"):
        project_page.close_create_form()
    with allure.step("Проверка, что форма закрыта"):
        assert not project_page.is_create_form_visible(), "Форма создания проекта осталась открыта"
        logger.info("Форма создания проекта успешно закрыта")

@pytest.mark.projects
@allure.title("Создание проекта с названием, содержащим специальные символы (например, @#$%)")
def test_create_project_special_chars(page):
    auth_page = AuthenticationPage(page)
    dashboard_page = DashboardPage(page)
    project_page = ProjectPage(page)
    with allure.step("Переход на страницу авторизации"):
        auth_page.navigate()
    with allure.step("Вход в систему"):
        auth_page.login(EMAIL, PASSWORD)
    with allure.step("Переход на дашборд"):
        page.goto(f"{BASE_URL}/dashboard", wait_until="domcontentloaded")
    with allure.step("Открытие формы создания проекта"):
        dashboard_page.click_plus_button()
    with allure.step("Заполнение формы с особыми символами"):
        project_name = "Test@#$%_" + datetime.now().strftime("%Y%m%d%H%M%S")
        project_page.fill_project_name(project_name)
        project_page.fill_description("Test with special chars")
        start_date = datetime.now().strftime("%Y-%m-%d")
        project_page.fill_start_date(start_date)
        end_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        project_page.fill_end_date(end_date)
        project_page.fill_status("In Progress")
    with allure.step("Отправка формы"):
        project_page.submit_create_project()
    with allure.step("Проверка отображения проекта"):
        page.wait_for_selector(f"text={project_name}", state="visible", timeout=5000)
        assert project_page.is_project_visible(project_name), "Проект с особыми символами не отображается"
        logger.info(f"Проект {project_name} с особыми символами успешно создан")

@pytest.mark.projects
@allure.title("Проверка, что кнопка 'Create' неактивна при пустом названии")
def test_create_button_disabled_on_empty_name(page):
    auth_page = AuthenticationPage(page)
    dashboard_page = DashboardPage(page)
    project_page = ProjectPage(page)
    with allure.step("Переход на страницу авторизации"):
        auth_page.navigate()
    with allure.step("Вход в систему"):
        auth_page.login(EMAIL, PASSWORD)
    with allure.step("Переход на дашборд"):
        page.goto(f"{BASE_URL}/dashboard", wait_until="domcontentloaded")
    with allure.step("Открытие формы создания проекта"):
        dashboard_page.click_plus_button()
    with allure.step("Оставление поля поля пустым"):
        project_page.fill_project_name("")
        project_page.fill_description("Test description")
        start_date = datetime.now().strftime("%Y-%m-%d")
        project_page.fill_start_date(start_date)
        end_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        project_page.fill_end_date(end_date)
        project_page.fill_status("In Progress")
    with allure.step("Проверка неактивности кнопки"):
        assert not project_page.is_create_button_enabled(), "Кнопка 'Create' активна при пустом названии"
        logger.info("Кнопка 'Create' корректно неактивна при пустом названии")

@pytest.mark.projects
@allure.title("Удаление первого проекта в списке")
def test_delete_first_project(page):
    auth_page = AuthenticationPage(page)
    dashboard_page = DashboardPage(page)
    project_page = ProjectPage(page)
    with allure.step("Переход на страницу авторизации"):
        auth_page.navigate()
    with allure.step("Вход в систему"):
        auth_page.login(EMAIL, PASSWORD)
    with allure.step("Переход на дашборд"):
        page.goto(f"{BASE_URL}/dashboard", wait_until="domcontentloaded")
    with allure.step("Удаление первого проекта"):
        try:
            project_name = dashboard_page.delete_first_project()
        except PlaywrightTimeoutError as e:
            logger.error(f"Failed to delete project: {e}")
            allure.attach(page.content(), name="delete_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(page.screenshot(), name="delete_error.png", attachment_type=allure.attachment_type.PNG)
            raise
    with allure.step("Проверка удаления"):
        assert not project_page.is_project_visible(project_name), f"Проект {project_name} не удалён"
        logger.info(f"Первый проект {project_name} успешно удалён")

@pytest.mark.projects
@allure.title("Проверка, что поля формы очищаются после успешного создания проекта")
def test_form_clears_after_creation(page):
    auth_page = AuthenticationPage(page)
    dashboard_page = DashboardPage(page)
    project_page = ProjectPage(page)
    with allure.step("Переход на страницу авторизации"):
        auth_page.navigate()
    with allure.step("Вход в систему"):
        auth_page.login(EMAIL, PASSWORD)
    with allure.step("Переход на дашборд"):
        page.goto(f"{BASE_URL}/dashboard", wait_until="domcontentloaded")
    with allure.step("Открытие формы создания проекта"):
        dashboard_page.click_plus_button()
    with allure.step("Заполнение и отправка формы"):
        project_name = "ClearTest_" + datetime.now().strftime("%Y%m%d%H%M%S")
        project_page.fill_project_name(project_name)
        project_page.fill_description("Test description")
        start_date = datetime.now().strftime("%Y-%m-%d")
        project_page.fill_start_date(start_date)
        end_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        project_page.fill_end_date(end_date)
        project_page.fill_status("In Progress")
        project_page.submit_create_project()
    with allure.step("Повторное открытие формы"):
        dashboard_page.click_plus_button()
    with allure.step("Проверка очистки полей"):
        assert project_page.is_field_empty("project_name"), "Поле названия не очищено"
        assert project_page.is_field_empty("description"), "Поле поля не очищено"
        assert project_page.is_field_empty("start_date"), "Поле даты начала не очищено"
        assert project_page.is_field_empty("end_date"), "Поле даты окончания не очищено"
        assert project_page.is_status_default(), "Статус не сброшен на 'Not Started'"
        logger.info("Поля формы успешно очищены после создания")

@pytest.mark.projects
@allure.title("Создание проекта с End Date раньше, чем Start Date")
def test_create_project_invalid_date_range(page):
    auth_page = AuthenticationPage(page)
    dashboard_page = DashboardPage(page)
    project_page = ProjectPage(page)
    with allure.step("Переход на страницу авторизации"):
        auth_page.navigate()
    with allure.step("Вход в систему"):
        auth_page.login(EMAIL, PASSWORD)
    with allure.step("Переход на дашборд"):
        page.goto(f"{BASE_URL}/dashboard", wait_until="domcontentloaded")
    with allure.step("Открытие формы создания проекта"):
        dashboard_page.click_plus_button()
    with allure.step("Заполнение формы с неверным диапазоном дат"):
        project_name = "InvalidDate_" + datetime.now().strftime("%Y%m%d%H%M%S")
        project_page.fill_project_name(project_name)
        project_page.fill_description("Test with invalid date range")
        start_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        project_page.fill_start_date(start_date)
        end_date = datetime.now().strftime("%Y-%m-%d")
        project_page.fill_end_date(end_date)
        project_page.fill_status("In Progress")
    with allure.step("Отправка формы"):
        project_page.submit_create_project()
    with allure.step("Проверка отображения проекта"):
        page.wait_for_selector(f"text={project_name}", state="visible", timeout=5000)
        assert project_page.is_project_visible(project_name), "Проект с неверным диапазоном дат не отображается"
        logger.info(f"Проект {project_name} с End Date раньше Start Date создан")

@pytest.mark.projects
@allure.title("Открытие созданного проекта")
def test_open_created_project(page):
    auth_page = AuthenticationPage(page)
    dashboard_page = DashboardPage(page)
    project_page = ProjectPage(page)
    with allure.step("Переход на страницу авторизации"):
        auth_page.navigate()
    with allure.step("Вход в систему"):
        auth_page.login(EMAIL, PASSWORD)
    with allure.step("Переход на дашборд"):
        page.goto(f"{BASE_URL}/dashboard", wait_until="domcontentloaded")
    with allure.step("Открытие формы проекта"):
        dashboard_page.click_plus_button()
    with allure.step("Создание проекта для открытия"):
        project_name = "OpenTest_" + datetime.now().strftime("%Y%m%d%H%M%S")
        project_page.fill_project_name(project_name)
        project_page.fill_description("Test for opening")
        start_date = datetime.now().strftime("%Y-%m-%d")
        project_page.fill_start_date(start_date)
        end_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        project_page.fill_end_date(end_date)
        project_page.fill_status("In Progress")
        project_page.submit_create_project()
    with allure.step("Открытие созданного проекта"):
        dashboard_page.open_project(project_name)
    with allure.step("Проверка открытия"):
        assert dashboard_page.page.url.startswith(f"{BASE_URL}/projects/"), "Проект не открыт"
        logger.info(f"Проект {project_name} успешно открыт")

@pytest.mark.projects
@allure.title("Создание проекта с некорректной датой (с годом до 275757)")
def test_create_project_invalid_date(page):
    auth_page = AuthenticationPage(page)
    dashboard_page = DashboardPage(page)
    project_page = ProjectPage(page)
    with allure.step("Переход на страницу авторизации"):
        auth_page.navigate()
    with allure.step("Вход в систему"):
        auth_page.login(EMAIL, PASSWORD)
    with allure.step("Переход на дашборд"):
        page.goto(f"{BASE_URL}/dashboard", wait_until="domcontentloaded")
    with allure.step("Открытие формы создания проекта"):
        dashboard_page.click_plus_button()
    with allure.step("Заполнение формы с некорректной датой"):
        project_name = "InvalidDateTest_" + datetime.now().strftime("%Y%m%d%H%M%S")
        project_page.fill_project_name(project_name)
        project_page.fill_description("Test with invalid date")
        invalid_start_date = "275760-01-01"
        project_page.fill_start_date(invalid_start_date)
        end_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        project_page.fill_end_date(end_date)
        project_page.fill_status("In Progress")
    with allure.step("Отправка формы"):
        project_page.submit_create_project()
    with allure.step("Проверка отображения проекта"):
        page.wait_for_selector(f"text={project_name}", state="visible", timeout=5000)
        assert project_page.is_project_visible(project_name), "Проект с некорректной датой не отображается"
        logger.info(f"Проект {project_name} с некорректной датой {invalid_start_date} создан")