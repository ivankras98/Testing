# tests/test_navigation.py
import pytest
import os
import allure
import json
from dotenv import load_dotenv
from playwright.sync_api import expect, TimeoutError as PlaywrightTimeoutError
from allure import title, step, attach
from allure_commons.types import AttachmentType
from utils.logger import logger
from settings import BASE_URL
from pages.authentication_page import AuthenticationPage
from pages.dashboard_page import DashboardPage

# Загрузка переменных из .env
load_dotenv()

@pytest.mark.navigation
@title("Загрузка дашборда")
def test_homepage_loads(dashboard_page):
    with step("Переход на дашборд"):
        dashboard_page.navigate_to(f"{BASE_URL}/dashboard")
    with step("Проверка загрузки дашборда"):
        logger.info(f"Текущий URL: {dashboard_page.page.url}")
        expect(dashboard_page.page).to_have_url(f"{BASE_URL}/dashboard", timeout=30000)

@pytest.mark.navigation
@title("Переход в раздел сообщений")
def test_messages_navigation(dashboard_page):
    with step("Переход в раздел сообщений"):
        dashboard_page.go_to_messages()
    with step("Проверка перехода на страницу сообщений"):
        logger.info(f"Текущий URL: {dashboard_page.page.url}")
        expect(dashboard_page.page).to_have_url(f"{BASE_URL}/messages", timeout=30000)

@pytest.mark.navigation
@title("Переход в раздел участников")
def test_members_navigation(dashboard_page):
    with step("Переход в раздел участников"):
        dashboard_page.go_to_members()
    with step("Проверка перехода на страницу участников"):
        logger.info(f"Текущий URL: {dashboard_page.page.url}")
        expect(dashboard_page.page).to_have_url(f"{BASE_URL}/members", timeout=30000)


@pytest.mark.navigation
@title("Переход на несуществующую страницу")
def test_nonexistent_page(page):
    auth_page = AuthenticationPage(page)
    with step("Переход на страницу авторизации"):
        auth_page.navigate()
        logger.info(f"Текущий URL после перехода на авторизацию: {auth_page.page.url}")
    with step("Переход на несуществующую страницу"):
        response = auth_page.page.goto(f"{BASE_URL}/nonexistent", wait_until="networkidle")
        logger.info(f"Статус ответа: {response.status if response else 'Нет ответа'}")
        logger.info(f"Текущий URL: {auth_page.page.url}")
    with step("Проверка редиректа на страницу авторизации"):
        expect(auth_page.page).to_have_url(f"{BASE_URL}/authentication", timeout=30000)
        auth_page.take_screenshot("nonexistent_auth_redirect.png")
        allure.attach.file("nonexistent_auth_redirect.png", name="Скриншот редиректа на авторизацию", attachment_type=allure.attachment_type.PNG)
        expect(auth_page.email_input).to_be_visible(timeout=15000)
        expect(auth_page.password_input).to_be_visible(timeout=15000)
        expect(auth_page.submit_button).to_be_visible(timeout=15000)

@pytest.mark.navigation
@title("Переход на дашборд без авторизации")
def test_dashboard_without_login(page):
    auth_page = AuthenticationPage(page)
    with step("Переход на дашборд"):
        auth_page.navigate(f"{BASE_URL}/dashboard")
    with step("Проверка редиректа на страницу авторизации"):
        logger.info(f"Текущий URL: {auth_page.page.url}")
        expect(auth_page.page).to_have_url(f"{BASE_URL}/authentication", timeout=30000)
        expect(auth_page.email_input).to_be_visible(timeout=30000)
        expect(auth_page.password_input).to_be_visible(timeout=30000)
        expect(auth_page.submit_button).to_be_visible(timeout=30000)

@pytest.mark.navigation
@title("Переход на проекты без авторизации")
def test_projects_without_login(page):
    auth_page = AuthenticationPage(page)
    with step("Переход на проекты"):
        auth_page.navigate(f"{BASE_URL}/projects")
    with step("Проверка редиректа на страницу авторизации"):
        logger.info(f"Текущий URL: {auth_page.page.url}")
        expect(auth_page.page).to_have_url(f"{BASE_URL}/authentication", timeout=30000)
        expect(auth_page.email_input).to_be_visible(timeout=30000)
        expect(auth_page.password_input).to_be_visible(timeout=30000)
        expect(auth_page.submit_button).to_be_visible(timeout=30000)

@pytest.mark.navigation
@title("Переход на задачи без авторизации")
def test_tasks_without_login(page):
    auth_page = AuthenticationPage(page)
    with step("Переход на задачи"):
        auth_page.navigate(f"{BASE_URL}/tasks")
    with step("Проверка редиректа на страницу авторизации"):
        logger.info(f"Текущий URL: {auth_page.page.url}")
        expect(auth_page.page).to_have_url(f"{BASE_URL}/authentication", timeout=30000)
        expect(auth_page.email_input).to_be_visible(timeout=30000)
        expect(auth_page.password_input).to_be_visible(timeout=30000)
        expect(auth_page.submit_button).to_be_visible(timeout=30000)

@pytest.mark.navigation
@title("Переход на участников без авторизации")
def test_members_without_login(page):
    auth_page = AuthenticationPage(page)
    with step("Переход на участников"):
        auth_page.navigate(f"{BASE_URL}/members")
    with step("Проверка редиректа на страницу авторизации"):
        logger.info(f"Текущий URL: {auth_page.page.url}")
        expect(auth_page.page).to_have_url(f"{BASE_URL}/authentication", timeout=30000)
        expect(auth_page.email_input).to_be_visible(timeout=30000)
        expect(auth_page.password_input).to_be_visible(timeout=30000)
        expect(auth_page.submit_button).to_be_visible(timeout=30000)

@pytest.mark.navigation
@title("Переход на сообщения без авторизации")
def test_messages_without_login(page):
    auth_page = AuthenticationPage(page)
    with step("Переход на сообщения"):
        auth_page.navigate(f"{BASE_URL}/messages")
    with step("Проверка редиректа на страницу авторизации"):
        logger.info(f"Текущий URL: {auth_page.page.url}")
        expect(auth_page.page).to_have_url(f"{BASE_URL}/authentication", timeout=30000)
        expect(auth_page.email_input).to_be_visible(timeout=30000)
        expect(auth_page.password_input).to_be_visible(timeout=30000)
        expect(auth_page.submit_button).to_be_visible(timeout=30000)