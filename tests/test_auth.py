import pytest
import allure
from pages.authentication_page import AuthenticationPage
from pages.dashboard_page import DashboardPage
from settings import BASE_URL, EMAIL, PASSWORD
from utils.logger import logger
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

@pytest.fixture(scope="function")
def logged_in_page(page: Page) -> DashboardPage:
    with allure.step("Authenticate user"):
        auth_page = AuthenticationPage(page).navigate()
        dashboard_page = auth_page.login(EMAIL, PASSWORD, expect_success=True)
        if not dashboard_page.is_loaded():
            logger.error("Dashboard page not loaded after login")
            allure.attach(page.content(), name="page_content", attachment_type=allure.attachment_type.HTML)
            raise AssertionError("Dashboard not loaded")
        yield dashboard_page

@pytest.mark.smoke
@pytest.mark.auth
@allure.title("Successful login")
def test_login_success(page: Page):
    with allure.step("Open authentication page"):
        auth_page = AuthenticationPage(page).navigate()
    with allure.step("Enter email and password"):
        auth_page.fill_email(EMAIL)
        auth_page.fill_password(PASSWORD)
    with allure.step("Submit login"):
        dashboard_page = auth_page.submit_login(expect_success=True)
    with allure.step("Verify dashboard load"):
        assert dashboard_page.is_loaded(), "Dashboard not loaded"
        try:
            page.wait_for_selector("h1, h2, div[class*='dashboard']", state="visible", timeout=10000)
            logger.info("Found dashboard-specific element")
            allure.attach(page.content(), name="dashboard_success.html", attachment_type=allure.attachment_type.HTML)
        except PlaywrightTimeoutError as e:
            logger.error(f"Dashboard element not found: {e}")
            allure.attach(page.content(), name="page.html", attachment_type=allure.attachment_type.HTML)
            raise

@pytest.mark.auth
@allure.title("Successful logout")
def test_logout_success(logged_in_page: DashboardPage):
    with allure.step("Perform logout"):
        try:
            auth_page = logged_in_page.logout()
        except PlaywrightTimeoutError as e:
            logger.error(f"Logout failed: {e}")
            allure.attach(
                logged_in_page.page.content(),
                name="dashboard.html",
                attachment_type=allure.attachment_type.HTML,
            )
            raise
    with allure.step("Verify authentication page load"):
        try:
            assert auth_page.is_loaded(), f"Authentication page not loaded, current URL: {logged_in_page.page.url}"
            logger.info("Logout successful")
        except AssertionError as e:
            logger.error(f"Verification failed: {e}")
            allure.attach(logged_in_page.page.content(), name="post_logout.html", attachment_type=allure.attachment_type.HTML)
            raise

@pytest.mark.auth
@allure.title("Login with invalid password")
def test_login_invalid_password(page: Page):
    with allure.step("Open authentication page"):
        auth_page = AuthenticationPage(page).navigate()
    with allure.step("Enter invalid password"):
        auth_page.fill_email(EMAIL)
        auth_page.fill_password("wrong_password")
        auth_page.submit_login(expect_success=False)
    with allure.step("Verify error message"):
        try:
            auth_page.error_message.wait_for(state="visible", timeout=10000)
            error_text = auth_page.error_message.text_content()
            logger.info(f"Error message text: {error_text}")
            assert auth_page.error_message.is_visible(), f"Error message not displayed, found text: {error_text}"
        except PlaywrightTimeoutError as e:
            logger.error(f"Error message not displayed: {e}")
            allure.attach(page.content(), name="invalid_password.html", attachment_type=allure.attachment_type.HTML)
            raise

