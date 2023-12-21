def change_state(current_state, current_level, new_state=None):
    if current_state == "main.py":
        current_state = "perehod.py"
    elif current_state == "model.py":
        if new_state is None:
            current_level += 1
            new_state = f"level_{current_level}.py"
        current_state = new_state

    return current_state, current_level
