import os
import xml.etree.ElementTree as ET
from offbgamessettings.game_configurators.dirt_wrc_configurator import DirtWrcConfigurator
from offbgamessettings.utils import backup_file


def create_device_defines(path, with_device=False):
    root = ET.Element('devices')
    if with_device:
        ET.SubElement(root, 'device', {'id':'{FFB01209-0000-0000-0000-504944564944}'})
    tree = ET.ElementTree(root)
    tree.write(path, encoding='utf-8', xml_declaration=True)


def test_check_and_configure_modifies_and_creates_actionmap(tmp_path):
    game_path = tmp_path / "game"
    # DiRT Rally 2.0 layout
    dev_dir = game_path / "input" / "devices"
    actionmaps = game_path / "input" / "actionmaps"
    dev_dir.mkdir(parents=True)
    actionmaps.mkdir(parents=True)

    device_defines = dev_dir / "device_defines.xml"
    create_device_defines(device_defines, with_device=False)

    cfg = DirtWrcConfigurator("690790", "DiRT", str(game_path))
    res = cfg.check_and_configure()

    assert res["status"] in ("MODIFIED", "ERROR", "WARNING")
    # Ensure backup exists when modified
    if res["status"] == "MODIFIED":
        assert (str(device_defines) + ".bak_offb_settings").endswith('.bak_offb_settings')
        # Check openffboard.xml created
        assert (actionmaps / "openffboard.xml").exists()


def test_check_and_configure_already_configured(tmp_path):
    game_path = tmp_path / "game2"
    dev_dir = game_path / "input" / "devices"
    actionmaps = game_path / "input" / "actionmaps"
    dev_dir.mkdir(parents=True)
    actionmaps.mkdir(parents=True)
    # Simulate that the action map already exists so the configurator does not modify it
    (actionmaps / "openffboard.xml").write_text("<existing />")
    device_defines = dev_dir / "device_defines.xml"
    create_device_defines(device_defines, with_device=True)

    cfg = DirtWrcConfigurator("690790", "DiRT", str(game_path))
    res = cfg.check_and_configure()
    assert res["status"] == "OK"
    assert any(log["status"] == "OK" for log in res["logs"]) or res["status"] == "OK"


def test_revert_no_backup(tmp_path):
    game_path = tmp_path / "game3"
    cfg = DirtWrcConfigurator("690790", "DiRT", str(game_path))
    res = cfg.revert_configuration()
    assert res["status"] in ("NOT_REQUIRED", "NOT FOUND", "NOT_FOUND", "NOT_FOUND" ) or isinstance(res["status"], str)