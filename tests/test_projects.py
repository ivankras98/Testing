import allure
from pages.projects_page import ProjectsPage
from utils.logger import logger

@allure.title("Проверка создания проекта")
@allure.description("Тестирует создание нового проекта через кнопку 'Создать проект' с заполнением формы.")
def test_create_project(logged_in_page):
    # Создаём объект ProjectsPage напрямую, используя Playwright Page из logged_in_page
    projects_page = ProjectsPage(logged_in_page.page)
    # Переходим на страницу дашборда через метод navigate() в ProjectsPage
    projects_page.navigate()
    projects_page.open_sidebar()
    projects_page.open_create_project_form()
    projects_page.fill_create_project_form(
        name="Test Project",
        description="Test description",
        start_date="2025-05-01",  # Формат YYYY-MM-DD для input type="date"
        end_date="2025-05-31",    # Формат YYYY-MM-DD для input type="date"
        status="In Progress"
    )
    projects_page.submit_create_project_form()
    assert projects_page.is_project_created(), "Проект не был создан"
    logger.info("Проект успешно создан и проверен")