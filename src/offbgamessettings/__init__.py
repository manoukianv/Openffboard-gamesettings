"""
Main package for the OpenFFBoard game configuration utility.

This package contains all the logic for discovering, configuring, and
reverting settings for sim racing games.

The organization is as follows:
- `game_discovery.py`: Detects installed games.
- `config_orchestrator.py`: Orchestrates the configuration process.
- `console_ui.py`: Manages console display.
- `utils.py`: Provides utility functions (e.g., backup).
- `game_configurators/`: A sub-package containing game-specific logic.
"""

__version__ = "0.0.1"

from .game_discovery import get_sim_racing_game_folders

# __all__ defines the public API of the package.
# Only get_sim_racing_game_folders is exposed during a `*` import.
__all__ = ["get_sim_racing_game_folders"]
