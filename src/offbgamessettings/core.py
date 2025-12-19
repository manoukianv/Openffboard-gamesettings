import os
import platform
import vdf

# List of AppIDs for common sim racing games on Steam
SIM_RACING_APP_IDS = {
    "244210": "Assetto Corsa",
    "805550": "Assetto Corsa Competizione",
    "378860": "Project CARS 2",
    "365960": "rFactor 2",
    "211500": "RaceRoom Racing Experience",
    "310560": "DiRT Rally",
    "690790": "DiRT Rally 2.0",
    "234630": "BeamNG.drive",
    "322500": "Wreckfest",
    "2399420": "Le Mans Ultimate",
    "1849250": "EA SPORTS WRC",
    "480": "Spacewar" # Often used for testing, good for development
}

def _get_steam_path_windows():
    """Find Steam installation path on Windows from the registry."""
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam")
        return winreg.QueryValueEx(key, "SteamPath")[0]
    except (ImportError, FileNotFoundError):
        return None

def _get_steam_path_linux():
    """Find Steam installation path on Linux."""
    home = os.path.expanduser("~")
    paths_to_check = [
        os.path.join(home, ".steam/steam"),
        os.path.join(home, ".local/share/Steam"),
    ]
    for path in paths_to_check:
        if os.path.isdir(path):
            return path
    return None

def find_steam_path():
    """
    Find the root path of the Steam installation based on the OS.
    
    Returns:
        str: The absolute path to the Steam directory, or None if not found.
    """
    os_name = platform.system()
    if os_name == "Windows":
        return _get_steam_path_windows()
    elif os_name == "Linux":
        return _get_steam_path_linux()
    else:
        return None

def get_sim_racing_game_folders():
    """
    Finds and returns the installation folders of sim racing games installed via Steam.

    Returns:
        dict: A dictionary mapping game names to their installation paths.
    """
    steam_path = find_steam_path()
    if not steam_path:
        return {}

    library_folders_path = os.path.join(steam_path, "steamapps", "libraryfolders.vdf")

    if not os.path.exists(library_folders_path):
        return {}
    
    with open(library_folders_path, "r", encoding="utf-8") as f:
        try:
            library_folders = vdf.load(f)["libraryfolders"]
        except (KeyError, vdf.VDFMalformedError):
            return {}

    game_folders = {}
    steam_library_paths = [steam_path] + [
        data["path"] for _, data in library_folders.items() if "path" in data
    ]

    for library_path in steam_library_paths:
        steamapps_path = os.path.join(library_path, "steamapps")
        if not os.path.isdir(steamapps_path):
            continue

        for item in os.listdir(steamapps_path):
            if item.startswith("appmanifest_") and item.endswith(".acf"):
                app_id = item.split("_")[1].split(".")[0]
                if app_id in SIM_RACING_APP_IDS:
                    acf_path = os.path.join(steamapps_path, item)
                    with open(acf_path, "r", encoding="utf-8") as f:
                        try:
                            acf_data = vdf.load(f)["AppState"]
                        except (KeyError, vdf.VDFMalformedError):
                            continue
                    
                    game_name = acf_data.get("name")
                    install_dir = acf_data.get("installdir")
                    
                    if game_name and install_dir:
                        game_path = os.path.join(steamapps_path, "common", install_dir)
                        if os.path.isdir(game_path):
                            game_folders[game_name] = game_path

    return game_folders
