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
    with allure.step("Открыть дашборд"):
        dashboard_page.navigate_to(f"{dashboard_page.BASE_URL}/dashboard")
    with allure.step("Проверить загрузку дашборда"):
        assert dashboard_page.is_loaded(), "Дашборд не загружен после авторизации"
        logger.info("Дашборд успешно загружен")
    yield dashboard_page
    page.close()


@pytest.mark.smoke
@pytest.mark.auth
@allure.title("Успешный вход")
def test_login_success(authenticated_context):
    page = authenticated_context.new_page()
    dashboard_page = DashboardPage(page)
    with allure.step("Открыть дашборд"):
        dashboard_page.navigate_to(f"{dashboard_page.BASE_URL}/dashboard")
    with allure.step("Проверить загрузку дашборда"):
        assert dashboard_page.is_loaded(), "Дашборд не загружен"
        try:
            page.wait_for_selector("h1, h2, div[class*='dashboard']", state="visible", timeout=10000)
            logger.info("Найден элемент дашборда")
            allure.attach(page.screenshot(), name="дашборд_успешно.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Элемент дашборда не найден: {e}")
            allure.attach(page.content(), name="дашборд_ошибка.html", attachment_type=allure.attachment_type.HTML)
            raise
    page.close()


@pytest.mark.auth
@pytest.mark.regression
@allure.title("Успешный выход")
def test_logout_success(logged_in_page: DashboardPage):
    with allure.step("Выполнить выход"):
        try:
            auth_page = logged_in_page.logout()
        except PlaywrightTimeoutError as e:
            logger.error(f"Выход не удался: {e}")
            allure.attach(logged_in_page.page.content(), name="дашборд_ошибка.html", attachment_type=allure.attachment_type.HTML)
            raise
    with allure.step("Проверить загрузку страницы авторизации"):
        try:
            assert auth_page.is_loaded(), f"Страница авторизации не загрузилась, текущий URL: {auth_page.page.url}"
            logger.info("Выход успешен")
            allure.attach(auth_page.page.screenshot(), name="страница_после_выхода.png", attachment_type=allure.attachment_type.PNG)
        except AssertionError as e:
            logger.error(f"Проверка не удалась: {e}")
            allure.attach(auth_page.page.content(), name="ошибка_после_выхода.html", attachment_type=allure.attachment_type.HTML)
            raise


@pytest.mark.auth
@pytest.mark.regression
@pytest.mark.parametrize(
    "email, password, test_name",
    [
        (os.getenv("EMAIL"), "wrong_password", "неверный пароль"),
        ("invalid-email@mail.ru", os.getenv("PASSWORD"), "неверный email"),
        ("", os.getenv("PASSWORD"), "пустой email"),
        (os.getenv("EMAIL"), "", "пустой пароль"),
        ("a" * 256 + "@example.com", os.getenv("PASSWORD"), "длинный email"),
        (os.getenv("EMAIL"), "a" * 101, "длинный пароль"),
    ],
    ids=["invalid_password", "invalid_email", "empty_email", "empty_password", "long_email", "long_password"]
)
@allure.title("Вход с некорректными данными: {test_name}")
def test_login_invalid_data(page: Page, email, password, test_name):
    auth_page = AuthenticationPage(page)
    with allure.step("Открыть страницу авторизации"):
        auth_page.navigate()
    with allure.step(f"Ввести данные: {test_name}"):
        auth_page.fill_email(email)
        auth_page.fill_password(password)
        auth_page.submit_login(expect_success=False)
    with allure.step("Проверить сообщение об ошибке"):
        try:
            auth_page.error_message.wait_for(state="visible", timeout=10000)
            error_text = auth_page.error_message.text_content()
            logger.info(f"Текст ошибки: {error_text}")
            assert auth_page.error_message.is_visible(), f"Сообщение об ошибке не отображено, текст: {error_text}"
            allure.attach(page.screenshot(), name=f"ошибка_{test_name}.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Сообщение об ошибке не отображено: {e}")
            allure.attach(page.content(), name=f"ошибка_{test_name}.html", attachment_type=allure.attachment_type.HTML)
            raise


