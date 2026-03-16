from aiod.configuration._config import Config
from aiod.configuration import config
from aiod.calls.urls import server_url


# --- Default values (after conftest override) ---


def test_api_server_overridden_by_conftest():
    assert config.api_server == "http://not.set/"


def test_version_overridden_by_conftest():
    assert config.version == "not_set"


def test_auth_server_overridden_by_conftest():
    assert config.auth_server == "http://not.set/"


def test_realm_overridden_by_conftest():
    assert config.realm == "not_set"


def test_client_id_overridden_by_conftest():
    assert config.client_id == "not_set"


# --- Config dataclass defaults ---


def test_fresh_config_has_correct_defaults():
    """A fresh Config() instance should have production defaults."""
    fresh = Config()
    assert fresh.api_server == "https://api.aiod.eu/"
    assert fresh.version == "v2"
    assert fresh.auth_server == "https://auth.aiod.eu/aiod-auth/"
    assert fresh.realm == "aiod"
    assert fresh.client_id == "aiod-sdk"
    assert fresh.request_timeout_seconds == 10


# --- Config attribute changes ---


def test_api_server_can_be_changed():
    config.api_server = "http://localhost:8000/"
    assert config.api_server == "http://localhost:8000/"


def test_version_can_be_changed():
    config.version = "v1"
    assert config.version == "v1"


def test_request_timeout_can_be_changed():
    config.request_timeout_seconds = 30
    assert config.request_timeout_seconds == 30


# --- server_url() ---


def test_server_url_with_test_defaults():
    url = server_url()
    assert url == "http://not.set/not_set/"


def test_server_url_reflects_config_changes():
    config.api_server = "http://example.com/"
    config.version = "v2"
    url = server_url()
    assert url == "http://example.com/v2/"


def test_server_url_with_explicit_version_parameter():
    """server_url(version='v3') should override config.version."""
    url = server_url(version="v3")
    assert "v3" in url


def test_server_url_with_empty_version():
    """Empty version string is falsy - should return api_server without version."""
    config.api_server = "http://example.com/"
    url = server_url(version="")
    assert url == "http://example.com/"


# --- Observer pattern ---


def test_observer_is_called_on_attribute_change():
    """Config.__setattr__ should notify registered observers."""
    changes = []
    config.subscribe("version", lambda key, old, new: changes.append((old, new)))
    old_version = config.version
    config.version = "v99"
    assert len(changes) == 1
    assert changes[0] == (old_version, "v99")


# --- _use_localhost convenience ---


def test_use_localhost_sets_local_urls():
    config._use_localhost()
    assert config.api_server == "http://localhost/"
    assert config.auth_server == "http://localhost/aiod-auth/"
    assert config.version == ""


def test_use_localhost_with_custom_version():
    config._use_localhost(version="v1")
    assert config.version == "v1"
