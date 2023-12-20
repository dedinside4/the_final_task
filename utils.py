def change_state(new_state=None):
    global current_state, current_level

    if current_state == "main_menu":
        current_state = "perehod.py"
    elif current_state == "model.py":
        if new_state is None:
            current_level += 1
            new_state = f"level_{current_level}.py"  # Adjust this according to your level naming convention
        current_state = new_state
