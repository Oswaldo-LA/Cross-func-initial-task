# test_incognito_browser.py
import pytest
from playwright.sync_api import sync_playwright, expect

class ProgressBarPage:
    def __init__(self, page):
        self.page = page
        self.start_button = lambda: self.page.locator(".mt-3.btn.btn-primary")

    def go_to_google(self):
        self.page.goto("https://www.google.com")
        assert "Google" in self.page.title()

    def go_to_demoqa_widgets(self):
        self.page.goto("https://demoqa.com")
        self.page.locator("div.card-body >> text=Widgets").click()
        expect(self.page).to_have_url("https://demoqa.com/widgets")

    def go_to_progress_bar(self):
        self.page.locator("ul.menu-list >> text=Progress Bar").click()
        expect(self.page).to_have_url("https://demoqa.com/progress-bar")

    def start_progress_bar(self):
        self.start_button().click()

    def wait_until_complete(self):
        self.page.wait_for_selector("div.progress-bar[aria-valuenow='100']", timeout=20000)

    def get_progress_text(self):
        return self.page.locator("div.progress-bar").inner_text()

    def expect_reset_button(self):
        expect(self.start_button()).to_have_text("Reset")

    def reload_page(self):
        self.page.reload()
        # Reasignación no necesaria; se usa lambda para obtener el botón actualizado

    def expect_start_button(self):
        expect(self.start_button()).to_have_text("Start")


@pytest.fixture(scope="function")
def browser_context():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        yield context
        context.close()
        browser.close()

class TestProgressBar:
    def test_progress_bar_completion_and_reset_button(self, browser_context):
        page = browser_context.new_page()
        progress_bar = ProgressBarPage(page)

        progress_bar.go_to_google()
        progress_bar.go_to_demoqa_widgets()
        progress_bar.go_to_progress_bar()

        progress_bar.start_progress_bar()
        progress_bar.wait_until_complete()
        assert "100%" in progress_bar.get_progress_text()
        progress_bar.expect_reset_button()

        progress_bar.reload_page()
        progress_bar.expect_start_button()




