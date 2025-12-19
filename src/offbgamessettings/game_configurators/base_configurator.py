# src/offbgamessettings/game_configurators/base_configurator.py
"""
Defines the Abstract Base Class (ABC) for all game configurators.

This module provides the `BaseGameConfigurator` class, which serves as a contract
for all concrete game configurator implementations. It ensures that every
configurator has a consistent interface for checking, applying, and reverting
configurations.

The use of an ABC allows the factory to treat all configurators uniformly,
simplifying the overall design and making it easy to extend with new game
configurations.
"""
from abc import ABC, abstractmethod

class BaseGameConfigurator(ABC):
    """
    Abstract Base Class for game configurators.

    Each subclass must implement the `check_and_configure` and
    `revert_configuration` methods.
    
    Attributes:
        app_id (str): The Steam AppID of the game.
        game_name (str): The name of the game.
        game_path (str): The installation path of the game.
        logs (list): A list to store log messages during operations.
        status (str): The final status of the configuration check.
    """
    def __init__(self, app_id, game_name, game_path):
        """
        Initializes the configurator with game-specific data.

        Args:
            app_id (str): The Steam AppID of the game.
            game_name (str): The name of the game.
            game_path (str): The installation path of the game.
        """
        self.app_id = app_id
        self.game_name = game_name
        self.game_path = game_path
        self.logs = []
        self.status = "OK"

    @abstractmethod
    def check_and_configure(self):
        """
        Checks the game's configuration and applies necessary changes.

        This method should contain the core logic for verifying game files
        and patching them if they are not compliant with OpenFFBoard requirements.

        Returns:
            dict: A dictionary containing the final 'status' and a list of 'logs'.
        """
        pass

    @abstractmethod
    def revert_configuration(self):
        """
        Restores the game's original configuration from a backup.

        This method should find any backup files created by the configurator
        and use them to restore the original game files.

        Returns:
            dict: A dictionary containing the final 'status' and a list of 'logs'.
        """
        pass
