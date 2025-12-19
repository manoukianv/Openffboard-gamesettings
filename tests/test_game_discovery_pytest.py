import os

import vdf

from offbgamessettings.game_discovery import get_sim_racing_game_folders


def write_vdf_library(path, libraries):
    # Build a VDF-like structure for the test
    data = {"libraryfolders": {}}
    for i, lib in enumerate(libraries):
        data["libraryfolders"][str(i)] = {"path": str(lib)}
    path.write_text(vdf.dumps(data))


def write_acf(path, appid, name, installdir):
    acf = {"AppState": {"appid": appid, "name": name, "installdir": installdir}}
    path.write_text(vdf.dumps(acf))


def test_get_sim_racing_game_folders_basic(tmp_path, monkeypatch):
    # Create fake steam installation
    steam = tmp_path / "Steam"
    steamapps = steam / "steamapps"
    common = steamapps / "common" / "assettocorsa"
    common.mkdir(parents=True)
    steamapps.mkdir(parents=True, exist_ok=True)

    # libraryfolders.vdf
    lib_vdf = steamapps / "libraryfolders.vdf"
    write_vdf_library(lib_vdf, [steam])

    # appmanifest
    manifest = steamapps / "appmanifest_244210.acf"
    write_acf(manifest, "244210", "Assetto Corsa", "assettocorsa")

    monkeypatch.setattr(
        "offbgamessettings.game_discovery.find_steam_path", lambda: str(steam)
    )

    games = get_sim_racing_game_folders()

    assert "244210" in games
    assert games["244210"]["name"] == "Assetto Corsa"
    assert games["244210"]["path"].endswith(
        os.path.join("steamapps", "common", "assettocorsa")
    )


def test_get_sim_racing_game_folders_no_steam(monkeypatch):
    monkeypatch.setattr(
        "offbgamessettings.game_discovery.find_steam_path", lambda: None
    )
    assert get_sim_racing_game_folders() == {}


def test_get_sim_racing_game_folders_malformed_vdf(tmp_path, monkeypatch):
    steam = tmp_path / "Steam"
    steamapps = steam / "steamapps"
    steamapps.mkdir(parents=True)

    lib_vdf = steamapps / "libraryfolders.vdf"
    lib_vdf.write_text("not a vdf")

    monkeypatch.setattr(
        "offbgamessettings.game_discovery.find_steam_path", lambda: str(steam)
    )

    assert get_sim_racing_game_folders() == {}
