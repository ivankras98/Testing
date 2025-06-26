# tests/conftest.py
import pytest
import requests
import os
import json
from dotenv import load_dotenv
from playwright.sync_api import Browser, Page
from pages.dashboard_page import DashboardPage
from pages.authentication_page import AuthenticationPage
from utils.logger import logger

load_dotenv()



@pytest.fixture(scope="module")
def authenticated_context(browser: Browser):
    logger.info("Настройка контекста с авторизацией через API")
    api_base_url = "http://localhost:8000/api"  
    email = os.getenv("EMAIL", "ikra-nn@yandex.ru")
    password = os.getenv("PASSWORD", "q1w2e3r4t5Y")
    
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
        logger.info("Переход на UI-авторизацию как запасной вариант")
        # UI-авторизация как fallback
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()
        auth_page = AuthenticationPage(page)
        auth_page.navigate()
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
                    "url": "http://localhost:3000",
                    "sameSite": "Strict",
                    "secure": True
                }
            ],
            "origins": [
                {
                    "origin": "http://localhost:3000",
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