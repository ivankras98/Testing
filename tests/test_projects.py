# test_projects.py
import pytest
import allure
from pages.project_page import ProjectPage
from playwright.sync_api import Page


@pytest.mark.smoke
@pytest.mark.projects
@allure.title("Проверка создания нового проекта")
@allure.description("Проверяет успешное создание нового проекта на странице /projects с отображением созданного проекта.")
def test_create_project(page: Page):
    project_name = "Test Project"
    with allure.step("Открыть страницу создания проекта"):
        project_page = ProjectPage(page).navigate()
    with allure.step("Ввести название проекта"):
        project_page.enter_project_name(project_name)
    with allure.step("Нажать кнопку 'Создать'"):
        project_page.click_create()
    with allure.step("Проверить отображение созданного проекта"):
        assert project_page.is_project_visible(project_name), "Созданный проект не отображается"