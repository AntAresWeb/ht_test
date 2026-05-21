import sys
from pathlib import Path

import pytest


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config) -> None :
    root_dir = Path(__file__).parent
    app_dir = root_dir / "app"
    sys.path.insert(0, str(app_dir))