@pytest.mark.auth
@pytest.mark.regression
@allure.title("Отображение формы авторизации")
def test_authentication_form_displayed(page: Page):
    auth_page = AuthenticationPage(page)
    with allure.step("Открыть страницу авторизации"):
        auth_page.navigate()
    with allure.step("Проверить контейнер формы"):
        form = auth_page.page.locator("form.mt-6.space-y-4")
        try:
            form.wait_for(state="visible", timeout=10000)
            logger.info("Контейнер формы авторизации виден")
            allure.attach(page.screenshot(), name="контейнер_формы_авторизации.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Контейнер формы не виден: {e}")
            allure.attach(page.content(), name="ошибка_контейнера_формы.html", attachment_type=allure.attachment_type.HTML)
            raise
    with allure.step("Проверить элементы формы"):
        try:
            expect(auth_page.email_input).to_be_visible(timeout=10000)
            assert auth_page.email_input.get_attribute("type") == "email", "Тип поля email не 'email'"
            expect(auth_page.password_input).to_be_visible(timeout=10000)
            assert auth_page.password_input.get_attribute("type") == "password", "Тип поля пароля не 'password'"
            expect(auth_page.submit_button).to_be_visible(timeout=10000)
            button_text = auth_page.submit_button.text_content().strip()
            assert button_text == "Sign In", f"Текст кнопки не 'Sign In', получено '{button_text}'"
            logger.info("Элементы формы авторизации корректно отображены")
            allure.attach(page.screenshot(), name="элементы_формы_авторизации.png", attachment_type=allure.attachment_type.PNG)
        except (AssertionError, PlaywrightTimeoutError) as e:
            logger.error(f"Проверка элементов формы не удалась: {e}")
            allure.attach(page.content(), name="ошибка_формы_авторизации.html", attachment_type=allure.attachment_type.HTML)
            raise


@pytest.mark.auth
@pytest.mark.regression
@allure.title("Вход после десяти неудачных попыток")
def test_login_block_after_attempts(page: Page):
    auth_page = AuthenticationPage(page)
    with allure.step("Открыть страницу авторизации"):
        auth_page.navigate()
    with allure.step("Выполнить десять неудачных попыток входа"):
        for i in range(10):
            auth_page.fill_email(os.getenv("EMAIL", "ikra-nn@yandex.ru"))
            auth_page.fill_password("wrongpass")
            auth_page.submit_login(expect_success=False)
            try:
                auth_page.error_message.wait_for(state="visible", timeout=10000)
                error_text = auth_page.error_message.text_content()
                logger.info(f"Текст ошибки после попытки {i+1}: {error_text}")
                allure.attach(page.screenshot(), name=f"неудачная_попытка_{i+1}.png", attachment_type=allure.attachment_type.PNG)
            except PlaywrightTimeoutError as e:
                logger.error(f"Сообщение об ошибке не отображено после попытки {i+1}: {e}")
                allure.attach(page.content(), name=f"ошибка_попытки_{i+1}.html", attachment_type=allure.attachment_type.HTML)
                raise
    with allure.step("Ввести корректные данные для входа"):
        dashboard_page = auth_page.login(os.getenv("EMAIL"), os.getenv("PASSWORD"))
    with allure.step("Проверить успешный вход"):
        try:
            assert dashboard_page.is_loaded(), f"Дашборд не загружен после корректного входа, текущий URL: {dashboard_page.page.url}"
            logger.info("Вход успешен после десяти неудачных попыток")
            allure.attach(page.screenshot(), name="успешный_вход.png", attachment_type=allure.attachment_type.PNG)
        except AssertionError as e:
            logger.error(f"Вход не удался: {e}")
            allure.attach(page.content(), name="ошибка_входа.html", attachment_type=allure.attachment_type.HTML)
            raise


