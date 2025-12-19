# src/offbgamessettings/__main__.py
import argparse
from offbgamessettings.core import get_sim_racing_game_folders, find_steam_path
from offbgamessettings import config_manager
from offbgamessettings import output

def main():
    """
    Entry point for the command-line interface.
    Finds and configures sim racing games for OpenFFBoard.
    """
    parser = argparse.ArgumentParser(description="OpenFFBoard Game Settings Utility")
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Display detailed information for all checks, including successful modifications."
    )
    parser.add_argument(
        "--revert",
        action="store_true",
        help="Restore original game configuration files from backups."
    )
    args = parser.parse_args()

    output.print_header("OpenFFBoard Game Settings Utility")

    if not find_steam_path():
        output.print_status("ERROR", "Steam installation not found. Please ensure Steam is installed.")
        return

    game_folders = get_sim_racing_game_folders()

    if game_folders:
        if args.revert:
            output.print_header("Reverting Configurations")
            results = config_manager.revert_configurations(game_folders)
        else:
            output.print_header("Configuration Check")
            results = config_manager.check_and_configure_games(game_folders)
        
        output.print_summary_table(results)
        output.print_details(results, verbose=args.verbose)
        
        output.print_header("Process Finished")
    else:
        output.print_status("INFO", "No supported sim racing games found.")

if __name__ == "__main__":
    main()
