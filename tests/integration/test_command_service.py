import pytest
from misc import exceptions
from service import command_service as sc
from service import resource_service as sr


def test_empty_command():
    with pytest.raises(exceptions.InvalidCommand):
        sc.parse_command("")


def test_unknown_command():
    with pytest.raises(exceptions.InvalidCommand):
        sc.parse_command("foo")


def test_insufficient_args():
    with pytest.raises(exceptions.InvalidCommand):
        sc.parse_command("create")


def test_list():
    method, args = sc.parse_command("list")
    assert method == sr.list_resources
    assert args == {}


def test_create():
    method, args = sc.parse_command("create resource-name")
    assert method == sr.create_resource
    assert args == {"resource_name": "resource-name"}


def test_lock_with_duration():
    method, args = sc.parse_command("lock resource-name 12 d")
    assert method == sr.acquire_resource
    assert args == {"resource_name": "resource-name", "duration": 12 * 24 * 60}

    method, args = sc.parse_command("lock resource-name 12 months")
    assert args == {"resource_name": "resource-name", "duration": 12 * 24 * 60 * 30}


def test_lock_with_message():
    method, args = sc.parse_command("lock resource-name 12 w some reason")
    assert args == {"resource_name": "resource-name", "duration": 12 * 24 * 60 * 7, "message": "some reason"}
