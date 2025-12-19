"""
Configurator for displaying parameter recommendations.

This configurator is not intended to modify game files. Its sole
purpose is to display advice or instructions to the user for games
that cannot be configured automatically.

For example, it can be used to remind the user to disable
certain driving aids in the game menus or to set the steering wheel
rotation to a specific value.

How it works:
-   It receives a list of strings (the recommendations) upon
    initialization.
-   The `check_and_configure` method simply adds each recommendation
    to the logs with an "INFO" status.
-   The `revert_configuration` method does nothing, as no changes
    were made.
"""
from .base_configurator import BaseGameConfigurator


class RecommendationConfigurator(BaseGameConfigurator):
    """
    A configurator that displays recommendations instead of modifying files.
    """

    def __init__(self, app_id, game_name, game_path, recommendations):
        """
        Initializes the configurator with game-specific recommendations.

        Args:
            app_id (str): The Steam AppID of the game.
            game_name (str): The name of the game.
            game_path (str): The installation path of the game.
            recommendations (list): A list of strings containing
                                  the recommendations to be displayed.
        """
        super().__init__(app_id, game_name, game_path)
        self.recommendations = recommendations
        # The default status is INFO because it only gives advice
        self.status = "INFO"

    def check_and_configure(self):
        """
        Adds the predefined recommendations to the logs for display.
        """
        for rec in self.recommendations:
            self.logs.append({"status": "INFO", "message": rec})
        return {"status": self.status, "logs": self.logs}

    def revert_configuration(self):
        """
        Does nothing because no changes are made by this configurator.

        Returns:
            dict: A "NOT REQUIRED" status to indicate that no action
                  was necessary.
        """
        self.status = "NOT REQUIRED"
        self.logs.append(
            {"status": "INFO", "message": "No changes to revert for recommendations."}
        )
        return {"status": self.status, "logs": self.logs}
