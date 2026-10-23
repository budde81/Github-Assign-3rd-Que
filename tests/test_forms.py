from __future__ import annotations

import pytest
from playwright.sync_api import expect

from pages.forms_page import FormsPage, RegistrationDetails


@pytest.mark.smoke
def test_login_accepts_documented_practice_credentials(forms_page: FormsPage) -> None:
    forms_page.submit_login("tester", "password123")

    expect(
        forms_page.page.get_by_text(
            "Login successful! Welcome, tester.", exact=True
        )
    ).to_be_visible()


@pytest.mark.parametrize(
    ("username", "password"),
    [
        pytest.param("wrong-user", "password123", id="unknown-username"),
        pytest.param("tester", "wrong-password", id="incorrect-password"),
        pytest.param("", "", id="empty-credentials"),
    ],
)
@pytest.mark.regression
def test_login_rejects_invalid_credentials(
    forms_page: FormsPage, username: str, password: str
) -> None:
    forms_page.submit_login(username, password)

    expect(
        forms_page.page.get_by_text(
            "Invalid credentials. Try username: tester, password: password123",
            exact=True,
        )
    ).to_be_visible()


@pytest.mark.regression
def test_password_visibility_can_be_toggled(forms_page: FormsPage) -> None:
    password_field = forms_page.login_password
    expect(password_field).to_have_attribute("type", "password")

    hide_button = forms_page.toggle_password_visibility()
    expect(password_field).to_have_attribute("type", "text")
    expect(hide_button).to_be_visible()

    show_button = forms_page.toggle_password_visibility()
    expect(password_field).to_have_attribute("type", "password")
    expect(show_button).to_be_visible()


@pytest.mark.regression
def test_forgot_password_dialog_opens_and_closes(forms_page: FormsPage) -> None:
    dialog = forms_page.open_forgot_password_dialog()
    expect(
        dialog.get_by_text(
            "Enter your username to retrieve your password.", exact=True
        )
    ).to_be_visible()

    dialog.get_by_test_id("forgot-password-modal-close").click()
    expect(dialog).to_be_hidden()


@pytest.mark.smoke
def test_registration_accepts_complete_details(forms_page: FormsPage) -> None:
    details = RegistrationDetails(
        first_name="Taylor",
        last_name="Tester",
        email="taylor.tester@example.com",
        country="India",
    )

    forms_page.submit_registration(details)

    expect(
        forms_page.page.get_by_text(
            "Registration successful for Taylor Tester!", exact=True
        )
    ).to_be_visible()


@pytest.mark.regression
def test_registration_requires_all_fields(forms_page: FormsPage) -> None:
    forms_page.page.get_by_test_id("register-submit").click()

    expect(
        forms_page.page.get_by_text(
            "Please fill in all required fields.", exact=True
        )
    ).to_be_visible()


@pytest.mark.regression
def test_clear_resets_registration_fields(forms_page: FormsPage) -> None:
    forms_page.registration_first_name.fill("Morgan")
    forms_page.registration_last_name.fill("Example")
    forms_page.registration_email.fill("morgan.example@example.com")
    forms_page.registration_country.select_option(label="Canada")

    forms_page.clear_registration()

    expect(forms_page.registration_first_name).to_have_value("")
    expect(forms_page.registration_last_name).to_have_value("")
    expect(forms_page.registration_email).to_have_value("")
    expect(
        forms_page.registration_country.locator("option:checked")
    ).to_have_text("Select country")
