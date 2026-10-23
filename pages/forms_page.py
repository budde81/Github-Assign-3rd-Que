from __future__ import annotations

from dataclasses import dataclass

from playwright.sync_api import Locator, Page, expect


@dataclass(frozen=True)
class RegistrationDetails:
    first_name: str
    last_name: str
    email: str
    country: str


class FormsPage:
    """Page object for the login and registration practice forms."""

    def __init__(self, page: Page, target_url: str) -> None:
        self.page = page
        self.target_url = target_url

        self.login_username = page.get_by_role("textbox", name="Username").first
        self.login_password = page.get_by_role("textbox", name="Password")
        self.registration_first_name = page.get_by_role(
            "textbox", name="First Name"
        )
        self.registration_last_name = page.get_by_role("textbox", name="Last Name")
        self.registration_email = page.get_by_role("textbox", name="Email")
        self.registration_country = page.get_by_role("combobox", name="Country")

    def open(self) -> None:
        self.page.goto(self.target_url, wait_until="domcontentloaded")
        expect(
            self.page.get_by_role("heading", name="Login & Registration Forms")
        ).to_be_visible()

        cookie_accept = self.page.get_by_test_id("cookie-accept")
        if cookie_accept.is_visible():
            cookie_accept.click()

    def submit_login(self, username: str, password: str) -> None:
        self.login_username.fill(username)
        self.login_password.fill(password)
        self.page.get_by_test_id("login-submit").click()

    def toggle_password_visibility(self) -> Locator:
        show_button = self.page.get_by_role("button", name="Show password")
        if show_button.is_visible():
            show_button.click()
            return self.page.get_by_role("button", name="Hide password")

        hide_button = self.page.get_by_role("button", name="Hide password")
        hide_button.click()
        return show_button

    def submit_registration(self, details: RegistrationDetails) -> None:
        self.registration_first_name.fill(details.first_name)
        self.registration_last_name.fill(details.last_name)
        self.registration_email.fill(details.email)
        self.registration_country.select_option(label=details.country)
        self.page.get_by_test_id("register-submit").click()

    def clear_registration(self) -> None:
        self.page.get_by_test_id("register-clear").click()

    def open_forgot_password_dialog(self) -> Locator:
        self.page.get_by_role("button", name="Forgot password?").click()
        dialog = self.page.get_by_role("dialog")
        expect(dialog.get_by_role("heading", name="Forgot Password")).to_be_visible()
        return dialog
