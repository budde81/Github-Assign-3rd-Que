from __future__ import annotations

import os
from collections.abc import Iterator
from urllib.parse import urlsplit, urlunsplit

import pytest
from playwright.sync_api import Page

from pages.forms_page import FormsPage

DEFAULT_TARGET_URL = "https://qapracticehub.com/#forms"
HEADED_PAGE_REVIEW_MS = 8_000


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--qa-url",
        action="store",
        default=os.getenv("QA_URL", DEFAULT_TARGET_URL),
        help="Full URL for the form page (default: QA_URL or the public practice page).",
    )


def _forms_url(raw_url: str) -> str:
    try:
        parsed = urlsplit(raw_url.strip())
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError
    except ValueError as exc:
        raise pytest.UsageError(
            f"Invalid --qa-url {raw_url!r}; provide an absolute HTTP(S) URL."
        ) from exc

    return urlunsplit(
        (parsed.scheme, parsed.netloc, parsed.path, parsed.query, "forms")
    )


@pytest.fixture
def forms_page(page: Page, request: pytest.FixtureRequest) -> Iterator[FormsPage]:
    target_url = _forms_url(request.config.getoption("--qa-url"))
    form_page = FormsPage(page, target_url)
    form_page.open()
    yield form_page

    if request.config.getoption("headed"):
        page.wait_for_timeout(HEADED_PAGE_REVIEW_MS)
