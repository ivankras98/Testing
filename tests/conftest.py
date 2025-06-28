# tests/conftest.py
import pytest
import requests
import os
import json
from dotenv import load_dotenv
from playwright.sync_api import Browser, Page
from pages.base_page import BasePage
from pages.dashboard_page import DashboardPage
from pages.authentication_page import AuthenticationPage
from utils.logger import logger
import allure

load_dotenv()


@pytest.fixture(scope="module")
def authenticated_context(browser: Browser):
    logger.info("Настройка контекста с авторизацией через API")
    api_base_url = BasePage.API_URL
    email = os.getenv("EMAIL", "ikra-nn@yandex.ru")
    password = os.getenv("PASSWORD", "q1w2e3r4t5Y")
    logger.info(f"API_URL: {api_base_url}, EMAIL: {email}")

    try:
        response = requests.post(
            f"{api_base_url}/auth/login",
            json={"email": email, "password": password},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        logger.info(f"Ответ API: {response.text}")
        response_data = response.json()
        token = response_data.get("token")
        user = response_data.get("user")
        if not token or not user:
            logger.error("Нет токена или данных пользователя в ответе API")
            raise AssertionError("Нет токена или данных пользователя в ответе API")
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка API-запроса: {e}")
        if e.response:
            logger.error(f"Ответ сервера: {e.response.text}")
        logger.info("Переход на UI-авторизацию как запасной вариант")
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()
        auth_page = AuthenticationPage(page)
        with allure.step("Открыть страницу авторизации"):
            auth_page.navigate()
        with allure.step("Выполнить вход"):
            auth_page.login(email, password, expect_success=True)
        context.storage_state(path="state.json")
        page.close()
        yield context
        context.close()
        logger.info("Контекст с авторизацией закрыт")
        return

    context = browser.new_context(
        ignore_https_errors=True,
        storage_state={
            "cookies": [
                {
                    "name": "jwt",
                    "value": response.cookies.get("jwt", token),
                    "url": BasePage.BASE_URL,
                    "sameSite": "Strict",
                    "secure": True
                }
            ],
            "origins": [
                {
                    "origin": BasePage.BASE_URL,
                    "localStorage": [
                        {"name": "authToken", "value": token},
                        {
                            "name": "persist:root",
                            "value": json.dumps({
                                "global": json.dumps({"isSidebarOpen": True, "isModalOpen": False, "isTaskDetailsModalOpen": False, "task": False}),
                                "auth": json.dumps({"user": user, "token": token}),
                                "_persist": json.dumps({"version": -1, "rehydrated": True})
                            })
                        }
                    ]
                }
            ]
        }
    )
    yield context
    context.close()
    logger.info("Контекст с авторизацией закрыт")