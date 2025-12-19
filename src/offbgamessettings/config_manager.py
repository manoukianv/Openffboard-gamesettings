# src/offbgamessettings/config_manager.py
import os
import shutil
import xml.etree.ElementTree as ET
import json
from . import output

def backup_file(file_path):
    """Creates a backup of a file. Returns True on success, False on failure."""
    if not os.path.exists(file_path):
        return False
    backup_path = file_path + ".bak_offb_settings"
    try:
        shutil.copy2(file_path, backup_path)
        return True
    except IOError:
        return False

def configure_dirt_wrc(game_name, game_path):
    """Configures DiRT series and EA WRC games."""
    logs = []
    status = "OK"

    device_defines_path = ""
    actionmaps_path = ""

    if "EA SPORTS™ WRC" in game_name:
        device_defines_path = os.path.join(game_path, "WRC", "Content", "input", "Windows", "devices", "device_defines.xml")
        actionmaps_path = os.path.join(game_path, "WRC", "Content", "input", "Windows", "actionmaps")
    elif "DiRT Rally 2.0" in game_name:
        device_defines_path = os.path.join(game_path, "input", "devices", "device_defines.xml")
        actionmaps_path = os.path.join(game_path, "input", "actionmaps")

    if not os.path.exists(device_defines_path):
        logs.append({"status": "WARNING", "message": "Could not find device_defines.xml. Skipping."})
        return {"status": "WARNING", "logs": logs}

    # --- 1. Check and modify device_defines.xml ---
    try:
        tree = ET.parse(device_defines_path)
        root = tree.getroot()
        device_id = "{FFB01209-0000-0000-0000-504944564944}"
        
        if not root.findall(f"device[@id='{device_id}']"):
            if backup_file(device_defines_path):
                logs.append({"status": "INFO", "message": f"Backup of {os.path.basename(device_defines_path)} created."})
                new_device = ET.Element("device", {"id": device_id, "name": "openffboard", "priority": "100", "type": "wheel", "official": "false"})
                root.append(new_device)
                tree.write(device_defines_path, encoding="utf-8", xml_declaration=True)
                logs.append({"status": "MODIFIED", "message": "Added OpenFFBoard device to device_defines.xml."})
                status = "MODIFIED"
            else:
                logs.append({"status": "ERROR", "message": f"Failed to create backup for {os.path.basename(device_defines_path)}."})
                status = "ERROR"
        else:
            logs.append({"status": "OK", "message": "OpenFFBoard device is already configured in device_defines.xml."})

    except ET.ParseError:
        logs.append({"status": "ERROR", "message": f"Failed to parse {os.path.basename(device_defines_path)}. File may be corrupted."})
        status = "ERROR"

    # --- 2. Check and create openffboard.xml in actionmaps ---
    if os.path.isdir(actionmaps_path):
        openffboard_xml_path = os.path.join(actionmaps_path, "openffboard.xml")
        if not os.path.exists(openffboard_xml_path):
            xml_content = """<action_map name="openffboard" device_name="openffboard" library="lib_direct_input"><axis_defaults><axis name="di_x_axis"><action deadzone="0" name="driving.steer.left" /><action deadzone="0" name="driving.steer.right" /></axis></axis_defaults><group name="driving"><group name="steer"><action name="left"><axis name="di_x_axis" type="lower" /></action><action name="right"><axis name="di_x_axis" type="upper" /></action></group></group></action_map>"""
            try:
                with open(openffboard_xml_path, "w", encoding="utf-8") as f:
                    f.write(xml_content)
                logs.append({"status": "MODIFIED", "message": "Created openffboard.xml action map."})
                if status != "ERROR": status = "MODIFIED"
            except IOError:
                logs.append({"status": "ERROR", "message": "Could not write openffboard.xml."})
                status = "ERROR"
        else:
            logs.append({"status": "OK", "message": "openffboard.xml action map already exists."})
    else:
        logs.append({"status": "WARNING", "message": "Actionmaps directory not found."})
        if status not in ["ERROR", "MODIFIED"]: status = "WARNING"

    return {"status": status, "logs": logs}

