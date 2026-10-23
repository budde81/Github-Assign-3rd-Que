# QA Practice Hub form automation

Pytest and Playwright end-to-end tests for the login and registration forms at
`https://qapracticehub.com/#forms`. Tests run in Google Chrome by default and
use accessible labels and roles for form fields.

## Setup

Use Python 3.10 or newer:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[test]"
python -m playwright install chrome
```

## Run

```powershell
pytest
```

Pytest uses the Chrome channel and retains traces, screenshots, and video only
for failing tests. Artifacts are written under `test-results/`.

Override the target URL when needed:

```powershell
$env:QA_URL = "https://qapracticehub.com/#forms"
pytest
```

Or pass `--qa-url` directly. The framework sets the `#forms` fragment even if
the provided URL has a different fragment.

Useful selectors:

```powershell
pytest -m smoke
pytest tests/test_forms.py
pytest --headed
pytest --browser-channel=msedge
```

When using `--headed`, each test keeps its Chrome page open for at least eight
seconds after the test finishes so the result can be viewed. Headless runs are
not delayed.

The sample site's documented login credentials are `tester` and
`password123`. Registration tests submit example data only; they do not
create accounts in a third-party service.
