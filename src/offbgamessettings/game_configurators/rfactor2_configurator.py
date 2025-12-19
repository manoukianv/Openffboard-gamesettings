"""
Configurator for rFactor 2.

This module handles the specific configuration for rFactor 2, which may
require inverting the Force Feedback (FFB) strength.

Configuration Rule (Controller.JSON):
- The 'Steering effects strength' value should be negative for OpenFFBoard.
- If the value is found to be positive, the user is prompted to apply the fix.
- The fix consists of inverting the value (e.g., 8000 becomes -8000).
"""
# src/offbgamessettings/game_configurators/rfactor2_configurator.py
import os
import json
import shutil
from .base_configurator import BaseGameConfigurator
from ..utils import backup_file
from .. import output

class Rfactor2Configurator(BaseGameConfigurator):
    
    def _get_controller_json_path(self):
        return os.path.join(self.game_path, "UserData", "player", "Controller.JSON")

    def check_and_configure(self):
        controller_json_path = self._get_controller_json_path()

        if not os.path.exists(controller_json_path):
            self.logs.append({"status": "WARNING", "message": "Controller.JSON not found. Skipping."})
            self.status = "WARNING"
            return {"status": self.status, "logs": self.logs}

        try:
            with open(controller_json_path, "r+", encoding="utf-8") as f:
                data = json.load(f)
                strength = data.get("Steering effects strength", 0)
                
                if strength > 0:
                    self.logs.append({"status": "INFO", "message": f"'Steering effects strength' is positive ({strength})."})
                    choice = output.ask_user("Do you want to apply the recommended negative value? (y/n):").lower()
                    
                    if choice == 'y':
                        if backup_file(controller_json_path):
                            self.logs.append({"status": "INFO", "message": "Backup of Controller.JSON created."})
                            data["Steering effects strength"] = -strength
                            f.seek(0)
                            json.dump(data, f, indent=2)
                            f.truncate()
                            self.logs.append({"status": "MODIFIED", "message": "Reversed 'Steering effects strength'."})
                            self.status = "MODIFIED"
                        else:
                            self.logs.append({"status": "ERROR", "message": "Failed to create backup for Controller.JSON."})
                            self.status = "ERROR"
                    else:
                        self.logs.append({"status": "INFO", "message": "Skipping modification as requested."})
                else:
                    self.logs.append({"status": "OK", "message": "'Steering effects strength' is already configured correctly."})

        except json.JSONDecodeError:
            self.logs.append({"status": "ERROR", "message": f"Failed to parse {os.path.basename(controller_json_path)}. File may be corrupted."})
            self.status = "ERROR"
        except Exception as e:
            self.logs.append({"status": "ERROR", "message": f"An unexpected error occurred: {e}"})
            self.status = "ERROR"
            
        return {"status": self.status, "logs": self.logs}

    def revert_configuration(self):
        controller_json_path = self._get_controller_json_path()
        backup_path = controller_json_path + ".bak_offb_settings"

        if os.path.exists(backup_path):
            try:
                shutil.copy2(backup_path, controller_json_path)
                self.logs.append({"status": "RESTORED", "message": f"Restored {os.path.basename(controller_json_path)} from backup."})
                self.status = "RESTORED"
            except IOError:
                self.logs.append({"status": "ERROR", "message": f"Failed to restore {os.path.basename(controller_json_path)}."})
                self.status = "ERROR"
        else:
            self.logs.append({"status": "INFO", "message": "No backup found to restore."})
            self.status = "NOT FOUND"
            
        return {"status": self.status, "logs": self.logs}
