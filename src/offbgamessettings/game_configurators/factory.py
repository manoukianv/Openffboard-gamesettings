"""
Implements the Factory design pattern for creating game configurator instances.

This module is the central point for dispatching configuration tasks. The
`ConfiguratorFactory` class uses a mapping (CONFIGURATOR_MAP) to associate a
Steam AppID with the appropriate concrete configurator class.

This design decouples the main application logic from the specific implementation
of each game configurator, making the system easy to extend: to support a new
game, one only needs to create a new configurator class and add it to the map.
"""# src/offbgamessettings/game_configurators/factory.py
from .dirt_wrc_configurator import DirtWrcConfigurator
from .rfactor2_configurator import Rfactor2Configurator
from .recommendation_configurator import RecommendationConfigurator

# --- Mapping from AppID to Configurator Class ---
CONFIGURATOR_MAP = {
    "1849250": DirtWrcConfigurator, # EA SPORTS WRC
    "690790": DirtWrcConfigurator,  # DiRT Rally 2.0
    "365960": Rfactor2Configurator, # rFactor 2
    "1134570": RecommendationConfigurator, # F1 2020
    "1692250": RecommendationConfigurator, # F1 22
}

# --- Recommendations for specific games ---
RECOMMENDATIONS = {
    "1134570": ["Disable all steering assists.", "Set steering range to 360 degrees."],
    "1692250": ["Disable all steering assists.", "Set steering range to 360 degrees."],
}

class ConfiguratorFactory:
    @staticmethod
    def get_configurator(app_id, game_name, game_path):
        config_class = CONFIGURATOR_MAP.get(app_id)
        
        if not config_class:
            return None # No specific configurator for this game
        
        if config_class == RecommendationConfigurator:
            recs = RECOMMENDATIONS.get(app_id, [])
            return RecommendationConfigurator(app_id, game_name, game_path, recs)
        else:
            return config_class(app_id, game_name, game_path)
