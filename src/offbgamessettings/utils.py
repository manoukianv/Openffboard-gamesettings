"""
Miscellaneous file utilities.

This module provides low-level helper functions that are used by
different game configurators, such as creating file backups.
"""
import os
import shutil


def backup_file(file_path):
    """
    Creates a backup of a file by adding a custom extension.

    The backup is a copy of the original file with the
    `.bak_offb_settings` extension added to its name. This naming convention
    makes it easy to identify backups created by this tool.

    Args:
        file_path (str): The absolute path to the file to be backed up.

    Returns:
        bool: True if the backup was created successfully, False otherwise.
    """
    if not os.path.exists(file_path):
        return False

    # Build the backup path
    backup_path = file_path + ".bak_offb_settings"

    try:
        # Copy the original file to the new backup location
        shutil.copy2(file_path, backup_path)
        return True
    except IOError:
        # The copy failed, likely due to permissions
        return False
