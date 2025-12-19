# src/offbgamessettings/config_manager.py
from .game_configurators.factory import ConfiguratorFactory

def check_and_configure_games(games_found):
    """Checks and configures all detected games using the factory."""
    results = {}
    for app_id, game_data in games_found.items():
        game_name = game_data['name']
        game_path = game_data['path']
        configurator = ConfiguratorFactory.get_configurator(app_id, game_name, game_path)
        if configurator:
            results[game_name] = configurator.check_and_configure()
        else:
            results[game_name] = {"status": "NOT REQUIRED", "logs": []}
    return results

def revert_configurations(games_found):
    """Reverts configurations for all detected games using the factory."""
    results = {}
    for app_id, game_data in games_found.items():
        game_name = game_data['name']
        game_path = game_data['path']
        configurator = ConfiguratorFactory.get_configurator(app_id, game_name, game_path)
        if configurator:
            results[game_name] = configurator.revert_configuration()
        else:
            results[game_name] = {"status": "NOT REQUIRED", "logs": []}
    return results

