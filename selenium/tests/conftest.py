import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait

from pages.share_cart_settings_page import ShareCartSettingsPage
from utils.config import DEFAULT_BASE_URL, env_bool
from utils.wordpress_auth import WordPressAdminLogin


def pytest_addoption(parser):
    parser.addoption("--base-url", default=os.getenv("SCUF_BASE_URL", DEFAULT_BASE_URL))
    parser.addoption("--admin-user", default=os.getenv("SCUF_ADMIN_USER"))
    parser.addoption("--admin-password", default=os.getenv("SCUF_ADMIN_PASSWORD"))
    parser.addoption("--browser", default=os.getenv("SCUF_BROWSER", "chrome"), choices=("chrome", "firefox"))
    parser.addoption("--headed", action="store_true", default=env_bool("SCUF_HEADED"))


@pytest.fixture(scope="session")
def base_url(pytestconfig):
    return pytestconfig.getoption("--base-url").rstrip("/")


@pytest.fixture(scope="session")
def admin_credentials(pytestconfig):
    username = pytestconfig.getoption("--admin-user")
    password = pytestconfig.getoption("--admin-password")
    if not username or not password:
        pytest.skip(
            "Set SCUF_ADMIN_USER and SCUF_ADMIN_PASSWORD, or pass "
            "--admin-user and --admin-password."
        )
    return username, password


@pytest.fixture
def driver(pytestconfig):
    browser = pytestconfig.getoption("--browser")
    headed = pytestconfig.getoption("--headed")

    if browser == "firefox":
        options = FirefoxOptions()
        if not headed:
            options.add_argument("-headless")
        instance = webdriver.Firefox(options=options)
    else:
        options = ChromeOptions()
        if not headed:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1440,1200")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-save-password-bubble")
        options.add_argument("--disable-features=PasswordLeakDetection")
        options.add_experimental_option(
            "prefs",
            {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
                "profile.password_manager_leak_detection": False,
            },
        )
        instance = webdriver.Chrome(options=options)

    instance.set_window_size(1440, 1200)
    yield instance
    instance.quit()


@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, 15)


@pytest.fixture
def share_cart_settings_page(driver, wait, base_url, admin_credentials):
    username, password = admin_credentials
    WordPressAdminLogin(driver, wait, base_url).login(username, password)
    return ShareCartSettingsPage(driver, wait, base_url)
