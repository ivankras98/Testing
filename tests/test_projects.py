import allure
from pages.projects_page import ProjectsPage
from utils.logger import logger

@allure.title("Проверка создания нового проекта")
@allure.description("Проверяет создание нового проекта через форму в разделе MY PROJECTS.")
def test_create_project(logged_in_page):
    projects_page = ProjectsPage(logged_in_page.page)
    projects_page.open_create_project_form()
    project_name = "Test Project"
    projects_page.fill_create_project_form(
        name=project_name,
        description="Description for Test Project",
        start_date="01.04.2025",
        end_date="30.04.2025",
        status="Active"
    )
    projects_page.submit_create_project_form()
    assert not projects_page.project_name_input.is_visible(), "Форма создания проекта не закрылась после отправки"
    try:
        projects_page.page.wait_for_selector(f"text={project_name}", timeout=10000)
        logger.info(f"Проект '{project_name}' отображается в списке")
    except Exception as e:
        logger.error(f"Проект '{project_name}' не найден в списке: {e}")
        projects_page.take_screenshot("project_list_error.png")
        allure.attach.file("project_list_error.png", name="Скриншот ошибки списка проектов", attachment_type=allure.attachment_type.PNG)
        raise