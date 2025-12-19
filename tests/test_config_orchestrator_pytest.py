from types import SimpleNamespace
from offbgamessettings import config_orchestrator


def test_check_and_configure_with_configurator(monkeypatch):
    fake_conf = SimpleNamespace(check_and_configure=lambda: {"status":"MODIFIED","logs":[]})
    monkeypatch.setattr('offbgamessettings.config_orchestrator.ConfiguratorFactory.get_configurator', lambda app_id, name, path: fake_conf)

    games = {"123": {"name":"GameX","path":"/tmp/gamex"}}
    res = config_orchestrator.check_and_configure_games(games)
    assert "GameX" in res
    assert res["GameX"]["status"] == "MODIFIED"


def test_check_and_configure_no_configurator(monkeypatch):
    monkeypatch.setattr('offbgamessettings.config_orchestrator.ConfiguratorFactory.get_configurator', lambda app_id, name, path: None)
    games = {"123": {"name":"GameY","path":"/tmp/gamey"}}
    res = config_orchestrator.check_and_configure_games(games)
    assert res["GameY"]["status"] == "NOT REQUIRED"


def test_revert_configurations(monkeypatch):
    fake_conf = SimpleNamespace(revert_configuration=lambda: {"status":"RESTORED","logs":[]})
    monkeypatch.setattr('offbgamessettings.config_orchestrator.ConfiguratorFactory.get_configurator', lambda app_id, name, path: fake_conf)

    games = {"123": {"name":"GameX","path":"/tmp/gamex"}}
    res = config_orchestrator.revert_configurations(games)
    assert res["GameX"]["status"] == "RESTORED"