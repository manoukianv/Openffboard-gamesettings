import os
import unittest
from unittest.mock import mock_open, patch

from offbgamessettings.game_discovery import (
    find_steam_path,
    get_sim_racing_game_folders,
)

# Sample VDF content for libraryfolders.vdf
MOCK_LIBRARYFOLDERS_VDF = """
"libraryfolders"
{
    "0"
    {
        "path"		"C:\\\\Program Files (x86)\\\\Steam"
        "label"		""
        "contentid"		"..."
        "totalsize"		"..."
        // ... other fields
    }
    "1"
    {
        "path"		"D:\\\\SteamLibrary"
        "label"		"My Other Library"
        // ... other fields
    }
}
"""

# Sample ACF content for a sim racing game
MOCK_APPMANIFEST_244210_ACF = """
"AppState"
{
    "appid"		"244210"
    "name"		"Assetto Corsa"
    "installdir"	"assettocorsa"
    // ... other fields
}
"""


class TestSimRacingGames(unittest.TestCase):
    @patch("platform.system")
    @patch(
        "offbgamessettings.game_discovery._get_steam_path_windows",
        return_value="C:\\Steam",
    )
    @patch(
        "offbgamessettings.game_discovery._get_steam_path_linux",
        return_value="/home/user/.steam/steam",
    )
    def test_find_steam_path(self, mock_linux, mock_windows, mock_system):
        """Test find_steam_path for different OS."""
        mock_system.return_value = "Windows"
        self.assertEqual(find_steam_path(), "C:\\Steam")

        mock_system.return_value = "Linux"
        self.assertEqual(find_steam_path(), "/home/user/.steam/steam")

        mock_system.return_value = "Darwin"  # Unsupported OS
        self.assertIsNone(find_steam_path())

    @patch(
        "offbgamessettings.game_discovery.find_steam_path", return_value="/fake/steam"
    )
    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open)
    @patch("os.listdir")
    @patch("os.path.isdir")
    def test_get_sim_racing_game_folders(
        self, mock_isdir, mock_listdir, mock_open_func, mock_exists, mock_find_steam
    ):
        """Test the main function to find sim racing game folders."""
        # Setup mocks
        mock_exists.return_value = True
        mock_isdir.return_value = True

        # Mock file system layout and contents
        mock_open_func.side_effect = [
            mock_open(
                read_data=MOCK_LIBRARYFOLDERS_VDF
            ).return_value,  # libraryfolders.vdf
            mock_open(
                read_data=MOCK_APPMANIFEST_244210_ACF
            ).return_value,  # appmanifest_244210.acf in first library
            mock_open(
                read_data=MOCK_APPMANIFEST_244210_ACF
            ).return_value,  # appmanifest_244210.acf in second library
        ]

        # Mock directory listing to find the manifest only in the main library
        def listdir_side_effect(path):
            if path == os.path.join("/fake/steam", "steamapps"):
                return ["appmanifest_244210.acf", "some_other_file.txt"]
            return []

        mock_listdir.side_effect = listdir_side_effect

        # Expected result
        expected_folders = {
            "244210": {
                "name": "Assetto Corsa",
                "path": os.path.join(
                    "/fake/steam", "steamapps", "common", "assettocorsa"
                ),
            }
        }

        # Run the function
        game_folders = get_sim_racing_game_folders()

        # Assertions
        self.assertEqual(game_folders, expected_folders)
        mock_open_func.assert_any_call(
            os.path.join("/fake/steam", "steamapps", "libraryfolders.vdf"),
            "r",
            encoding="utf-8",
        )
        mock_open_func.assert_any_call(
            os.path.join("/fake/steam", "steamapps", "appmanifest_244210.acf"),
            "r",
            encoding="utf-8",
        )


if __name__ == "__main__":
    unittest.main()
