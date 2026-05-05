from selenium.webdriver.common.by import By


def test_general_tab_renders_expected_controls(share_cart_settings_page):
    page = share_cart_settings_page.open("General")

    assert page.element((By.NAME, "share_cart_url_for_woo_enable")).is_displayed()
    assert page.element((By.NAME, "save_cart_url_for_woo_enable")).is_displayed()


def test_general_settings_save_refresh_and_persist(share_cart_settings_page):
    page = share_cart_settings_page.open("General")

    page.set_checkbox("share_cart_url_for_woo_enable", False)
    page.set_checkbox("save_cart_url_for_woo_enable", True)
    page.click_save_settings()
    page.refresh_and_wait()

    assert page.checkbox_checked("share_cart_url_for_woo_enable") is False
    assert page.checkbox_checked("save_cart_url_for_woo_enable") is True
