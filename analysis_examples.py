def process_data(data):
    total = 0
    for i in range(len(data)):
        if data[i] < 0:
            continue
        for j in range(data[i]):
            if j % 2 == 0:
                total += j
    return total


def check_access(role, is_active, is_admin):
    if (role == "user" and is_active) or is_admin:
        return True
    return False


def process_matrix(matrix):
    count = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] > 0:
                for k in range(matrix[i][j]):
                    count += k % 3
    return count


def validate_input(user, password):
    if not user:
        return "Missing user"
    if len(password) < 8:
        return "Weak password"
    if any(char.isdigit() for char in password) and any(
        char.isupper() for char in password
    ):
        return "Valid"
    return "Invalid"


def update_task_status(task, new_status, user_role):
    valid_transitions = {
        "open": ["in_progress", "closed"],
        "in_progress": ["closed", "on_hold"],
        "on_hold": ["in_progress"],
        "closed": [],
    }

    if task["status"] == new_status:
        return "No change"
    if new_status not in valid_transitions.get(task["status"], []):
        return "Invalid transition"
    if user_role not in ["admin", "manager"] and new_status == "closed":
        return "Permission denied"

    task["status"] = new_status
    return "Updated"
