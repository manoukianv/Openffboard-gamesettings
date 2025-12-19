# src/offbgamessettings/__main__.py
import argparse
from offbgamessettings.game_discovery import get_sim_racing_game_folders, find_steam_path
from offbgamessettings import config_orchestrator
from offbgamessettings import console_ui

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

    console_ui.print_header("OpenFFBoard Game Settings Utility")

    if not find_steam_path():
        console_ui.print_status("ERROR", "Steam installation not found. Please ensure Steam is installed.")
        return

    games_found = get_sim_racing_game_folders()

    if games_found:
        if args.revert:
            console_ui.print_header("Reverting Configurations")
            results = config_orchestrator.revert_configurations(games_found)
        else:
            console_ui.print_header("Configuration Check")
            results = config_orchestrator.check_and_configure_games(games_found)
        
        console_ui.print_summary_table(results)
        console_ui.print_details(results, verbose=args.verbose)
        
        console_ui.print_header("Process Finished")
    else:
        console_ui.print_status("INFO", "No supported sim racing games found.")

if __name__ == "__main__":
    main()
