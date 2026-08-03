from playwright.sync_api import Page, expect
import pytest

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.email_input    = page.get_by_label("Email")
        self.password_input = page.get_by_label("Password")
        self.submit_button  = page.get_by_role("button", name="Login")
        self.error_message  = page.get_by_role("alert")

    def navigate(self):
        self.page.goto("https://the-internet.herokuapp.com/login")

    def login(self, email: str, password: str):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()

    def get_error(self) -> str:
        return self.error_message.text_content()

@pytest.fixture
def login_page(page: Page):
    login = LoginPage(page)
    login.navigate()
    return login

@pytest.mark.skip(reason="UI test — requires local browser install, kept for local practice")
def test_successful_login(login_page):
    login_page.login("qa@email.com", "password123")
    expect(login_page.page).to_have_url("https://tenable.test.com/dashboard")

@pytest.mark.skip(reason="UI test — requires local browser install, kept for local practice")
def test_failed_login(login_page):
    login_page.login("wrong@email.com", "wrongpassword")
    assert "Invalid credentials" in login_page.get_error()