# tests/test_auth.py
import pytest
import allure
import os
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError, expect
from pages.authentication_page import AuthenticationPage
from pages.dashboard_page import DashboardPage
from utils.logger import logger
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture(scope="function")
def logged_in_page(authenticated_context):
    page = authenticated_context.new_page()
    dashboard_page = DashboardPage(page)
    dashboard_page.navigate_to(f"{dashboard_page.BASE_URL}/dashboard")
    with allure.step("Проверка загрузки дашборда после авторизации"):
        assert dashboard_page.is_loaded(), "Дашборд не загружен после API-авторизации"
        logger.info("Дашборд успешно загружен")
    yield dashboard_page
    page.close()

@pytest.mark.smoke
@pytest.mark.auth
@allure.title("Успешный вход")
def test_login_success(authenticated_context):
    page = authenticated_context.new_page()
    dashboard_page = DashboardPage(page)
    with allure.step("Переход на дашборд"):
        dashboard_page.navigate_to(f"{dashboard_page.BASE_URL}/dashboard")
    with allure.step("Проверка загрузки дашборда"):
        assert dashboard_page.is_loaded(), "Дашборд не загружен"
        try:
            page.wait_for_selector("h1, h2, div[class*='dashboard']", state="visible", timeout=10000)
            logger.info("Найден элемент дашборда")
            allure.attach(page.screenshot(), name="dashboard_success.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Элемент дашборда не найден: {e}")
            allure.attach(page.content(), name="dashboard_error.html", attachment_type=allure.attachment_type.HTML)
            raise
    page.close()

@pytest.mark.auth
@allure.title("Успешный выход")
def test_logout_success(logged_in_page: DashboardPage):
    with allure.step("Выполнение выхода"):
        try:
            auth_page = logged_in_page.logout()
        except PlaywrightTimeoutError as e:
            logger.error(f"Выход не удался: {e}")
            allure.attach(logged_in_page.page.content(), name="dashboard_error.html", attachment_type=allure.attachment_type.HTML)
            raise
    with allure.step("Проверка загрузки страницы авторизации"):
        try:
            assert auth_page.is_loaded(), f"Страница авторизации не загрузилась, текущий URL: {auth_page.page.url}"
            logger.info("Выход успешен")
            allure.attach(auth_page.page.screenshot(), name="post_logout.png", attachment_type=allure.attachment_type.PNG)
        except AssertionError as e:
            logger.error(f"Проверка не удалась: {e}")
            allure.attach(auth_page.page.content(), name="post_logout_error.html", attachment_type=allure.attachment_type.HTML)
            raise

@pytest.mark.auth
@pytest.mark.parametrize(
    "email, password, test_name",
    [
        (os.getenv("EMAIL", "ikra-nn@yandex.ru"), "wrong_password", "неверный пароль"),
        ("invalid-email@mail.ru", os.getenv("PASSWORD", "q1w2e3r4t5Y"), "неверный email"),
        ("", os.getenv("PASSWORD", "q1w2e3r4t5Y"), "пустой email"),
        (os.getenv("EMAIL", "ikra-nn@yandex.ru"), "", "пустой пароль"),
        ("a" * 256 + "@example.com", os.getenv("PASSWORD", "q1w2e3r4t5Y"), "длинный email"),
        (os.getenv("EMAIL", "ikra-nn@yandex.ru"), "a" * 101, "длинный пароль"),
    ],
    ids=["invalid_password", "invalid_email", "empty_email", "empty_password", "long_email", "long_password"]
)
@allure.title("Вход с некорректными данными: {test_name}")
def test_login_invalid_data(page: Page, email, password, test_name):
    auth_page = AuthenticationPage(page)
    with allure.step("Открытие страницы авторизации"):
        auth_page.navigate()
    with allure.step(f"Ввод данных: {test_name}"):
        auth_page.fill_email(email)
        auth_page.fill_password(password)
        auth_page.submit_login(expect_success=False)
    with allure.step("Проверка сообщения об ошибке"):
        try:
            auth_page.error_message.wait_for(state="visible", timeout=10000)
            error_text = auth_page.error_message.text_content()
            logger.info(f"Текст ошибки: {error_text}")
            assert auth_page.error_message.is_visible(), f"Сообщение об ошибке не отображено, текст: {error_text}"
            allure.attach(page.screenshot(), name=f"invalid_{test_name}.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Сообщение об ошибке не отображено: {e}")
            allure.attach(page.content(), name=f"invalid_{test_name}_error.html", attachment_type=allure.attachment_type.HTML)
            raise

