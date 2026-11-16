from itertools import product

import pytest

from analysis_examples import (
    check_access,
    process_data,
    process_matrix,
    update_task_status,
    validate_input,
)


@pytest.mark.parametrize(
    "data,expected", [([], 0), ([-1], 0), ([0], 0), ([1], 0), ([2], 0), ([-1, 0, 3], 2)]
)
def test_process_data(data, expected):
    assert process_data(data) == expected


@pytest.mark.parametrize("is_user,active,admin", tuple(product((False, True), repeat=3)))
def test_check_access(is_user, active, admin):
    expected = admin or (is_user and active)
    assert check_access("user" if is_user else "guest", active, admin) is expected


@pytest.mark.parametrize(
    "matrix,expected", [([], 0), ([[]], 0), ([[-1, 0]], 0), ([[1, 2], [], [3]], 4)]
)
def test_process_matrix(matrix, expected):
    assert process_matrix(matrix) == expected


@pytest.mark.parametrize(
    "user,password,expected",
    [
        ("", "abcdefgA1", "Missing user"),
        ("alice", "A1", "Weak password"),
        ("alice", "abcdefgh", "Invalid"),
        ("alice", "Abcdefgh", "Invalid"),
        ("alice", "abcdefg1", "Invalid"),
        ("alice", "Abcdefg1", "Valid"),
    ],
)
def test_validate_input(user, password, expected):
    assert validate_input(user, password) == expected


@pytest.mark.parametrize(
    "old,new,regular",
    [
        ("open", "open", "No change"),
        ("open", "in_progress", "Updated"),
        ("open", "on_hold", "Invalid transition"),
        ("open", "closed", "Permission denied"),
        ("in_progress", "open", "Invalid transition"),
        ("in_progress", "in_progress", "No change"),
        ("in_progress", "on_hold", "Updated"),
        ("in_progress", "closed", "Permission denied"),
        ("on_hold", "open", "Invalid transition"),
        ("on_hold", "in_progress", "Updated"),
        ("on_hold", "on_hold", "No change"),
        ("on_hold", "closed", "Invalid transition"),
        ("closed", "open", "Invalid transition"),
        ("closed", "in_progress", "Invalid transition"),
        ("closed", "on_hold", "Invalid transition"),
        ("closed", "closed", "No change"),
        ("open", "unknown", "Invalid transition"),
        ("unknown", "closed", "Invalid transition"),
    ],
)
@pytest.mark.parametrize("role", ("member", "manager", "admin"))
def test_update_task_status(old, new, regular, role):
    expected = "Updated" if regular == "Permission denied" and role != "member" else regular
    task = {"status": old}
    assert update_task_status(task, new, role) == expected
    assert task["status"] == (new if expected == "Updated" else old)


