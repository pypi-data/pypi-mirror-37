import pytest

from io import StringIO
from logging import StreamHandler, WARNING, Logger
from contextlib import contextmanager
from pathlib import Path
from typing import Callable, ContextManager

HERE = Path(__file__).parent
APP_DIR = HERE / 'sample_app'
DATA_ROOT = HERE / 'sample_data'
DATA_ROOT_2 = HERE / 'sample_data_2'


@pytest.fixture
def app_dir():
    return APP_DIR


@pytest.fixture
def data_root():
    return DATA_ROOT


@pytest.fixture
def data_root_2():
    return DATA_ROOT_2


@pytest.fixture
def catch_log_warnings() -> Callable[[Logger], ContextManager[StreamHandler]]:
    @contextmanager
    def catcher(logger: Logger):
        handler = StreamHandler(StringIO())
        handler.setLevel(WARNING)
        logger.addHandler(handler)
        yield handler

    return catcher


def get_local_paths():
    return dict(
        app=APP_DIR,
        data=DATA_ROOT / 'data',
        config=DATA_ROOT / 'config',
        summary=DATA_ROOT / 'summary',
        output=DATA_ROOT / 'output',
    )


@pytest.fixture
def local(monkeypatch):
    """patches the paths for local testing"""
    monkeypatch.setattr("fastgenomics._common.DEFAULT_APP_DIR", str(APP_DIR))
    monkeypatch.setattr("fastgenomics._common.DEFAULT_DATA_ROOT", str(DATA_ROOT))
    monkeypatch.setattr("fastgenomics._common._PATHS", {})
    monkeypatch.setattr("fastgenomics.io._PARAMETERS", {})
    monkeypatch.setattr("fastgenomics._common._MANIFEST", {})
    monkeypatch.setattr("fastgenomics._common._INPUT_FILE_MAPPING", {})


@pytest.fixture
def fg_env(monkeypatch):
    """sets app_dir and data_root by env-variables"""
    monkeypatch.setenv('FG_APP_DIR', str(APP_DIR))
    monkeypatch.setenv('FG_DATA_ROOT', str(DATA_ROOT))
    monkeypatch.setattr("fastgenomics._common._PATHS", {})
    monkeypatch.setattr("fastgenomics.io._PARAMETERS", {})
    monkeypatch.setattr("fastgenomics._common._MANIFEST", {})
    monkeypatch.setattr("fastgenomics._common._INPUT_FILE_MAPPING", {})


@pytest.fixture
def clear_output():
    """clear everything except of .gitignore"""
    for name in ['output', 'summary']:
        sub_dir = DATA_ROOT / name
        for entry in sub_dir.glob('*.*'):
            if entry.name != '.gitignore':
                entry.unlink()


@pytest.fixture
def fake_docker(monkeypatch):
    """fakes the docker-environment by overriding the running_within_docker-method returning always true"""
    monkeypatch.setattr("fastgenomics.tools.running_within_docker", lambda: True)
