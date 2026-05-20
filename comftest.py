# conftest.py (в корне проекта)
import pathlib
import sys

ROOT_DIR = pathlib.Path(__file__).parent.absolute()

sys.path.append(str(ROOT_DIR / "app"))
