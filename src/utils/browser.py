from playwright.sync_api import sync_playwright


def launch_browser(headless=False):
    """
    Launch a Chromium browser and return the Playwright objects.
    """
    playwright = sync_playwright().start()

    browser = playwright.chromium.launch(
        headless=headless
    )

    page = browser.new_page()

    return playwright, browser, page