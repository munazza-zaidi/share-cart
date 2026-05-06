def test_privacy_tab_renders_expected_controls(share_cart_settings_page):
    page = share_cart_settings_page.open("Privacy")

    assert page.input("Default Cart Privacy").is_displayed()


def test_privacy_option_save_refresh_and_persist(share_cart_settings_page):
    page = share_cart_settings_page.open("Privacy")

    page.select_radio_option("Default Cart Privacy", "Private")
    page.click_save_settings()
    page.refresh_and_wait()

    assert page.selected_radio_value("Default Cart Privacy") == "private"
