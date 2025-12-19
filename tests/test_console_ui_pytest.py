import re
import builtins
from offbgamessettings import console_ui


def strip_ansi(s):
    return re.sub(r"\x1b\[[0-9;]*m", "", s)


def test_prints_and_ask_user(capsys, monkeypatch):
    console_ui.print_header("Header Test")
    console_ui.print_status("OK", "Everything fine")
    console_ui.print_recommendation("Do X")

    console_ui.print_summary_table({"GameA": {"status": "OK"}, "LongGame": {"status": "WARNING"}})

    console_ui.print_details({"GameA": {"logs": [{"status":"ERROR","message":"Bad"}, {"status":"INFO","message":"Info"}]},
                               "GameB": {"logs": [{"status":"INFO","message":"Other"}]}}
                              , verbose=False)

    captured = capsys.readouterr().out
    clean = strip_ansi(captured)

    assert "--- Header Test ---" in clean
    assert "[OK] Everything fine" in clean
    assert "Recommendation:" in clean
    assert "GameA" in clean
    assert "Status" in clean

    # ask_user
    monkeypatch.setattr('builtins.input', lambda prompt: 'y')
    assert console_ui.ask_user("Proceed?") == 'y'