@pytest.mark.auth
@allure.title("Login with invalid email")
def test_login_invalid_email(page: Page):
    with allure.step("Open authentication page"):
        auth_page = AuthenticationPage(page).navigate()
    with allure.step("Enter invalid email"):
        auth_page.fill_email("invalid-email@mail.ru")
        auth_page.fill_password(PASSWORD)
        auth_page.submit_login(expect_success=False)
    with allure.step("Verify error message"):
        try:
            auth_page.error_message.wait_for(state="visible", timeout=10000)
            error_text = auth_page.error_message.text_content()
            logger.info(f"Error message text: {error_text}")
            assert auth_page.error_message.is_visible(), f"Error message not displayed, found text: {error_text}"
        except PlaywrightTimeoutError as e:
            logger.error(f"Error message not displayed: {e}")
            allure.attach(page.content(), name="invalid_email.html", attachment_type=allure.attachment_type.HTML)
            raise

@pytest.mark.auth
@allure.title("Login with empty email")
def test_login_empty_email(page: Page):
    with allure.step("Open authentication page"):
        auth_page = AuthenticationPage(page).navigate()
    with allure.step("Leave email empty"):
        auth_page.fill_email("")
        auth_page.fill_password(PASSWORD)
        auth_page.submit_login(expect_success=False)
    with allure.step("Verify error message"):
        try:
            auth_page.error_message.wait_for(state="visible", timeout=10000)
            error_text = auth_page.error_message.text_content()
            logger.info(f"Error message text: {error_text}")
            assert auth_page.error_message.is_visible(), f"Error message not displayed, found text: {error_text}"
        except PlaywrightTimeoutError as e:
            logger.error(f"Error message not displayed: {e}")
            allure.attach(page.content(), name="empty_email.html", attachment_type=allure.attachment_type.HTML)
            raise

@pytest.mark.auth
@allure.title("Login with empty password")
def test_login_empty_password(page: Page):
    with allure.step("Open authentication page"):
        auth_page = AuthenticationPage(page).navigate()
    with allure.step("Leave password empty"):
        auth_page.fill_email(EMAIL)
        auth_page.fill_password("")
        auth_page.submit_login(expect_success=False)
    with allure.step("Verify error message"):
        try:
            auth_page.error_message.wait_for(state="visible", timeout=10000)
            error_text = auth_page.error_message.text_content()
            logger.info(f"Error message text: {error_text}")
            assert auth_page.error_message.is_visible(), f"Error message not displayed, found text: {error_text}"
        except PlaywrightTimeoutError as e:
            logger.error(f"Error message not displayed: {e}")
            allure.attach(page.content(), name="empty_password.html", attachment_type=allure.attachment_type.HTML)
            raise

@pytest.mark.auth
@allure.title("Login with long email")
def test_login_long_email(page: Page):
    with allure.step("Open authentication page"):
        auth_page = AuthenticationPage(page).navigate()
    with allure.step("Enter long email"):
        long_email = "a" * 256 + "@example.com"
        auth_page.fill_email(long_email)
        auth_page.fill_password(PASSWORD)
        auth_page.submit_login(expect_success=False)
    with allure.step("Verify error message"):
        try:
            auth_page.error_message.wait_for(state="visible", timeout=10000)
            error_text = auth_page.error_message.text_content()
            logger.info(f"Error message text: {error_text}")
            assert auth_page.error_message.is_visible(), f"Error message not displayed, found text: {error_text}"
        except PlaywrightTimeoutError as e:
            logger.error(f"Error message not displayed: {e}")
            allure.attach(page.content(), name="long_email.html", attachment_type=allure.attachment_type.HTML)
            raise

@pytest.mark.auth
@allure.title("Login with long password")
def test_login_long_password(page: Page):
    with allure.step("Open authentication page"):
        auth_page = AuthenticationPage(page).navigate()
    with allure.step("Enter long password"):
        long_pass = "a" * 101
        auth_page.fill_email(EMAIL)
        auth_page.fill_password(long_pass)
        auth_page.submit_login(expect_success=False)
    with allure.step("Verify error message"):
        try:
            auth_page.error_message.wait_for(state="visible", timeout=10000)
            error_text = auth_page.error_message.text_content()
            logger.info(f"Error message text: {error_text}")
            assert auth_page.error_message.is_visible(), f"Error message not displayed, found text: {error_text}"
        except PlaywrightTimeoutError as e:
            logger.error(f"Error message not displayed: {e}")
            allure.attach(page.content(), name="long_password.html", attachment_type=allure.attachment_type.HTML)
            raise

