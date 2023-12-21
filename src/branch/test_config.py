import pytest

from branch.config import read_settings
from branch.testing import modified_environ


@pytest.fixture()
def config_path(tmpdir):
    return f"{tmpdir}/branch.yaml"


@pytest.fixture()
def setup_config(config_path):
    with open(config_path, "w") as fd:
        fd.write(
            """
            server:
                host: localhost
                port: 9090
                ui_port: 9089
                log_level: debug
            storage:
                location: local://.branch/cluster_1
                create: true
            cli:
                table:
                    width: 1000
            feature_flag:
                tui: true
            """
        )


def test_read_settings(config_path, setup_config):
    settings = read_settings(config_path)
    assert settings.server.host == "localhost"
    assert settings.server.port == 9090
    assert settings.server.ui_port == 9089
    assert settings.server.log_level == "debug"
    assert settings.storage.location == "local://.branch/cluster_1"
    assert settings.storage.create is True
    assert settings.cli.table.width == 1000
    assert settings.feature_flag.tui is True


@pytest.fixture()
def setup_empty(config_path):
    with open(config_path, "w") as fd:
        fd.write("")
    yield config_path


def test_read_settings_empty_defaults(config_path, setup_empty):
    settings = read_settings(config_path)
    assert settings.server.host == "0.0.0.0"
    assert settings.server.port == 9000
    assert settings.server.ui_port == 8999
    assert settings.server.log_level == "info"
    assert settings.storage.location == "local://.branch"
    assert settings.storage.create is False
    assert settings.cli.table.width is None
    assert settings.feature_flag.tui is False


def test_read_settings_no_file_defaults(tmpdir):
    settings = read_settings(f"{tmpdir}/i_dont_exist.yaml")
    assert settings.server.host == "0.0.0.0"
    assert settings.server.port == 9000
    assert settings.server.ui_port == 8999
    assert settings.server.log_level == "info"
    assert settings.storage.location == "local://.branch"
    assert settings.storage.create is False
    assert settings.cli.table.width is None
    assert settings.feature_flag.tui is False


def test_read_settings_can_override_attributes_with_env_vars(config_path):
    test_env = {
        "BRANCH_SERVER_HOST": "branch-server-host",
        "BRANCH_SERVER_PORT": "9012",
        "BRANCH_SERVER_UI_PORT": "9013",
        "BRANCH_SERVER_LOG_LEVEL": "warn",
        "BRANCH_STORAGE_LOCATION": "local://.branch/cluster_2",
        "BRANCH_STORAGE_CREATE": "true",
        "BRANCH_CLI_TABLE_WIDTH": "200",
        "BRANCH_FEATURE_FLAG_TUI": "true",
    }
    with modified_environ(**test_env):
        settings = read_settings(config_path)
        assert settings.server.host == test_env["BRANCH_SERVER_HOST"]
        assert settings.server.port == int(test_env["BRANCH_SERVER_PORT"])
        assert settings.server.ui_port == int(test_env["BRANCH_SERVER_UI_PORT"])
        assert settings.server.log_level == test_env["BRANCH_SERVER_LOG_LEVEL"]
        assert settings.storage.location == test_env["BRANCH_STORAGE_LOCATION"]
        assert settings.storage.create is bool(test_env["BRANCH_STORAGE_CREATE"])
        assert settings.cli.table.width == int(test_env["BRANCH_CLI_TABLE_WIDTH"])
        assert settings.feature_flag.tui is bool(test_env["BRANCH_FEATURE_FLAG_TUI"])
