# src/offbgamessettings/output.py
import colorama
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# --- Single Source of Truth for Status Colors ---
STATUS_COLORS = {
    "OK": Fore.GREEN,
    "MODIFIED": Fore.GREEN,
    "INFO": Fore.CYAN,
    "WARNING": Fore.YELLOW,
    "ERROR": Fore.RED,
    "NOT REQUIRED": Fore.BLACK,
    "RESTORED": Fore.RED,
    "NOT FOUND": Fore.YELLOW
}

def print_header(title):
    """Prints a main header."""
    print(f"\n{Style.BRIGHT}{Fore.CYAN}--- {title} ---{Style.RESET_ALL}")

def print_status(status, message):
    """Prints a status message with appropriate color."""
    color = STATUS_COLORS.get(status.upper(), Fore.WHITE)
    print(f"[{color}{Style.BRIGHT}{status.upper()}{Style.RESET_ALL}] {message}")

def print_recommendation(message):
    """Prints a recommendation message."""
    print(f"  {Fore.BLUE}Recommendation:{Style.RESET_ALL} {message}")

def ask_user(prompt):
    """Asks the user for input with consistent styling."""
    return input(f"{Fore.YELLOW}{prompt} {Style.RESET_ALL}")

def print_summary_table(results):
    """Prints a summary table of all game checks."""
    print_header("Summary")
    
    max_len = max(len(game) for game in results.keys()) if results else 0
    
    print(f"{'Game'.ljust(max_len)} | Status")
    print(f"{'-' * max_len}-|--------")
    
    for game, data in results.items():
        status = data['status']
        color = STATUS_COLORS.get(status.upper(), Fore.WHITE)
        print(f"{game.ljust(max_len)} | {color}{Style.BRIGHT}{status}{Style.RESET_ALL}")

def print_details(results, verbose=False):
    """
    Prints the detailed logs.
    Shows WARNING and ERROR logs by default.
    Shows INFO and MODIFIED logs only if verbose is True.
    """
    details_to_show = {}
    for game, data in results.items():
        logs_to_show = []
        for log in data['logs']:
            status = log['status'].upper()
            if status in ["WARNING", "ERROR"]:
                logs_to_show.append(log)
            elif verbose and status in ["INFO", "MODIFIED", "OK"]:
                logs_to_show.append(log)
        
        if logs_to_show:
            details_to_show[game] = {"logs": logs_to_show}

    if not details_to_show:
        return

    print_header("Details")
    
    for game, data in details_to_show.items():
        print(f"\n{Style.BRIGHT}{game}:{Style.RESET_ALL}")
        for log in data['logs']:
            print(f"  ", end="") 
            print_status(log['status'], log['message'])
