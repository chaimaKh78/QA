# conftest.py
import os

# Allow Django database operations in async contexts (Playwright tests)
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

import pytest

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "ignore_https_errors": True,
    }