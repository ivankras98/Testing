import pytest
import allure
from pages.project_page import ProjectPage
from pages.dashboard_page import DashboardPage

@pytest.mark.smoke
@pytest.mark.projects
@allure.title("Проверка создания нового проекта")
@allure.description("Проверяет успешное создание нового проекта на странице /dashboard с заполнением всех полей и отображением проекта.")
def test_create_project(logged_in_page: DashboardPage):
    project_page = ProjectPage(logged_in_page.page)  # Используем страницу из logged_in_page
    with allure.step("Открыть страницу дашборда"):
        project_page.navigate()
    with allure.step("Открыть форму создания проекта"):
        project_page.open_create_project_form()
    with allure.step("Ввести название проекта"):
        project_name = project_page.fill_project_name()
    with allure.step("Ввести описание проекта"):
        project_page.fill_description()
    with allure.step("Ввести дату начала проекта"):
        start_date = project_page.fill_start_date()
    with allure.step("Ввести дату окончания проекта"):
        project_page.fill_end_date(start_date)
    with allure.step("Выбрать статус проекта"):
        project_page.fill_status()
    with allure.step("Нажать кнопку 'Create'"):
        project_page.submit_create_project()
    with allure.step("Проверить отображение созданного проекта"):
        assert project_page.is_project_visible(project_name), "Созданный проект не отображается"