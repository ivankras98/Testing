# tests/test_projects.py
import pytest
import allure
from pages.project_page import ProjectPage
from playwright.sync_api import Page

@pytest.mark.smoke
@pytest.mark.feature("projects")
@allure.title("Проверка создания проекта")
@allure.description("Проверяет создание нового проекта на странице /projects.")
def test_create_project(page: Page):
    with allure.step("Открыть страницу проектов с помощью метода navigate()"):
        project_page = ProjectPage(page).navigate()
    with allure.step("Ввести название 'Test Project' в поле 'input[name='projectName']'"):
        project_page.enter_project_name("Test Project")
    with allure.step("Нажать кнопку 'Создать' с селектором 'button[type='submit']'"):
        project_page.click_create()
    with allure.step("Проверить, что отображается проект 'Test Project'"):
        assert project_page.is_project_visible("Test Project"), "Проект не отображается"