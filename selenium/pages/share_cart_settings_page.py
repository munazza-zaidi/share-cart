from urllib.parse import urlencode

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class ShareCartSettingsPage:
    SETTINGS_PATH = "/wp-admin/admin.php"

    TABS = {
        "general": "General",
        "url": "URL Config",
        "display": "Display",
        "redirect": "Redirect",
        "privacy": "Privacy",
        "popup": "Popup Style",
        "sharing": "Sharing",
        "errors": "Error Handling",
    }

    TAB_ALIASES = {
        "general": "general",
        "url": "url",
        "url config": "url",
        "display": "display",
        "redirect": "redirect",
        "privacy": "privacy",
        "popup": "popup",
        "popup style": "popup",
        "sharing": "sharing",
        "error": "errors",
        "errors": "errors",
        "error handling": "errors",
    }

    def __init__(self, driver, wait, base_url):
        self.driver = driver
        self.wait = wait
        self.base_url = base_url.rstrip("/")

    def open(self, tab="general"):
        tab_slug = self._normalize_tab(tab)
        query = urlencode(
            {
                "page": "wc-settings",
                "tab": "share_cart_url_for_woo",
                "scuf_tab": tab_slug,
            }
        )
        self.driver.get(f"{self.base_url}{self.SETTINGS_PATH}?{query}")
        self.wait_for_tab(tab_slug)
        return self

    def navigate_to_tab(self, tab):
        tab_slug = self._normalize_tab(tab)
        tab_link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, self.TABS[tab_slug])))
        tab_link.click()
        self.wait_for_tab(tab_slug)
        return self

    def navigate_to_general_tab(self):
        return self.navigate_to_tab("General")

    def navigate_to_url_config_tab(self):
        return self.navigate_to_tab("URL Config")

    def navigate_to_display_tab(self):
        return self.navigate_to_tab("Display")

    def navigate_to_redirect_tab(self):
        return self.navigate_to_tab("Redirect")

    def navigate_to_privacy_tab(self):
        return self.navigate_to_tab("Privacy")

    def navigate_to_popup_style_tab(self):
        return self.navigate_to_tab("Popup Style")

    def navigate_to_sharing_tab(self):
        return self.navigate_to_tab("Sharing")

    def navigate_to_error_handling_tab(self):
        return self.navigate_to_tab("Error Handling")

    def wait_for_tab(self, tab):
        tab_slug = self._normalize_tab(tab)
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".scuf-settings-wrap")))
        self.wait.until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, ".nav-tab-active span"),
                self.TABS[tab_slug],
            )
        )

    def click_save_settings(self):
        current_tab = self.active_tab_slug()
        self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//input[@type='submit' and @value='Save Settings']"
                    " | //button[normalize-space()='Save Settings']",
                )
            )
        ).click()
        self.wait.until(lambda driver: "scuf_saved=1" in driver.current_url)
        self.wait_for_tab(current_tab)
        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(normalize-space(), 'Settings saved successfully.')]")
            )
        )

    def refresh_and_wait(self):
        current_tab = self.active_tab_slug()
        self.driver.refresh()
        self.wait_for_tab(current_tab)

    def set_checkbox(self, identifier, checked=True):
        checkbox = self.checkbox(identifier)
        if checkbox.is_selected() != checked:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
            checkbox.click()
        self.wait.until(lambda _: checkbox.is_selected() == checked)

    def checkbox_checked(self, identifier):
        return self.checkbox(identifier).is_selected()

    def select_radio_option(self, group_label, option_label):
        radio = self.wait.until(
            EC.element_to_be_clickable(self._radio_option_locator(group_label, option_label))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", radio)
        radio.click()
        self.wait.until(lambda _: radio.is_selected())

    def selected_radio_value(self, group_label):
        radios = self.wait.until(
            EC.presence_of_all_elements_located(self._radio_group_locator(group_label))
        )
        for radio in radios:
            if radio.is_selected():
                return radio.get_attribute("value")
        raise AssertionError(f"No selected radio option found for '{group_label}'.")

    def enter_text(self, identifier, value):
        element = self.input(identifier)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        element.clear()
        element.send_keys(value)

    def input_value(self, identifier):
        return self.input(identifier).get_attribute("value")

    def text_of(self, identifier):
        return self.element(identifier).text

    def element(self, identifier):
        return self.wait.until(EC.presence_of_element_located(self._locator(identifier)))

    def input(self, identifier):
        return self.wait.until(EC.element_to_be_clickable(self._field_locator(identifier)))

    def checkbox(self, identifier):
        return self.wait.until(EC.element_to_be_clickable(self._field_locator(identifier)))

    def active_tab_slug(self):
        label = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".nav-tab-active span"))
        ).text.strip()
        for slug, tab_label in self.TABS.items():
            if tab_label == label:
                return slug
        raise ValueError(f"Unknown active tab label: {label}")

    def _normalize_tab(self, tab):
        tab_key = str(tab).strip().lower()
        if tab_key in self.TABS:
            return tab_key
        if tab_key in self.TAB_ALIASES:
            return self.TAB_ALIASES[tab_key]
        raise ValueError(f"Unknown tab: {tab}")

    def _locator(self, identifier):
        if isinstance(identifier, tuple):
            return identifier

        value = self._xpath_literal(str(identifier))
        return (By.XPATH, f"//*[@id={value} or @name={value} or @placeholder={value} or normalize-space()={value}]")

    def _field_locator(self, identifier):
        if isinstance(identifier, tuple):
            return identifier

        value = self._xpath_literal(str(identifier))
        return (
            By.XPATH,
            "("
            f"//*[@name={value} or @id={value} or @placeholder={value}]"
            " | "
            f"//*[@id=(//label[normalize-space()={value} or .//span[normalize-space()={value}]]/@for)]"
            " | "
            f"//label[normalize-space()={value} or .//span[normalize-space()={value}]]//input"
            " | "
            f"//label[normalize-space()={value} or .//span[normalize-space()={value}]]//textarea"
            " | "
            f"//label[normalize-space()={value} or .//span[normalize-space()={value}]]//select"
            " | "
            f"//tr[.//th[normalize-space()={value}]]//input"
            " | "
            f"//tr[.//th[normalize-space()={value}]]//textarea"
            " | "
            f"//tr[.//th[normalize-space()={value}]]//select"
            ")[1]",
        )

    def _radio_option_locator(self, group_label, option_label):
        group = self._xpath_literal(str(group_label))
        option = self._xpath_literal(str(option_label))
        return (
            By.XPATH,
            f"//tr[.//th[normalize-space()={group}]]"
            f"//label[contains(normalize-space(), {option})]//input[@type='radio']",
        )

    def _radio_group_locator(self, group_label):
        group = self._xpath_literal(str(group_label))
        return (
            By.XPATH,
            f"//tr[.//th[normalize-space()={group}]]//input[@type='radio']",
        )

    @staticmethod
    def _xpath_literal(value):
        if "'" not in value:
            return f"'{value}'"
        if '"' not in value:
            return f'"{value}"'
        return "concat(" + ', "\'", '.join(f"'{part}'" for part in value.split("'")) + ")"