@pytest.mark.auth
@allure.title("Authentication form is displayed")
def test_authentication_form_displayed(page: Page):
    with allure.step("Open authentication page"):
        auth_page = AuthenticationPage(page).navigate()
    with allure.step("Verify form container"):
        form = page.locator("form.mt-6.space-y-4")
        try:
            form.wait_for(state="visible", timeout=10000)
            logger.info("Authentication form container is visible")
        except PlaywrightTimeoutError as e:
            logger.error(f"Form container not visible: {e}")
            allure.attach(page.content(), name="form_container_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(page.screenshot(), name="form_container_error.png", attachment_type=allure.attachment_type.PNG)
            raise
    with allure.step("Verify form elements"):
        try:
            auth_page.email_input.wait_for(state="visible", timeout=10000)
            assert auth_page.email_input.is_visible(), "Email input not visible"
            assert auth_page.email_input.get_attribute("type") == "email", "Email input type is not 'email'"
            auth_page.password_input.wait_for(state="visible", timeout=10000)
            assert auth_page.password_input.is_visible(), "Password input not visible"
            assert auth_page.password_input.get_attribute("type") == "password", "Password input type is not 'password'"
            auth_page.submit_button.wait_for(state="visible", timeout=10000)
            assert auth_page.submit_button.is_visible(), "Submit button not visible"
            button_text = auth_page.submit_button.text_content().strip()
            assert button_text == "Sign In", f"Submit button text is not 'Sign In', got '{button_text}'"
            logger.info("Authentication form elements are displayed correctly")
            allure.attach(page.screenshot(), name="auth_form_screenshot.png", attachment_type=allure.attachment_type.PNG)
        except (AssertionError, PlaywrightTimeoutError) as e:
            logger.error(f"Form elements verification failed: {e}")
            allure.attach(page.content(), name="auth_form_error.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(page.screenshot(), name="auth_form_error.png", attachment_type=allure.attachment_type.PNG)
            raise

@pytest.mark.auth
@allure.title("Login after ten failed attempts")
def test_login_block_after_attempts(page: Page):
    with allure.step("Open authentication page"):
        auth_page = AuthenticationPage(page).navigate()
    with allure.step("Perform ten failed login attempts"):
        for i in range(10):
            auth_page.fill_email(EMAIL)
            auth_page.fill_password("wrongpass")
            auth_page.submit_login(expect_success=False)
            try:
                auth_page.error_message.wait_for(state="visible", timeout=10000)
                error_text = auth_page.error_message.text_content()
                logger.info(f"Error message after attempt {i+1}: {error_text}")
            except PlaywrightTimeoutError as e:
                logger.error(f"Error message not displayed after attempt {i+1}: {e}")
                allure.attach(page.content(), name=f"failed_attempt_{i+1}.html", attachment_type=allure.attachment_type.HTML)
                raise
    with allure.step("Attempt login with correct password"):
        auth_page.fill_email(EMAIL)
        auth_page.fill_password(PASSWORD)
        dashboard_page = auth_page.submit_login(expect_success=True)
    with allure.step("Verify successful login"):
        try:
            assert dashboard_page.is_loaded(), f"Dashboard not loaded after correct login, current URL: {page.url}"
            logger.info("Login successful after ten failed attempts")
            allure.attach(page.content(), name="successful_login.html", attachment_type=allure.attachment_type.HTML)
        except AssertionError as e:
            logger.error(f"Login failed: {e}")
            allure.attach(page.content(), name="login_failure.html", attachment_type=allure.attachment_type.HTML)
            allure.attach(page.screenshot(), name="login_failure.png", attachment_type=allure.attachment_type.PNG)
            raise