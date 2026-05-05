# Share Cart Selenium Tests

Standalone Selenium pytest framework using Page Object Model.

## Install

```bash
cd selenium
python3 -m pip install -r requirements.txt
```

## Run

```bash
SCUF_ADMIN_USER="admin" \
SCUF_ADMIN_PASSWORD="your_wp_password" \
python3 -m pytest --base-url=http://git-sites.local --headed
```

Run a single test file:

```bash
SCUF_ADMIN_USER="admin" \
SCUF_ADMIN_PASSWORD="your_wp_password" \
python3 -m pytest tests/test_general_settings.py --headed
```

The Chrome fixture disables password manager prompts and leak-detection popups so
browser security UI does not block WordPress admin login during automation.
