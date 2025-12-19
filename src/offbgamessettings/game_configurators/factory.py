"""
Implements the Factory design pattern to create instances of game configurators.

This module is the central point for dispatching configuration tasks. The
`ConfiguratorFactory` class uses a mapping table (`CONFIGURATOR_MAP`)
to associate a Steam AppID with the appropriate concrete configurator class.

This design decouples the main application logic from the specific
implementation of each game configurator, making the system easy to extend:
to support a new game, simply create a new configurator class and
add it to the mapping table.
"""
from .dirt_wrc_configurator import DirtWrcConfigurator
from .rfactor2_configurator import Rfactor2Configurator
from .recommendation_configurator import RecommendationConfigurator

# --- Mapping table from AppID to configurator class ---
# This is the core of the factory. To add support for a new game,
# simply add a new entry here.
CONFIGURATOR_MAP = {
    "1849250": DirtWrcConfigurator,        # EA SPORTS WRC
    "690790": DirtWrcConfigurator,         # DiRT Rally 2.0
    "365960": Rfactor2Configurator,        # rFactor 2
    "1134570": RecommendationConfigurator, # F1 2020 (recommendation example)
    "1692250": RecommendationConfigurator, # F1 22 (recommendation example)
}

# --- Specific recommendations for games that need them ---
# Used by the RecommendationConfigurator.
RECOMMENDATIONS = {
    "1134570": ["Disable all steering assists.", "Set the steering range to 360 degrees."],
    "1692250": ["Disable all steering assists.", "Set the steering range to 360 degrees."],
}

class ConfiguratorFactory:
    """
    A static factory for creating instances of game configurators.
    """
    @staticmethod
    def get_configurator(app_id, game_name, game_path):
        """
        Returns an instance of the appropriate configurator for a given game.

        Args:
            app_id (str): The Steam AppID of the game.
            game_name (str): The name of the game.
            game_path (str): The installation path of the game.

        Returns:
            BaseGameConfigurator or None: An instance of a game configurator if
                                        a mapping exists, otherwise None.
        """
        config_class = CONFIGURATOR_MAP.get(app_id)
        
        if not config_class:
            # No configurator is defined for this game
            return None
        
        # Special case for the recommendation configurator, which needs
        # additional arguments during its initialization.
        if config_class == RecommendationConfigurator:
            recs = RECOMMENDATIONS.get(app_id, [])
            return RecommendationConfigurator(app_id, game_name, game_path, recs)
        else:
            # Standard instantiation for all other configurators
            return config_class(app_id, game_name, game_path)