@pytest.mark.auth
@pytest.mark.regression
@allure.title("Отображение формы регистрации")
def test_signup_form_displayed(page: Page):
    auth_page = AuthenticationPage(page)
    with allure.step("Открыть страницу авторизации"):
        auth_page.navigate()
    with allure.step("Открыть форму регистрации"):
        auth_page.open_signup_form()
    with allure.step("Проверить видимость заголовка формы регистрации"):
        try:
            expect(auth_page.signup_header).to_be_visible(timeout=10000)
            logger.info("Заголовок формы регистрации 'Sign Up' отображен")
            allure.attach(page.screenshot(), name="signup_form_header.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Заголовок формы регистрации не отображен: {e}")
            allure.attach(page.content(), name="signup_form_header_error.html", attachment_type=allure.attachment_type.HTML)
            raise

@pytest.mark.auth
@pytest.mark.regression
@allure.title("Проверка ошибки при пустых полях регистрации")
def test_signup_empty_fields(page: Page):
    auth_page = AuthenticationPage(page)
    with allure.step("Открыть страницу авторизации"):
        auth_page.navigate()
    with allure.step("Открыть форму регистрации"):
        auth_page.open_signup_form()
    with allure.step("Нажать на кнопку Sign Up с пустыми полями"):
        auth_page.submit_signup(expect_success=False)
    with allure.step("Проверить сообщение об ошибке"):
        try:
            auth_page.signup_error_message.wait_for(state="visible", timeout=10000)
            error_text = auth_page.signup_error_message.text_content()
            assert "All fields are required" in error_text, f"Ожидалось сообщение 'All fields are required', получено: {error_text}"
            logger.info(f"Сообщение об ошибке: {error_text}")
            allure.attach(page.screenshot(), name="signup_empty_fields_error.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Сообщение об ошибке не отображено: {e}")
            allure.attach(page.content(), name="signup_empty_fields_error.html", attachment_type=allure.attachment_type.HTML)
            raise

@pytest.mark.auth
@pytest.mark.regression
@allure.title("Успешная регистрация с корректными данными")
def test_signup_success(page: Page):
    auth_page = AuthenticationPage(page)
    name = auth_page.generate_random_name()
    email = auth_page.generate_random_email()
    phone = auth_page.generate_random_phone()
    password = "q1w2e3r4t5Y"
    with allure.step("Открыть страницу авторизации"):
        auth_page.navigate()
    with allure.step("Открыть форму регистрации"):
        auth_page.open_signup_form()
    with allure.step("Заполнить форму регистрации"):
        auth_page.signup(name, email, phone, password, password, expect_success=True)
    with allure.step("Проверить переход на дашборд"):
        dashboard_page = DashboardPage(page)
        try:
            assert dashboard_page.is_loaded(), f"Дашборд не загружен после регистрации, текущий URL: {page.url}"
            logger.info("Успешная регистрация и переход на дашборд")
            allure.attach(page.screenshot(), name="signup_success.png", attachment_type=allure.attachment_type.PNG)
        except AssertionError as e:
            logger.error(f"Переход на дашборд не удался: {e}")
            allure.attach(page.content(), name="signup_success_error.html", attachment_type=allure.attachment_type.HTML)
            raise

@pytest.mark.auth
@pytest.mark.regression
@allure.title("Регистрация с длинным именем")
def test_signup_long_name(page: Page):
    auth_page = AuthenticationPage(page)
    name = auth_page.generate_random_name(length=100)
    email = auth_page.generate_random_email()
    phone = auth_page.generate_random_phone()
    password = "q1w2e3r4t5Y"
    with allure.step("Открыть страницу авторизации"):
        auth_page.navigate()
    with allure.step("Открыть форму регистрации"):
        auth_page.open_signup_form()
    with allure.step("Заполнить форму регистрации с длинным именем"):
        auth_page.signup(name, email, phone, password, password, expect_success=True)
    with allure.step("Проверить переход на дашборд"):
        dashboard_page = DashboardPage(page)
        try:
            assert dashboard_page.is_loaded(), f"Дашборд не загружен после регистрации, текущий URL: {page.url}"
            logger.info("Успешная регистрация с длинным именем")
            allure.attach(page.screenshot(), name="signup_long_name.png", attachment_type=allure.attachment_type.PNG)
        except AssertionError as e:
            logger.error(f"Переход на дашборд не удался: {e}")
            allure.attach(page.content(), name="signup_long_name_error.html", attachment_type=allure.attachment_type.HTML)
            raise

