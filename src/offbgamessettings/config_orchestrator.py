"""
Game Configuration Orchestrator.

This module acts as the "conductor" of the configuration process.
Its role is to take the list of games detected by `game_discovery` and
invoke the appropriate configurator for each game.

Architecture:
-   It uses `ConfiguratorFactory` to get the specific configurator instance
    for each game, based on the Steam AppID.
-   It decouples the main application logic from the configuration details
    of each game. To add support for a new game, only the factory and a new
    configurator need to be created, without modifying this orchestrator.
-   It handles the two main workflows: checking/configuring and reverting
    changes.
"""
from .game_configurators.factory import ConfiguratorFactory


def check_and_configure_games(games_found):
    """
    Checks and configures all detected games.

    For each game in the list, this function asks the factory for the
    appropriate configurator and executes its `check_and_configure` method.

    Args:
        games_found (dict): The dictionary of games returned by
                            `game_discovery.get_sim_racing_game_folders()`.

    Returns:
        dict: A results dictionary where the keys are the game names and the
              values are the results of the configuration operation (status
              and logs).
    """
    results = {}
    for app_id, game_data in games_found.items():
        game_name = game_data["name"]
        game_path = game_data["path"]
        # Use the factory to get the specific configurator for this game
        configurator = ConfiguratorFactory.get_configurator(
            app_id, game_name, game_path
        )

        if configurator:
            # The game has a configurator, so we run it
            results[game_name] = configurator.check_and_configure()
        else:
            # The game was detected, but no action is required
            results[game_name] = {"status": "NOT REQUIRED", "logs": []}
    return results


def revert_configurations(games_found):
    """
    Reverts the configurations for all detected games.

    For each game in the list, this function asks the factory for the
    appropriate configurator and executes its `revert_configuration` method.

    Args:
        games_found (dict): The dictionary of games returned by
                            `game_discovery.get_sim_racing_game_folders()`.

    Returns:
        dict: A results dictionary where the keys are the game names and the
              values are the results of the revert operation.
    """
    results = {}
    for app_id, game_data in games_found.items():
        game_name = game_data["name"]
        game_path = game_data["path"]
        # Use the factory to get the specific configurator for this game
        configurator = ConfiguratorFactory.get_configurator(
            app_id, game_name, game_path
        )

        if configurator:
            # The game has a configurator, so we run the revert
            results[game_name] = configurator.revert_configuration()
        else:
            # The game was detected, but no action is required
            results[game_name] = {"status": "NOT REQUIRED", "logs": []}
    return results
