from selenium.webdriver.common.by import By


def test_url_config_tab_renders_expected_controls(share_cart_settings_page):
    page = share_cart_settings_page.open("URL Config")

    assert page.input("Link Prefix").is_displayed()
    assert page.input("Link Code Length").is_displayed()
    assert page.element((By.ID, "scuf-url-preview-text")).is_displayed()


def test_url_config_save_refresh_and_persist(share_cart_settings_page):
    page = share_cart_settings_page.open("URL Config")

    page.enter_text("Link Prefix", "qa_ref")
    page.enter_text("Link Code Length", "10")
    page.wait.until(
        lambda _: "qa_ref=a1b2c3d4e5" in page.element((By.ID, "scuf-url-preview-text")).text
    )

    page.click_save_settings()
    page.refresh_and_wait()

    assert page.input_value("Link Prefix") == "qa_ref"
    assert page.input_value("Link Code Length") == "10"
    assert "qa_ref=a1b2c3d4e5" in page.text_of((By.ID, "scuf-url-preview-text"))
