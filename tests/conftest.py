# tests/conftest.py
import pytest
import os
import requests
import json
import allure
from playwright.sync_api import Playwright, Page
from pages.authentication_page import AuthenticationPage
from pages.dashboard_page import DashboardPage
from settings import BASE_URL, EMAIL, PASSWORD
from utils.logger import logger

def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: mark test as smoke test")
    config.addinivalue_line("markers", "regression: mark test as regression test")
    config.addinivalue_line("markers", "auth: mark test as authentication test")
    config.addinivalue_line("markers", "projects: mark test as projects test")
    config.addinivalue_line("markers", "tasks: mark test as tasks test")
    config.addinivalue_line("markers", "navigation: mark test as navigation test")

@pytest.fixture(scope="session")
def browser(playwright: Playwright):
    headless = os.getenv("HEADLESS", "true").lower() == "true"
    logger.info(f"Запуск браузера Chromium в режиме headless={headless}")
    browser = playwright.chromium.launch(headless=headless)
    yield browser
    logger.info("Закрытие браузера")
    browser.close()

@pytest.fixture(scope="function")
def page(browser):
    logger.info("Создание новой страницы")
    context = browser.new_context()
    page = context.new_page()
    page.on("console", lambda msg: logger.info(f"Консоль браузера: {msg.text}"))
    page.on("request", lambda req: logger.info(f"Запрос: {req.method} {req.url}"))
    page.on("response", lambda res: logger.info(f"Ответ: {res.status} {res.url}"))
    yield page
    logger.info("Закрытие контекста страницы")
    context.close()

@pytest.fixture(scope="function")
def auth_page(page: Page):
    return AuthenticationPage(page)

@pytest.fixture(scope="function")
def authenticated_page(page: Page, auth_page):
    logger.info("Выполнение авторизации через UI для получения страницы дашборда")
    auth_page.navigate()
    dashboard = auth_page.login(os.getenv("EMAIL", "test@example.com"), os.getenv("PASSWORD", "password"))
    page.evaluate("window.localStorage.setItem('authToken', 'test-token')")
    yield page
    page.evaluate("window.localStorage.clear()")

@pytest.fixture(scope="function")
def authenticated_page_via_api(page: Page):
    logger.info("Получение токена через API и установка в localStorage")
    try:
        api_base_url = "http://localhost:8000"
        response = requests.post(
            f"{api_base_url}/api/auth/login",
            json={"email": EMAIL, "password": PASSWORD},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        response_data = response.json()
        logger.info(f"Ответ API: {json.dumps(response_data, indent=2)}")
        logger.info(f"Заголовки API: {json.dumps(dict(response.headers), indent=2)}")
        logger.info(f"Cookies API: {json.dumps(dict(response.cookies), indent=2)}")
        token = response_data.get("token")
        user = response_data.get("user")
        if not token or not user:
            logger.error("Токен или данные пользователя не получены из API")
            raise ValueError("Токен или данные пользователя не получены")
        logger.info("Токен и данные пользователя успешно получены")

        jwt_cookie = response.cookies.get("jwt")
        if jwt_cookie:
            page.context.add_cookies([{
                "name": "jwt",
                "value": jwt_cookie,
                "url": "http://localhost:3000",
                "sameSite": "None",
                "secure": True
            }])
            logger.info("Cookie jwt добавлено")
        else:
            logger.warning("Cookie jwt отсутствует в ответе API")

        page.goto(f"{BASE_URL}/dashboard", wait_until="networkidle")
        page.wait_for_url(f"{BASE_URL}/dashboard", timeout=30000)
        logger.info(f"Страница загружена: {page.url}")

        persist_root = {
            "global": json.dumps({
                "isSidebarOpen": True,
                "isModalOpen": False,
                "isTaskDetailsModalOpen": False,
                "task": None
            }),
            "auth": json.dumps({
                "user": user,
                "token": token
            }),
            "_persist": json.dumps({
                "version": -1,
                "rehydrated": True
            })
        }
        try:
            page.evaluate(f"window.localStorage.setItem('persist:root', '{json.dumps(persist_root)}')")
            logger.info("persist:root установлен в localStorage")
            local_storage = page.evaluate("window.localStorage.getItem('persist:root')")
            logger.info(f"Содержимое localStorage: {local_storage}")
        except Exception as e:
            logger.error(f"Ошибка при установке localStorage: {e}")
            page.screenshot(path="localstorage_error.png")
            allure.attach.file("localstorage_error.png", name="Скриншот ошибки localStorage", attachment_type=allure.attachment_type.PNG)
            raise

        page.reload(wait_until="networkidle")
        page.wait_for_url(f"{BASE_URL}/dashboard", timeout=30000)
        logger.info("Страница перезагружена")

        cookies = page.context.cookies()
        logger.info(f"Текущие cookies: {json.dumps(cookies, indent=2)}")

        page.screenshot(path="dashboard_after_auth.png")
        allure.attach.file("dashboard_after_auth.png", name="Скриншот дашборда после авторизации", attachment_type=allure.attachment_type.PNG)
    except Exception as e:
        logger.error(f"Ошибка при авторизации через API: {e}")
        page.screenshot(path="auth_error.png")
        allure.attach.file("auth_error.png", name="Скриншот ошибки авторизации", attachment_type=allure.attachment_type.PNG)
        raise
    yield page
    page.evaluate("window.localStorage.clear()")
    page.context.clear_cookies()

@pytest.fixture(scope="function")
def dashboard_page(authenticated_page_via_api):
    return DashboardPage(authenticated_page_via_api)