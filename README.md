# offbgamessettings

A tool to detect and configure Steam sim racing games for OpenFFBoard.

## Features

- **Game Detection**: Automatically finds sim racing games installed via Steam (Windows & Linux).
- **Auto-Configuration**: Checks game files and applies necessary modifications for OpenFFBoard compatibility.
- **Safe Modifications**: Automatically creates backups of any files it modifies.
- **Interactive Prompts**: Asks for confirmation before making critical changes.

## How it Works

The tool scans for known sim racing games and compares their configuration files against the recommendations from the [official OpenFFBoard Games setup guide](https://github.com/Ultrawipf/OpenFFBoard/wiki/Games-setup).

It can currently perform automatic modifications for:
- **DiRT Series & EA SPORTS WRC**: Adds the OpenFFBoard device to `device_defines.xml` and creates the necessary `openffboard.xml` action map.
- **rFactor 2**: Checks for and corrects reversed Force Feedback settings in `Controller.JSON`.

For other games, it will display the recommended in-game settings.

**Disclaimer**: This tool will offer to modify game files. While backups are created automatically, use it at your own risk.

## Installation

Install the package in editable mode for development:
```bash
pip install -e .
```

This will also install a command-line tool `offbgamessettings`.

## Usage

### Checking and Applying Configurations

Run the tool from your terminal to scan for games and apply recommended settings:
```bash
offbgamessettings
```

To see detailed logs for all operations (including successful ones), use the `--verbose` flag:
```bash
offbgamessettings --verbose
```

### Reverting Configurations

The tool automatically creates a backup (`.bak_offb_settings`) of any file it modifies. To restore these original files, use the `--revert` flag:
```bash
offbgamessettings --revert
```

```python
from offbgamessettings import get_sim_racing_game_folders

game_folders = get_sim_racing_game_folders()

if game_folders:
    print("Found sim racing games:")
    for game, path in game_folders.items():
        print(f"- {game}: {path}")
else:
    print("No sim racing games found.")
```

## Development

To set up the development environment:

```bash
pip install -r requirements-dev.txt
pre-commit install
```

## Tests

To run the tests:

```bash
pytest
```

## Building the Executable

You can create a standalone executable using PyInstaller.

1.  **Install development dependencies**:
    ```bash
    pip install -r requirements-dev.txt
    ```

2.  **Run PyInstaller**:
    The command will create a single executable file in the `dist` folder.
    ```bash
    pyinstaller --onefile --name offbgamessettings --paths src src/offbgamessettings/__main__.py
    ```

## License

MIT
