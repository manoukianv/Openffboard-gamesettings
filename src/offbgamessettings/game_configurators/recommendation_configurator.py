# src/offbgamessettings/game_configurators/recommendation_configurator.py
from .base_configurator import BaseGameConfigurator

class RecommendationConfigurator(BaseGameConfigurator):
    def __init__(self, game_name, game_path, recommendations):
        super().__init__(game_name, game_path)
        self.recommendations = recommendations

    def check_and_configure(self):
        for rec in self.recommendations:
            self.logs.append({"status": "INFO", "message": rec})
        self.status = "INFO"
        return {"status": self.status, "logs": self.logs}

    def revert_configuration(self):
        # No files to revert for recommendations
        self.status = "NOT REQUIRED"
        return {"status": self.status, "logs": self.logs}
