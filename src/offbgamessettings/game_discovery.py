"""
Game and Steam Installation Discovery.

This module is responsible for locating the user's Steam installation
(on Windows and Linux) and identifying installed sim racing games.

How it works:
1.  `find_steam_path()`: Attempts to find the Steam root directory using
    OS-specific methods (Windows registry, common Linux paths).
2.  `get_sim_racing_game_folders()`:
    -   Reads Steam's `libraryfolders.vdf` file to find all game library
        folders.
    -   Scans each library folder for `appmanifest_*.acf` files.
    -   Filters these manifests using a predefined list of sim racing game
        AppIDs (`SIM_RACING_APP_IDS`).
    -   Extracts the game name and installation path from each matching
        manifest.
    -   Returns a structured dictionary containing the information of the
        found games.
"""
import os
import platform
import vdf

# Dictionary of Steam AppIDs for popular sim racing games.
# This list is used to filter installed games and only act on relevant titles.
# The key is the Steam AppID, the value is the game's name.
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
    "480": "Spacewar" # Often used for testing, useful for development
}

def _get_steam_path_windows():
    """
    Finds the Steam installation path on Windows via the registry.

    Returns:
        str or None: The absolute path to the Steam directory, or None if not found.
    """
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam")
        return winreg.QueryValueEx(key, "SteamPath")[0]
    except (ImportError, FileNotFoundError):
        return None

def _get_steam_path_linux():
    """
    Finds the Steam installation path on Linux by checking common locations.

    Returns:
        str or None: The absolute path to the Steam directory, or None if not found.
    """
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
    Finds the root path of the Steam installation based on the OS.

    This function acts as a dispatcher for the OS-specific search functions.

    Returns:
        str or None: The absolute path to the Steam directory, or None if not found.
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

    The process involves reading Steam libraries, finding game manifests, and
    filtering by the relevant AppIDs.

    Returns:
        dict: A dictionary where each key is a game AppID and the value is
              another dictionary containing the 'name' and 'path' of the game.
              Ex: {'244210': {'name': 'Assetto Corsa', 'path': '...'}}
    """
    steam_path = find_steam_path()
    if not steam_path:
        return {}

    library_folders_path = os.path.join(steam_path, "steamapps", "libraryfolders.vdf")

    if not os.path.exists(library_folders_path):
        return {}
    
    with open(library_folders_path, "r", encoding="utf-8") as f:
        try:
            # Load the VDF file that lists all Steam libraries
            library_folders = vdf.load(f)["libraryfolders"]
        except (KeyError, vdf.VDFMalformedError):
            return {}

    games_found = {}
    # Include the main Steam folder as well as all other library folders
    steam_library_paths = [steam_path] + [
        data["path"] for _, data in library_folders.items() if "path" in data
    ]

    for library_path in steam_library_paths:
        steamapps_path = os.path.join(library_path, "steamapps")
        if not os.path.isdir(steamapps_path):
            continue

        # Iterate through all files in the steamapps folder
        for item in os.listdir(steamapps_path):
            if item.startswith("appmanifest_") and item.endswith(".acf"):
                # Extract the AppID from the filename (e.g., appmanifest_244210.acf)
                app_id = item.split("_")[1].split(".")[0]
                if app_id in SIM_RACING_APP_IDS:
                    acf_path = os.path.join(steamapps_path, item)
                    with open(acf_path, "r", encoding="utf-8") as f:
                        try:
                            # Load the game manifest to get details
                            acf_data = vdf.load(f)["AppState"]
                        except (KeyError, vdf.VDFMalformedError):
                            continue
                    
                    game_name = acf_data.get("name")
                    install_dir = acf_data.get("installdir")
                    
                    if game_name and install_dir:
                        game_path = os.path.join(steamapps_path, "common", install_dir)
                        if os.path.isdir(game_path):
                            # Add the found game to the results dictionary
                            games_found[app_id] = {"name": game_name, "path": game_path}
                            
    return games_found
