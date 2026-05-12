def validate_action(action, observation):

    action_type = action.get("action")


    # =========================
    # click_text validation
    # =========================
    if action_type == "click_text":

        target = action.get("text", "").lower()

        elements = observation.get("elements", [])

        for el in elements:

            text = el.get("text", "").lower()

            if target in text:

                return True

        print(f"Validation failed: text '{target}' not found")

        return False


    # =========================
    # type validation
    # =========================
    elif action_type == "type":

        text = action.get("text")

        if not text:

            print("Validation failed: empty type text")

            return False

        return True


    # =========================
    # click validation
    # =========================
    elif action_type == "click":

        x = action.get("x")
        y = action.get("y")

        if x is None or y is None:

            print("Validation failed: invalid coordinates")

            return False

        return True


    # =========================
    # wait validation
    # =========================
    elif action_type == "wait":

        seconds = action.get("seconds", 0)

        if seconds < 0 or seconds > 30:

            print("Validation failed: invalid wait")

            return False

        return True


    # =========================
    # press validation
    # =========================
    elif action_type == "press":

        key = action.get("key")

        if not key:

            print("Validation failed: missing key")

            return False

        return True


    # =========================
    # default safe actions
    # =========================
    return True