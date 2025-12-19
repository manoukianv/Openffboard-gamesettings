"""
Sub-package for specific game configurators.

This package contains all modules responsible for the configuration logic
specific to each game or family of games. The architecture is designed to be
extensible: to support a new game, simply add a new configurator module here.

Design:
- `base_configurator.py`: Defines the abstract base class that all other
  configurators must inherit from.
- `factory.py`: Provides a factory to instantiate the correct configurator
  based on the game's AppID.
- `*_configurator.py`: Each file implements the logic for a specific game
  (e.g., `dirt_wrc_configurator.py`).
"""
# This empty file makes this directory a Python package.