def configure_rfactor2(game_name, game_path):
    """Configures rFactor 2."""
    logs = []
    status = "OK"
    
    controller_json_path = os.path.join(game_path, "UserData", "player", "Controller.JSON")

    if not os.path.exists(controller_json_path):
        logs.append({"status": "WARNING", "message": "Controller.JSON not found. Skipping."})
        return {"status": "WARNING", "logs": logs}

    try:
        with open(controller_json_path, "r+", encoding="utf-8") as f:
            data = json.load(f)
            strength = data.get("Steering effects strength", 0)
            
            if strength > 0:
                logs.append({"status": "INFO", "message": f"'Steering effects strength' is positive ({strength})."})
                choice = output.ask_user("Do you want to apply the recommended negative value? (y/n):").lower()
                
                if choice == 'y':
                    if backup_file(controller_json_path):
                        logs.append({"status": "INFO", "message": "Backup of Controller.JSON created."})
                        data["Steering effects strength"] = -strength
                        f.seek(0)
                        json.dump(data, f, indent=2)
                        f.truncate()
                        logs.append({"status": "MODIFIED", "message": "Reversed 'Steering effects strength'."})
                        status = "MODIFIED"
                    else:
                        logs.append({"status": "ERROR", "message": "Failed to create backup for Controller.JSON."})
                        status = "ERROR"
                else:
                    logs.append({"status": "INFO", "message": "Skipping modification as requested."})
            else:
                logs.append({"status": "OK", "message": "'Steering effects strength' is already configured correctly."})

    except json.JSONDecodeError:
        logs.append({"status": "ERROR", "message": f"Failed to parse {os.path.basename(controller_json_path)}. File may be corrupted."})
        status = "ERROR"
    except Exception as e:
        logs.append({"status": "ERROR", "message": f"An unexpected error occurred: {e}"})
        status = "ERROR"
        
    return {"status": status, "logs": logs}

def show_f1_recommendations(game_name):
    """Returns recommendations for F1 games."""
    logs = [
        {"status": "INFO", "message": "This game requires manual in-game adjustments."},
        {"status": "INFO", "message": "Disable all steering assists."},
        {"status": "INFO", "message": "Set steering range to 360 degrees in OpenFFBoard."}
    ]
    return {"status": "INFO", "logs": logs}

def show_wrc_series_recommendations(game_name):
    """Returns recommendations for WRC series (8, Generations)."""
    logs = [
        {"status": "INFO", "message": "This game requires manual in-game adjustments."},
        {"status": "INFO", "message": "Set steering range to 540 degrees in OpenFFBoard."},
        {"status": "INFO", "message": "Adjust Spring gain in-game (10 to max)."}
    ]
    return {"status": "INFO", "logs": logs}

def check_and_configure_games(game_folders):
    """Checks and configures all detected games, returning the results."""
    results = {}
    for game_name, game_path in game_folders.items():
        if "DiRT" in game_name or ("WRC" in game_name and "EA SPORTS" in game_name):
            results[game_name] = configure_dirt_wrc(game_name, game_path)
        elif "rFactor 2" in game_name:
            results[game_name] = configure_rfactor2(game_name, game_path)
        elif "F1" in game_name:
            results[game_name] = show_f1_recommendations(game_name)
        elif "WRC 8" in game_name or "WRC Generations" in game_name:
            results[game_name] = show_wrc_series_recommendations(game_name)
        else:
            results[game_name] = {"status": "NOT REQUIRED", "logs": []}
    return results

def revert_configurations(game_folders):
    """Finds and restores backups for all detected games."""
    results = {}
    for game_name, game_path in game_folders.items():
        logs = []
        
        config_files = []
        if "EA SPORTS™ WRC" in game_name:
            config_files.append(os.path.join(game_path, "WRC", "Content", "input", "Windows", "devices", "device_defines.xml"))
        elif "DiRT Rally 2.0" in game_name:
            config_files.append(os.path.join(game_path, "input", "devices", "device_defines.xml"))
        elif "rFactor 2" in game_name:
            config_files.append(os.path.join(game_path, "UserData", "player", "Controller.JSON"))
            
        if not config_files:
            results[game_name] = {"status": "NOT REQUIRED", "logs": []}
            continue

        files_restored = 0
        files_with_errors = 0
        backups_found = 0

        for file_path in config_files:
            backup_path = file_path + ".bak_offb_settings"
            if os.path.exists(backup_path):
                backups_found += 1
                try:
                    shutil.copy2(backup_path, file_path)
                    logs.append({"status": "RESTORED", "message": f"Restored {os.path.basename(file_path)} from backup."})
                    files_restored += 1
                except IOError:
                    logs.append({"status": "ERROR", "message": f"Failed to restore {os.path.basename(file_path)}."})
                    files_with_errors += 1
        
        final_status = "OK"
        if files_with_errors > 0:
            final_status = "ERROR"
        elif files_restored > 0:
            final_status = "RESTORED"
        elif backups_found == 0:
            final_status = "NOT FOUND"
            logs.append({"status": "INFO", "message": "No backups found to restore."})

        results[game_name] = {"status": final_status, "logs": logs}
        
    return results

