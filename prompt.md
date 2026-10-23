# Prompt: QA Practice Hub Registration and Login Automation

Generate and maintain a production-ready UI test automation framework for the
Registration and Login forms on `https://qapracticehub.com/#forms`.

## Required technology and environment

- Implement the tests in Python with pytest and Playwright's synchronous API.
- Use the pytest-playwright fixtures and execute the browser tests in Google
  Chrome (Chromium engine, Chrome channel).
- Use the available Python, pytest, and Playwright MCP servers in the Chrome
  environment to inspect and validate the live practice page before relying on
  selectors or expected behavior.
- Keep browser interaction in test code; do not add application code or submit
  real personal information.
- Keep all Login and Registration test cases together in one pytest module
  (for example, `tests/test_forms.py`) rather than splitting them into separate
  login and registration test files.

## Coverage

- Include both positive (valid input / expected success) and negative (invalid
  or missing input / expected validation or rejection) test cases for Login
  and Registration. Keep them as distinct, clearly named tests or parameter
  cases so each behavior is reported independently.
- Positive cases:
  - Verify both forms load and are operable.
  - Verify login succeeds with the credentials documented on the practice
    page.
  - Verify registration succeeds with complete, valid example data.
  - Verify the password visibility control, forgot-password dialog, and
    registration Clear action work as expected.
- Negative cases:
  - Verify login rejects a wrong username, a wrong password, and empty
    credentials, asserting the user-visible error.
  - Verify registration rejects missing required fields and displays the
    appropriate user-visible validation.
  - Add other invalid registration cases only when the live page's actual
    validation rules and expected results have been verified; do not assume
    browser or application behavior from conventional form design.
- Assert user-visible results rather than implementation details wherever
  possible, and ensure each negative test proves the invalid submission does
  not produce a success result.

## Engineering requirements

- Use maintainable page objects, typed test helpers, semantic/accessibility
  locators, and pytest fixtures.
- Handle the cookie consent dialog without making tests depend on an existing
  browser profile.
- Make the target URL configurable through `QA_URL` or `--qa-url`; default to
  the public forms page.
- Configure repeatable Chrome execution, strict pytest markers, and
  failure-only screenshots, video, and Playwright traces.
- Keep test data deterministic and non-sensitive. Do not log credentials,
  introduce fixed sleeps, silently swallow exceptions, or rely on fragile
  positional selectors where a semantic locator is available.
- Provide concise setup and run instructions and validate test collection and
  the merged test module after changes.
