"""
Action validation: verify actions are safe before execution.
Prevents invalid actions, missing coordinates, bad parameters.
"""

from logger import logger


def validate_action(action, observation):
    """
    Validate action before execution.
    
    Args:
        action: Action dict with 'action' key
        observation: Current screen observation
        
    Returns:
        True if valid, False otherwise
    """
    
    action_type = action.get("action")
    
    if not action_type:
        logger.warning("Validation: no action type specified")
        return False
    
    logger.debug(f"Validating action: {action_type}")
    
    # =========================
    # click_text validation
    # =========================
    if action_type == "click_text":

        target = action.get("text", "").lower()

        if not target:
            logger.warning("Validation failed: empty click_text target")
            return False

        elements = observation.get("elements", [])

        for el in elements:

            text = el.get("text", "").lower()

            if target in text:
                logger.info(f"Validation: click_text '{target}' found on screen")
                return True

        logger.warning(f"Validation failed: text '{target}' not found in elements")
        return False


    # =========================
    # type validation
    # =========================
    elif action_type == "type":

        text = action.get("text")

        if not text:
            logger.warning("Validation failed: empty type text")
            return False

        if len(text) > 1000:
            logger.warning(f"Validation warning: type text is very long ({len(text)} chars)")

        logger.info(f"Validation: type action valid ({len(text)} chars)")
        return True


    # =========================
    # click validation
    # =========================
    elif action_type == "click":

        x = action.get("x")
        y = action.get("y")

        if x is None or y is None:
            logger.warning(f"Validation failed: invalid click coordinates ({x}, {y})")
            return False

        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            logger.warning(f"Validation failed: click coordinates not numeric ({x}, {y})")
            return False

        logger.info(f"Validation: click action valid at ({x}, {y})")
        return True


    # =========================
    # wait validation
    # =========================
    elif action_type == "wait":

        seconds = action.get("seconds", 0)

        if not isinstance(seconds, (int, float)):
            logger.warning(f"Validation failed: wait time not numeric ({seconds})")
            return False

        if seconds < 0 or seconds > 60:
            logger.warning(f"Validation failed: wait time out of range ({seconds}s)")
            return False

        logger.info(f"Validation: wait action valid ({seconds}s)")
        return True


    # =========================
    # press validation
    # =========================
    elif action_type == "press":

        key = action.get("key")

        if not key:
            logger.warning("Validation failed: missing key for press action")
            return False

        valid_keys = [
            "enter", "return", "tab", "esc", "escape",
            "backspace", "delete", "home", "end",
            "pageup", "pagedown", "up", "down", "left", "right"
        ]

        if isinstance(key, str):
            if key.lower() not in valid_keys:
                logger.warning(f"Validation warning: unusual key '{key}'")

        logger.info(f"Validation: press action valid (key={key})")
        return True


    # =========================
    # open_app validation
    # =========================
    elif action_type == "open_app":

        app_name = action.get("app")

        if not app_name:
            logger.warning("Validation failed: no app specified for open_app")
            return False

        logger.info(f"Validation: open_app action valid (app={app_name})")
        return True


    # =========================
    # open_website validation
    # =========================
    elif action_type == "open_website":

        url = action.get("url")

        if not url:
            logger.warning("Validation failed: no URL specified for open_website")
            return False

        if not isinstance(url, str):
            logger.warning(f"Validation failed: URL not string ({type(url)})")
            return False

        logger.info(f"Validation: open_website action valid (url={url[:50]}...)")
        return True


    # =========================
    # done validation
    # =========================
    elif action_type == "done":
        logger.info("Validation: done action valid")
        return True


    # =========================
    # Unknown but safe
    # =========================
    logger.info(f"Validation: unknown action type '{action_type}', allowing")
    return True
