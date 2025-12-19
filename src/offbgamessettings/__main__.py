"""
Main entry point for the command-line application.

This module is responsible for parsing command-line arguments and
orchestrating the main workflow of the application.

Workflow:
1.  **Argument Parsing**: Uses `argparse` to handle options
    like `--verbose` and `--revert`.
2.  **Header Display**: Displays a welcome banner.
3.  **Game Discovery**: Calls functions from `game_discovery` to
    find the Steam installation and relevant games.
4.  **Action Execution**:
    - If `--revert` is used, it asks `config_orchestrator` to revert
      the configurations.
    - Otherwise, it asks to check and apply the configurations.
5.  **Result Display**: Uses `console_ui` to display a summary
    table and detailed logs (depending on the `--verbose` option).
"""
import argparse
from offbgamessettings.game_discovery import get_sim_racing_game_folders, find_steam_path
from offbgamessettings import config_orchestrator
from offbgamessettings import console_ui

def main():
    """
    Entry point for the command-line interface.
    Finds and configures sim racing games for OpenFFBoard.
    """
    # Set up the argument parser for the command line
    parser = argparse.ArgumentParser(description="Game configuration utility for OpenFFBoard")
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Displays detailed information for all checks, including successful modifications."
    )
    parser.add_argument(
        "--revert",
        action="store_true",
        help="Restores the original game configuration files from backups."
    )
    args = parser.parse_args()

    console_ui.print_header("Game Configuration Utility for OpenFFBoard")

    # Step 1: Check if Steam is installed
    if not find_steam_path():
        console_ui.print_status("ERROR", "Steam installation not found. Please ensure Steam is installed.")
        return

    # Step 2: Discover installed simulation games
    games_found = get_sim_racing_game_folders()

    if games_found:
        # Step 3: Execute the requested action (configure or revert)
        if args.revert:
            console_ui.print_header("Reverting configurations")
            results = config_orchestrator.revert_configurations(games_found)
        else:
            console_ui.print_header("Checking configuration")
            results = config_orchestrator.check_and_configure_games(games_found)
        
        # Step 4: Display the results to the user
        console_ui.print_summary_table(results)
        console_ui.print_details(results, verbose=args.verbose)
        
        console_ui.print_header("Process finished")
    else:
        # No supported games were found
        console_ui.print_status("INFO", "No supported sim racing games were found.")

# Ensures that the main() function is called when the script is executed directly
if __name__ == "__main__":
    main()