@pytest.mark.auth
@allure.title("Отображение формы авторизации")
def test_authentication_form_displayed(page: Page):
    auth_page = AuthenticationPage(page)
    with allure.step("Открытие страницы авторизации"):
        auth_page.navigate()
    with allure.step("Проверка контейнера формы"):
        form = auth_page.page.locator("form.mt-6.space-y-4")
        try:
            form.wait_for(state="visible", timeout=10000)
            logger.info("Контейнер формы авторизации виден")
            allure.attach(page.screenshot(), name="auth_form_container.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Контейнер формы не виден: {e}")
            allure.attach(page.content(), name="form_container_error.html", attachment_type=allure.attachment_type.HTML)
            raise
    with allure.step("Проверка элементов формы"):
        try:
            expect(auth_page.email_input).to_be_visible(timeout=10000)
            assert auth_page.email_input.get_attribute("type") == "email", "Тип поля email не 'email'"
            expect(auth_page.password_input).to_be_visible(timeout=10000)
            assert auth_page.password_input.get_attribute("type") == "password", "Тип поля пароля не 'password'"
            expect(auth_page.submit_button).to_be_visible(timeout=10000)
            button_text = auth_page.submit_button.text_content().strip()
            assert button_text == "Sign In", f"Текст кнопки не 'Sign In', получено '{button_text}'"
            logger.info("Элементы формы авторизации корректно отображены")
            allure.attach(page.screenshot(), name="auth_form_elements.png", attachment_type=allure.attachment_type.PNG)
        except (AssertionError, PlaywrightTimeoutError) as e:
            logger.error(f"Проверка элементов формы не удалась: {e}")
            allure.attach(page.content(), name="auth_form_error.html", attachment_type=allure.attachment_type.HTML)
            raise

@pytest.mark.auth
@allure.title("Вход после десяти неудачных попыток")
def test_login_block_after_attempts(page: Page):
    auth_page = AuthenticationPage(page)
    with allure.step("Открытие страницы авторизации"):
        auth_page.navigate()
    with allure.step("Выполнение десяти неудачных попыток входа"):
        for i in range(10):
            auth_page.fill_email(os.getenv("EMAIL", "ikra-nn@yandex.ru"))
            auth_page.fill_password("wrongpass")
            auth_page.submit_login(expect_success=False)
            try:
                auth_page.error_message.wait_for(state="visible", timeout=10000)
                error_text = auth_page.error_message.text_content()
                logger.info(f"Текст ошибки после попытки {i+1}: {error_text}")
                allure.attach(page.screenshot(), name=f"failed_attempt_{i+1}.png", attachment_type=allure.attachment_type.PNG)
            except PlaywrightTimeoutError as e:
                logger.error(f"Сообщение об ошибке не отображено после попытки {i+1}: {e}")
                allure.attach(page.content(), name=f"failed_attempt_{i+1}_error.html", attachment_type=allure.attachment_type.HTML)
                raise
    with allure.step("Попытка входа с правильным паролем"):
        dashboard_page = auth_page.login(os.getenv("EMAIL", "ikra-nn@yandex.ru"), os.getenv("PASSWORD", "q1w2e3r4t5Y"))
    with allure.step("Проверка успешного входа"):
        try:
            assert dashboard_page.is_loaded(), f"Дашборд не загружен после корректного входа, текущий URL: {dashboard_page.page.url}"
            logger.info("Вход успешен после десяти неудачных попыток")
            allure.attach(page.screenshot(), name="successful_login.png", attachment_type=allure.attachment_type.PNG)
        except AssertionError as e:
            logger.error(f"Вход не удался: {e}")
            allure.attach(page.content(), name="login_failure.html", attachment_type=allure.attachment_type.HTML)
            raise