"""
Console User Interface (UI).

This module centralizes all display logic for the command-line application.
It is responsible for formatting output, using colors to improve readability,
and interacting with the user (such as confirmation prompts).

Dependencies:
-   `colorama`: Used to provide colored output that is compatible with both
    Windows and Linux terminals. It is initialized once when the module is
    loaded.

Structure:
-   `STATUS_COLORS`: A central dictionary that maps status types (e.g., "OK",
    "ERROR") to `colorama` color codes, ensuring visual consistency
    throughout the application.
-   Display Functions: A series of functions (`print_header`, `print_status`,
    etc.) for specific display tasks, such as printing headers, status
    messages, or summary tables.
-   Interaction Functions: `ask_user` for asking the user questions.
"""
import colorama
from colorama import Fore, Style, init

# Initialize colorama to work on all platforms
# autoreset=True ensures that each print statement resets the color style
init(autoreset=True)

# Central dictionary for status colors.
# Ensures color consistency across the entire interface.
STATUS_COLORS = {
    "OK": Fore.GREEN,
    "MODIFIED": Fore.GREEN,
    "INFO": Fore.CYAN,
    "WARNING": Fore.YELLOW,
    "ERROR": Fore.RED,
    "NOT REQUIRED": Fore.BLACK,
    "RESTORED": Fore.RED,
    "NOT FOUND": Fore.YELLOW,
}


def print_header(title):
    """
    Prints a formatted section header to improve readability.

    Args:
        title (str): The text to display in the header.
    """
    print(f"\n{Style.BRIGHT}{Fore.CYAN}--- {title} ---{Style.RESET_ALL}")


def print_status(status, message):
    """
    Prints a status message with the appropriate color.

    The color is determined by the `STATUS_COLORS` dictionary.

    Args:
        status (str): The type of status (e.g., "OK", "ERROR").
        message (str): The message to display.
    """
    color = STATUS_COLORS.get(status.upper(), Fore.WHITE)
    print(f"[{color}{Style.BRIGHT}{status.upper()}{Style.RESET_ALL}] {message}")


def print_recommendation(message):
    """
    Prints a recommendation message with a distinctive style.

    Args:
        message (str): The recommendation to display.
    """
    print(f"  {Fore.BLUE}Recommendation:{Style.RESET_ALL} {message}")


def ask_user(prompt):
    """
    Asks the user a question and returns their response.

    Args:
        prompt (str): The message to display to the user.

    Returns:
        str: The user's response.
    """
    return input(f"{Fore.YELLOW}{prompt} {Style.RESET_ALL}")


def print_summary_table(results):
    """
    Prints a summary table of the results of all game checks.

    Args:
        results (dict): The results dictionary returned by the orchestrator.
    """
    print_header("Summary")

    max_len = max(len(game) for game in results.keys()) if results else 0

    print(f"{'Game'.ljust(max_len)} | Status")
    print(f"{'-' * max_len}-|--------")

    for game, data in results.items():
        status = data["status"]
        color = STATUS_COLORS.get(status.upper(), Fore.WHITE)
        print(f"{game.ljust(max_len)} | {color}{Style.BRIGHT}{status}{Style.RESET_ALL}")


def print_details(results, verbose=False):
    """
    Prints the detailed logs for each game.

    By default, only "WARNING" and "ERROR" messages are displayed.
    If `verbose` is True, "INFO", "MODIFIED", and "OK" messages are also
    included, providing a complete view of the process.

    Args:
        results (dict): The results dictionary returned by the orchestrator.
        verbose (bool): If True, displays all log levels.
    """
    details_to_show = {}
    for game, data in results.items():
        logs_to_show = []
        for log in data["logs"]:
            status = log["status"].upper()
            # Always show warnings and errors
            if status in ["WARNING", "ERROR"]:
                logs_to_show.append(log)
            # Only show other statuses in verbose mode
            elif verbose and status in ["INFO", "MODIFIED", "OK"]:
                logs_to_show.append(log)

        if logs_to_show:
            details_to_show[game] = {"logs": logs_to_show}

    if not details_to_show:
        return

    print_header("Details")

    for game, data in details_to_show.items():
        print(f"\n{Style.BRIGHT}{game}:{Style.RESET_ALL}")
        for log in data["logs"]:
            print(f"  ", end="")
            print_status(log["status"], log["message"])
