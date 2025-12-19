import os
import shutil

from offbgamessettings.utils import backup_file


def test_backup_file_nonexistent(tmp_path):
    path = tmp_path / "does_not_exist.txt"
    assert backup_file(str(path)) is False


def test_backup_file_success(tmp_path):
    f = tmp_path / "myfile.txt"
    f.write_text("hello")

    assert backup_file(str(f)) is True

    bak = tmp_path / "myfile.txt.bak_offb_settings"
    assert bak.exists()
    assert bak.read_text() == "hello"

    # cleanup
    bak.unlink()
    f.unlink()