@pytest.mark.auth
@pytest.mark.regression
@allure.title("Регистрация с некорректным номером телефона (буквы)")
def test_signup_invalid_phone_letters(page: Page):
    auth_page = AuthenticationPage(page)
    name = auth_page.generate_random_name()
    email = auth_page.generate_random_email()
    phone = "89abcdefghi"
    password = "q1w2e3r4t5Y"
    with allure.step("Открыть страницу авторизации"):
        auth_page.navigate()
    with allure.step("Открыть форму регистрации"):
        auth_page.open_signup_form()
    with allure.step("Заполнить форму регистрации с буквами в номере телефона"):
        auth_page.signup(name, email, phone, password, password, expect_success=False)
    with allure.step("Проверить отсутствие перехода на дашборд"):
        try:
            assert not page.url.endswith("/dashboard"), f"Неожиданный переход на дашборд, текущий URL: {page.url}"
            logger.info("Регистрация не выполнена из-за некорректного номера телефона")
            allure.attach(page.screenshot(), name="signup_invalid_phone_letters.png", attachment_type=allure.attachment_type.PNG)
        except AssertionError as e:
            logger.error(f"Неожиданный переход на дашборд: {e}")
            allure.attach(page.content(), name="signup_invalid_phone_letters_error.html", attachment_type=allure.attachment_type.HTML)
            raise

@pytest.mark.auth
@pytest.mark.regression
@allure.title("Регистрация с длинным номером телефона")
def test_signup_long_phone(page: Page):
    auth_page = AuthenticationPage(page)
    name = auth_page.generate_random_name()
    email = auth_page.generate_random_email()
    phone = "89" + "1" * 10
    password = "q1w2e3r4t5Y"
    with allure.step("Открыть страницу авторизации"):
        auth_page.navigate()
    with allure.step("Открыть форму регистрации"):
        auth_page.open_signup_form()
    with allure.step("Заполнить форму регистрации с длинным номером телефона"):
        auth_page.signup(name, email, phone, password, password, expect_success=False)
    with allure.step("Проверить отсутствие перехода на дашборд"):
        try:
            assert not page.url.endswith("/dashboard"), f"Неожиданный переход на дашборд, текущий URL: {page.url}"
            logger.info("Регистрация не выполнена из-за длинного номера телефона")
            allure.attach(page.screenshot(), name="signup_long_phone.png", attachment_type=allure.attachment_type.PNG)
        except AssertionError as e:
            logger.error(f"Неожиданный переход на дашборд: {e}")
            allure.attach(page.content(), name="signup_long_phone_error.html", attachment_type=allure.attachment_type.HTML)
            raise

@pytest.mark.auth
@pytest.mark.regression
@allure.title("Регистрация с несовпадающими паролями")
def test_signup_password_mismatch(page: Page):
    auth_page = AuthenticationPage(page)
    name = auth_page.generate_random_name()
    email = auth_page.generate_random_email()
    phone = auth_page.generate_random_phone()
    password = "q1w2e3r4t5Y"
    confirm_password = "different_password"
    with allure.step("Открыть страницу авторизации"):
        auth_page.navigate()
    with allure.step("Открыть форму регистрации"):
        auth_page.open_signup_form()
    with allure.step("Заполнить форму регистрации с несовпадающими паролями"):
        auth_page.signup(name, email, phone, password, confirm_password, expect_success=False)
    with allure.step("Проверить сообщение об ошибке"):
        try:
            auth_page.signup_error_message.wait_for(state="visible", timeout=10000)
            error_text = auth_page.signup_error_message.text_content()
            assert "Passwords do not match" in error_text, f"Ожидалось сообщение 'Passwords do not match', получено: {error_text}"
            logger.info(f"Сообщение об ошибке: {error_text}")
            allure.attach(page.screenshot(), name="signup_password_mismatch_error.png", attachment_type=allure.attachment_type.PNG)
        except PlaywrightTimeoutError as e:
            logger.error(f"Сообщение об ошибке не отображено: {e}")
            allure.attach(page.content(), name="signup_password_mismatch_error.html", attachment_type=allure.attachment_type.HTML)
            raise