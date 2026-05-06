def test_general_tab_renders_expected_controls(share_cart_settings_page):
    page = share_cart_settings_page.open("General")

    assert page.checkbox("Enable Share Cart").is_displayed()
    assert page.checkbox("Enable Save Cart").is_displayed()


def test_general_settings_save_refresh_and_persist(share_cart_settings_page):
    page = share_cart_settings_page.open("General")

    page.set_checkbox("Enable Share Cart", False)
    page.set_checkbox("Enable Save Cart", True)
    page.click_save_settings()
    page.refresh_and_wait()

    assert page.checkbox_checked("Enable Share Cart") is False
    assert page.checkbox_checked("Enable Save Cart") is True
