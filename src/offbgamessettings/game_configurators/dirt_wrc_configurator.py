"""
Configurator for Codemasters games (DiRT series, EA SPORTS WRC).

This module handles the specific configuration required for games developed
by Codemasters, which share a similar input file structure.

Configuration rules:
1.  **device_defines.xml**:
    -   This file must contain an entry for the OpenFFBoard for the
        game to recognize the device.
    -   The configuration adds a `<device>` node with the hardware device ID
        of the OpenFFBoard: `{FFB01209-0000-0000-0000-504944564944}`.
2.  **openffboard.xml**:
    -   An `action map` file must be created in the
        `actionmaps` directory to define how the steering wheel axes are
        used in-game (e.g., steering).
    -   This configurator creates this file if it is missing.

The path to the configuration files varies slightly between games
(e.g., DiRT Rally 2.0 vs. WRC), which is handled by the `_get_paths` method.
"""
import os
import shutil
import xml.etree.ElementTree as ET

from ..utils import backup_file
from .base_configurator import BaseGameConfigurator


class DirtWrcConfigurator(BaseGameConfigurator):
    def _get_paths(self):
        """
        Determines the paths of the configuration files based on the game's AppID.

        Returns:
            tuple: (device_defines_path, actionmaps_path) or (None, None) if
                   the game's AppID is not recognized.
        """
        if self.app_id == "1849250":  # EA SPORTS WRC
            device_path = os.path.join(
                self.game_path,
                "WRC",
                "Content",
                "input",
                "Windows",
                "devices",
                "device_defines.xml",
            )
            actionmaps_path = os.path.join(
                self.game_path,
                "WRC",
                "Content",
                "input",
                "Windows",
                "actionmaps",
            )
            return device_path, actionmaps_path
        elif self.app_id == "690790":  # DiRT Rally 2.0
            device_path = os.path.join(
                self.game_path, "input", "devices", "device_defines.xml"
            )
            actionmaps_path = os.path.join(self.game_path, "input", "actionmaps")
            return device_path, actionmaps_path
        return None, None

    def check_and_configure(self):
        """
        Checks and configures the `device_defines.xml` and `openffboard.xml` files.
        """
        device_defines_path, actionmaps_path = self._get_paths()

        if not device_defines_path or not os.path.exists(device_defines_path):
            self.logs.append(
                {
                    "status": "WARNING",
                    "message": (
                        "Could not find device_defines.xml. The game may be corrupt or "
                        "incomplete."
                    ),
                }
            )
            self.status = "WARNING"
            return {"status": self.status, "logs": self.logs}

        # --- 1. Check and modify device_defines.xml ---
        try:
            tree = ET.parse(device_defines_path)
            root = tree.getroot()
            device_id = "{FFB01209-0000-0000-0000-504944564944}"

            # Check if the OpenFFBoard device node already exists
            if not root.findall(f".//device[@id='{device_id}']"):
                # Back up the file before modifying it
                if backup_file(device_defines_path):
                    self.logs.append(
                        {
                            "status": "INFO",
                            "message": (
                                "Backup of " f"{os.path.basename(device_defines_path)} created."
                            ),
                        }
                    )
                    # Create and add the new device element
                    new_device = ET.Element(
                        "device",
                        {
                            "id": device_id,
                            "name": "openffboard",
                            "priority": "100",
                            "type": "wheel",
                            "official": "false",
                        },
                    )
                    root.append(new_device)
                    tree.write(
                        device_defines_path, encoding="utf-8", xml_declaration=True
                    )
                    self.logs.append(
                        {
                            "status": "MODIFIED",
                            "message": "OpenFFBoard device added to device_defines.xml.",
                        }
                    )
                    self.status = "MODIFIED"
                else:
                    self.logs.append(
                        {
                            "status": "ERROR",
                            "message": (
                                f"Failed to create backup for {os.path.basename(device_defines_path)}."
                            ),
                        }
                    )
                    self.status = "ERROR"
            else:
                self.logs.append(
                    {
                        "status": "OK",
                        "message": (
                            "OpenFFBoard device is already configured in "
                            "device_defines.xml."
                        ),
                    }
                )

        except ET.ParseError:
            self.logs.append(
                {
                    "status": "ERROR",
                    "message": (
                        f"Failed to parse {os.path.basename(device_defines_path)}. "
                        "The file may be corrupt."
                    ),
                }
            )
            self.status = "ERROR"

        # --- 2. Check and create openffboard.xml in actionmaps ---
        if actionmaps_path and os.path.isdir(actionmaps_path):
            openffboard_xml_path = os.path.join(actionmaps_path, "openffboard.xml")
            if not os.path.exists(openffboard_xml_path):
                # XML content for the basic action mapping
                xml_content = (
                    '<action_map name="openffboard" device_name="openffboard" '
                    'library="lib_direct_input">'
                    "<axis_defaults>"
                    '<axis name="di_x_axis">'
                    '<action deadzone="0" name="driving.steer.left" />'
                    '<action deadzone="0" name="driving.steer.right" />'
                    "</axis>"
                    "</axis_defaults>"
                    '<group name="driving">'
                    '<group name="steer">'
                    '<action name="left">'
                    '<axis name="di_x_axis" type="lower" />'
                    "</action>"
                    '<action name="right">'
                    '<axis name="di_x_axis" type="upper" />'
                    "</action>"
                    "</group>"
                    "</group>"
                    "</action_map>"
                )
                try:
                    with open(openffboard_xml_path, "w", encoding="utf-8") as f:
                        f.write(xml_content)
                    self.logs.append(
                        {
                            "status": "MODIFIED",
                            "message": "Action map file openffboard.xml created.",
                        }
                    )
                    if self.status != "ERROR":
                        self.status = "MODIFIED"
                except IOError:
                    self.logs.append(
                        {
                            "status": "ERROR",
                            "message": (
                                "Could not write to openffboard.xml."
                            ),
                        }
                    )
                    self.status = "ERROR"
            else:
                self.logs.append(
                    {
                        "status": "OK",
                        "message": "Action map file openffboard.xml already exists.",
                    }
                )
        else:
            self.logs.append(
                {"status": "WARNING", "message": "Actionmaps directory not found."}
            )
            if self.status not in ["ERROR", "MODIFIED"]:
                self.status = "WARNING"

        return {"status": self.status, "logs": self.logs}

    def revert_configuration(self):
        """
        Restores `device_defines.xml` from the backup.

        Note: The `openffboard.xml` file is not deleted because it
        does not overwrite any existing files, and its deletion is not critical.
        """
        device_defines_path, _ = self._get_paths()

        if not device_defines_path:
            self.status = "NOT REQUIRED"
            return {"status": self.status, "logs": self.logs}

        backup_path = device_defines_path + ".bak_offb_settings"
        if os.path.exists(backup_path):
            try:
                shutil.copy2(backup_path, device_defines_path)
                self.logs.append(
                    {
                        "status": "RESTORED",
                        "message": (
                            f"{os.path.basename(device_defines_path)} restored "
                            "from backup."
                        ),
                    }
                )
                self.status = "RESTORED"
            except IOError:
                self.logs.append(
                    {
                        "status": "ERROR",
                        "message": (
                            "Failed to restore "
                            f"{os.path.basename(device_defines_path)}."
                        ),
                    }
                )
                self.status = "ERROR"
        else:
            self.logs.append(
                {"status": "INFO", "message": "No backup found to restore."}
            )
            self.status = "NOT FOUND"

        return {"status": self.status, "logs": self.logs}
