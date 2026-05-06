def test_display_tab_renders_expected_controls(share_cart_settings_page):
    page = share_cart_settings_page.open("Display")

    assert page.input("Save Cart Menu Title").is_displayed()
    assert page.input("Save Cart Endpoint").is_displayed()
    assert page.input("Text Above Share Button").is_displayed()


def test_display_settings_save_refresh_and_persist(share_cart_settings_page):
    page = share_cart_settings_page.open("Display")

    page.enter_text("Save Cart Menu Title", "QA Saved Carts")
    page.enter_text("Save Cart Endpoint", "qa-saved-carts")
    page.enter_text("Text Above Share Button", "QA message above the share cart button.")

    page.click_save_settings()
    page.refresh_and_wait()

    assert page.input_value("Save Cart Menu Title") == "QA Saved Carts"
    assert page.input_value("Save Cart Endpoint") == "qa-saved-carts"
    assert page.input_value("Text Above Share Button") == "QA message above the share cart button."
