"""
Configurator for rFactor 2.

This module handles the specific configuration for rFactor 2, which requires
special attention to the direction of force feedback (FFB).

Configuration rule (Controller.JSON file):
- The value of the 'Steering effects strength' parameter must be negative to
  be compatible with the OpenFFBoard. A positive value results in
  inverted force feedback (the wheel turns in the wrong direction).
- If a positive value is detected, the configurator prompts the user
  to apply the correction.
- The correction simply consists of inverting the sign of the value
  (e.g., 8000 becomes -8000).
"""
import json
import os
import shutil

from .. import console_ui
from ..utils import backup_file
from .base_configurator import BaseGameConfigurator


class Rfactor2Configurator(BaseGameConfigurator):
    def _get_controller_json_path(self):
        """
        Builds the path to the `Controller.JSON` file.

        Returns:
            str: The absolute path to the configuration file.
        """
        return os.path.join(self.game_path, "UserData", "player", "Controller.JSON")

    def check_and_configure(self):
        """
        Checks and corrects the value of 'Steering effects strength' in
        the `Controller.JSON` file.
        """
        controller_json_path = self._get_controller_json_path()

        if not os.path.exists(controller_json_path):
            self.logs.append(
                {
                    "status": "WARNING",
                    "message": "Controller.JSON file not found. The user profile may not have been created yet.",
                }
            )
            self.status = "WARNING"
            return {"status": self.status, "logs": self.logs}

        try:
            with open(controller_json_path, "r+", encoding="utf-8") as f:
                data = json.load(f)
                strength = data.get("Steering effects strength", 0)

                # If the force is positive, it must be inverted
                if strength > 0:
                    self.logs.append(
                        {
                            "status": "INFO",
                            "message": f"The value of 'Steering effects strength' is positive ({strength}).",
                        }
                    )
                    # Ask for user confirmation before modifying
                    choice = console_ui.ask_user(
                        "Do you want to apply the recommended negative value? (y/n): "
                    ).lower()

                    if choice == "y":
                        if backup_file(controller_json_path):
                            self.logs.append(
                                {
                                    "status": "INFO",
                                    "message": "Backup of Controller.JSON created.",
                                }
                            )
                            # Invert the value and rewrite the JSON file
                            data["Steering effects strength"] = -strength
                            f.seek(0)
                            json.dump(data, f, indent=2)
                            f.truncate()
                            self.logs.append(
                                {
                                    "status": "MODIFIED",
                                    "message": "The value of 'Steering effects strength' has been inverted.",
                                }
                            )
                            self.status = "MODIFIED"
                        else:
                            self.logs.append(
                                {
                                    "status": "ERROR",
                                    "message": "Failed to create backup for Controller.JSON.",
                                }
                            )
                            self.status = "ERROR"
                    else:
                        self.logs.append(
                            {
                                "status": "INFO",
                                "message": "Modification skipped at the user's request.",
                            }
                        )
                else:
                    self.logs.append(
                        {
                            "status": "OK",
                            "message": "The value of 'Steering effects strength' is already configured correctly.",
                        }
                    )

        except json.JSONDecodeError:
            self.logs.append(
                {
                    "status": "ERROR",
                    "message": f"Failed to parse {os.path.basename(controller_json_path)}. The file may be corrupt.",
                }
            )
            self.status = "ERROR"
        except Exception as e:
            self.logs.append(
                {"status": "ERROR", "message": f"An unexpected error occurred: {e}"}
            )
            self.status = "ERROR"

        return {"status": self.status, "logs": self.logs}

    def revert_configuration(self):
        """
        Restores `Controller.JSON` from the backup.
        """
        controller_json_path = self._get_controller_json_path()
        backup_path = controller_json_path + ".bak_offb_settings"

        if os.path.exists(backup_path):
            try:
                shutil.copy2(backup_path, controller_json_path)
                self.logs.append(
                    {
                        "status": "RESTORED",
                        "message": f"{os.path.basename(controller_json_path)} restored from backup.",
                    }
                )
                self.status = "RESTORED"
            except IOError:
                self.logs.append(
                    {
                        "status": "ERROR",
                        "message": f"Failed to restore {os.path.basename(controller_json_path)}.",
                    }
                )
                self.status = "ERROR"
        else:
            self.logs.append(
                {"status": "INFO", "message": "No backup found to restore."}
            )
            self.status = "NOT FOUND"

        return {"status": self.status, "logs": self.logs}
