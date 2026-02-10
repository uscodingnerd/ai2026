from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.amazon.com")
    print(page.title())

    # sleep / wait for 5 seconds
    page.wait_for_timeout(5000)  # milliseconds

    browser.close()
