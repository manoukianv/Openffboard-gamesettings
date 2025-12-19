from offbgamessettings.game_configurators.recommendation_configurator import (
    RecommendationConfigurator,
)


def test_recommendation_logs_and_revert():
    recs = ["Disable assists", "Set rotation to 360"]
    cfg = RecommendationConfigurator("1134570", "F1", "/tmp", recs)
    res = cfg.check_and_configure()
    assert res["status"] == "INFO"
    assert any(r["message"] == "Disable assists" for r in res["logs"]) or len(
        res["logs"]
    ) == len(recs)

    rev = cfg.revert_configuration()
    assert rev["status"] == "NOT REQUIRED"
