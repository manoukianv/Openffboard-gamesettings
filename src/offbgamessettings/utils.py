# src/offbgamessettings/utils.py
import os
import shutil

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
