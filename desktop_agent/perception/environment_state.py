from window_manager import get_active_window


def get_environment_state():

    title = get_active_window()

    if not title:
        return "unknown"


    title = title.lower()


    if "chrome" in title:
        return "chrome"


    if "powershell" in title:
        return "powershell"


    if "visual studio code" in title:
        return "vscode"


    return "unknown"