from offbgamessettings.game_configurators.factory import ConfiguratorFactory, CONFIGURATOR_MAP
from offbgamessettings.game_configurators.recommendation_configurator import RecommendationConfigurator


def test_get_configurator_unknown():
    assert ConfiguratorFactory.get_configurator("0000", "X", "/tmp") is None


def test_get_configurator_known_types():
    # Pick keys that are known to exist in CONFIGURATOR_MAP
    for app_id in CONFIGURATOR_MAP.keys():
        cfg = ConfiguratorFactory.get_configurator(app_id, "Game", "/tmp")
        assert cfg is not None


def test_recommendation_configurator_initialization():
    # Ensure recommendation configurator gets its recommendations
    app_id = "1134570"
    cfg = ConfiguratorFactory.get_configurator(app_id, "F1", "/tmp")
    assert isinstance(cfg, RecommendationConfigurator)
    assert isinstance(cfg.recommendations, list)