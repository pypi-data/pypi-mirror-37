#!/usr/bin/env python3

import argparse
import datetime
import json
import logging
import logging.handlers
import sys
import time

import digitalocean

import mock
import pytest
from dobackup import dobackup

# token_str = "e3394c55ae7dda73e62cb10d3016bdbaabcc977e0827049e1de824fe2d7345e4"
# existing_droplet_name = "pbox"
# non_existing_droplet_name = "test-drop"
# existing_droplet_id = "93202316"
# non_existing_droplet_id = "123456"
# existing_snap_id = "00000000"
# non_existing_snap_id = "0000000"
__version__ = "1.4.1.dev1"
token_str = "03124a75daded6ff4a26ba33e25a600df878815a4cdabe5b724f47516e403f3d"
existing_droplet_name = "openproject"
non_existing_droplet_name = "test-drop"
existing_droplet_id = "89258859"
non_existing_droplet_id = "123456"
existing_snap_id = "38478530"
non_existing_snap_id = "0000000"


def test_set_tokens(monkeypatch, do_token):
    monkeypatch.setattr('builtins.input', lambda x: token_str)
    dobackup.set_tokens()
    assert do_token == token_str


@pytest.fixture
def do_token():
    do_token = dobackup.get_token(token_id=0)
    return do_token


@pytest.fixture
def manager(do_token):
    manager = dobackup.set_manager(do_token)
    return manager


# def test_version():
#     assert dobackup.__version__ == __version__


def test_get_token(do_token):
    assert do_token == token_str


def test_set_manager(manager):
    # manager = dobackup.set_manager(do_token)
    assert isinstance(manager, digitalocean.Manager) is True


def test_find_droplet_name(manager):
    drop = dobackup.find_droplet(existing_droplet_name, manager)
    assert isinstance(drop, digitalocean.Droplet) is True


def test_find_droplet_id(manager):
    drop = dobackup.find_droplet(existing_droplet_id, manager)
    assert isinstance(drop, digitalocean.Droplet) is True


def test_find_droplet_wrong_name(manager):
    drop = dobackup.find_droplet(non_existing_droplet_name, manager)
    assert isinstance(drop, digitalocean.Droplet) is False


def test_find_droplet_wrong_id(manager):
    drop = dobackup.find_droplet(non_existing_droplet_id, manager)
    assert isinstance(drop, digitalocean.Droplet) is False


def test_find_snapshot(manager, do_token):
    snap_obj = dobackup.find_snapshot(existing_snap_id, manager, do_token, droplet_id=000000)
    assert isinstance(snap_obj, digitalocean.Snapshot) is True


def test_find_snapshot_wrong_id(manager, do_token):
    with mock.patch('dobackup.dobackup.sys.exit') as exit_mock:
        snap_obj = dobackup.find_snapshot(
            non_existing_snap_id, manager, do_token, droplet_id=000000)
        assert snap_obj is None

# To handle sys.exit in code
# def test_tag_droplet_wrong_id(manager, do_token):
#     with pytest.raises(SystemExit) as pytest_wrapped_e:
#         with mock.patch('sys.argv', ['dobackup', '--tag-server', non_existing_droplet_id]):
#             assert pytest_wrapped_e.type == SystemExit
#             assert pytest_wrapped_e.value.code == 1


def test_tag_droplet_wrong_id():
    with mock.patch('sys.argv', ['dobackup', '--tag-droplet', non_existing_droplet_id]):
        assert dobackup.main() == 1


def test_untag_droplet_wrong_id():
    with mock.patch('sys.argv', ['dobackup', '--untag-droplet', non_existing_droplet_id]):
        assert dobackup.main() == 1


def test_delete_snap_wrong_id():
    with mock.patch('sys.argv', ['dobackup', '--delete-snap', non_existing_droplet_id]):
        assert dobackup.main() == 1


def test_backup_drop_wrong_id():
    with mock.patch('sys.argv', ['dobackup', '--backup', non_existing_droplet_id]):
        assert dobackup.main() == 1


def test_powerup_wrong_id():
    with mock.patch('sys.argv', ['dobackup', '--powerup', non_existing_droplet_id]):
        assert dobackup.main() == 1


def test_main():

    with mock.patch('sys.argv', ['dobackup', '--list-droplets']):
        assert dobackup.main() == 0
    with mock.patch('sys.argv', ['dobackup', '--list-snaps']):
        assert dobackup.main() == 0
    with mock.patch('sys.argv', ['dobackup', '--list-tags']):
        assert dobackup.main() == 0
    with mock.patch('sys.argv', ['dobackup', '--list-backups']):
        assert dobackup.main() == 0
    with mock.patch('sys.argv', ['dobackup', '--list-tagged']):
        assert dobackup.main() == 0
    with mock.patch('sys.argv', ['dobackup', '--list-older-than', '7']):
        assert dobackup.main() == 0
    with mock.patch('sys.argv', ['dobackup', '--tag-droplet', non_existing_droplet_id]):
        assert dobackup.main() == 1

        # dobackup.run(token_id=None, init, list_drops, list_backups, list_snaps, list_tagged, list_tags,
        #              list_older_than, tag_server, untag_server, tag_name, delete_older_than,
        #              delete_snap, backup, backup_all, shutdown, powerup, restore_drop,
        #              restore_to)
