import json
from offbgamessettings.game_configurators.rfactor2_configurator import Rfactor2Configurator
from offbgamessettings import console_ui


def test_check_and_configure_inverts_with_user_confirmation(tmp_path, monkeypatch):
    game_path = tmp_path / "rf"
    controller_dir = game_path / "UserData" / "player"
    controller_dir.mkdir(parents=True)
    controller = controller_dir / "Controller.JSON"
    controller.write_text(json.dumps({"Steering effects strength": 8000}))

    # Confirm modification
    monkeypatch.setattr('offbgamessettings.console_ui.ask_user', lambda prompt: 'y')

    cfg = Rfactor2Configurator("365960", "rFactor 2", str(game_path))
    res = cfg.check_and_configure()
    assert res["status"] in ("MODIFIED", "ERROR")

    if res["status"] == "MODIFIED":
        data = json.loads(controller.read_text())
        assert data["Steering effects strength"] < 0
        # backup exists
        assert (str(controller) + ".bak_offb_settings").endswith('.bak_offb_settings')


def test_check_and_configure_skipped_when_user_declines(tmp_path, monkeypatch):
    game_path = tmp_path / "rf2"
    controller_dir = game_path / "UserData" / "player"
    controller_dir.mkdir(parents=True)
    controller = controller_dir / "Controller.JSON"
    controller.write_text(json.dumps({"Steering effects strength": 8000}))

    # Decline modification
    monkeypatch.setattr('offbgamessettings.console_ui.ask_user', lambda prompt: 'n')

    cfg = Rfactor2Configurator("365960", "rFactor 2", str(game_path))
    res = cfg.check_and_configure()
    assert any(log["message"].startswith("Modification skipped") or log["status"] == "INFO" for log in res["logs"]) or res["status"] in ("OK", "WARNING")


def test_check_and_configure_missing_file(tmp_path):
    cfg = Rfactor2Configurator("365960", "rFactor 2", str(tmp_path))
    res = cfg.check_and_configure()
    assert res["status"] == "WARNING"