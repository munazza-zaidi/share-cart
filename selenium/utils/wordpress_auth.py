from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class WordPressAdminLogin:
    def __init__(self, driver, wait, base_url):
        self.driver = driver
        self.wait = wait
        self.base_url = base_url.rstrip("/")

    def login(self, username, password):
        self.driver.get(urljoin(f"{self.base_url}/", "wp-login.php"))

        username_input = self.wait.until(EC.element_to_be_clickable((By.NAME, "log")))
        username_input.clear()
        username_input.send_keys(username)

        password_input = self.wait.until(EC.element_to_be_clickable((By.NAME, "pwd")))
        password_input.clear()
        password_input.send_keys(password)

        self.wait.until(EC.element_to_be_clickable((By.ID, "wp-submit"))).click()
        self.wait.until(lambda driver: "wp-login.php" not in driver.current_url)
